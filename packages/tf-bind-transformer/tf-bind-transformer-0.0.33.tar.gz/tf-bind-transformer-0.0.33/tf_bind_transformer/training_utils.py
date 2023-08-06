import torch
from torch import nn
from torch.optim import AdamW
from tf_bind_transformer.data import read_bed, collate_dl_outputs, get_dataloader, remap_df_add_experiment_target_cell
from tf_bind_transformer.data import RemapAllPeakDataset, NegativePeakDataset, ScopedNegativePeakDataset

def exists(val):
    return val is not None

def separate_weight_decayable_params(params):
    no_wd_params = set([param for param in params if param.ndim < 2])
    wd_params = set(params) - no_wd_params
    return wd_params, no_wd_params

def get_optimizer(params, lr = 3e-4, wd = 1e-1, filter_by_requires_grad = False):
    if filter_by_requires_grad:
        params = list(filter(lambda t: t.requires_grad, params))

    params = set(params)
    wd_params, no_wd_params = separate_weight_decayable_params(params)

    param_groups = [
        {'params': list(wd_params)},
        {'params': list(no_wd_params), 'weight_decay': 0},
    ]

    return AdamW(param_groups, lr = lr, weight_decay = wd)

# simple Trainer class

class Trainer(nn.Module):
    def __init__(
        self,
        model,
        *,
        remap_bed_file,
        negative_bed_file,
        factor_fasta_folder,
        fasta_file,
        train_chromosome_ids,
        valid_chromosome_ids,
        batch_size,
        validate_every = 250,
        grad_clip_norm = None,
        grad_accum_every = 1,
        held_out_targets = [],
        held_out_cell_types = [],
        context_length = 4096,
        shuffle = False,
        train_sample_frac = 1.,
        valid_sample_frac = 1.,
        remap_sample_frac = 1.,
        shift_aug_range = (-2, 2),
        rc_aug = True,
        experiments_json_path = None,
        read_value_aux_loss = False,
        checkpoint_filename = './checkpoint.pt',
        include_scoped_negs = False,
        scoped_negs_remap_bed_path = None,
        scoped_negs_path = None,
        scoped_negs_exts = '.bed.bool.npy'
    ):
        super().__init__()
        self.model = model

        remap_df = read_bed(remap_bed_file)

        if remap_sample_frac < 1:
            remap_df = remap_df.sample(frac = remap_sample_frac)

        remap_df = remap_df_add_experiment_target_cell(remap_df)

        neg_df = read_bed(negative_bed_file)

        self.ds = RemapAllPeakDataset(
            remap_df = remap_df,
            fasta_file = fasta_file,
            factor_fasta_folder = factor_fasta_folder,
            filter_chromosome_ids = train_chromosome_ids,
            exclude_targets = held_out_targets,
            exclude_cell_types = held_out_cell_types,
            context_length = context_length,
            remap_df_frac = train_sample_frac,
            shift_augs = shift_aug_range,
            rc_aug = rc_aug,
            experiments_json_path = experiments_json_path
        )

        self.neg_ds = NegativePeakDataset(
            remap_df = remap_df,
            negative_df = neg_df,
            fasta_file = fasta_file,
            factor_fasta_folder = factor_fasta_folder,
            filter_chromosome_ids = train_chromosome_ids,
            exclude_targets = held_out_targets,
            exclude_cell_types = held_out_cell_types,
            context_length = context_length,
            experiments_json_path = experiments_json_path
        )

        self.valid_ds = RemapAllPeakDataset(
            remap_df = remap_df,
            fasta_file = fasta_file,
            factor_fasta_folder = factor_fasta_folder,
            include_targets = held_out_targets,
            include_cell_types = held_out_cell_types,
            filter_chromosome_ids = valid_chromosome_ids,
            context_length = context_length,
            remap_df_frac = valid_sample_frac,
            shift_augs = shift_aug_range,
            rc_aug = rc_aug,
            experiments_json_path = experiments_json_path
        )

        self.valid_neg_ds = NegativePeakDataset(
            remap_df = remap_df,
            negative_df = neg_df,
            fasta_file = fasta_file,
            factor_fasta_folder = factor_fasta_folder,
            filter_chromosome_ids = valid_chromosome_ids,
            include_targets = held_out_targets,
            include_cell_types = held_out_cell_types,
            context_length = context_length,
            experiments_json_path = experiments_json_path
        )

        self.include_scoped_negs = include_scoped_negs

        self.dl = get_dataloader(self.ds, cycle_iter = True, shuffle = shuffle, batch_size = batch_size)
        self.neg_dl = get_dataloader(self.neg_ds, cycle_iter = True, shuffle = shuffle, batch_size = batch_size)

        if include_scoped_negs:
            self.scoped_neg_ds = ScopedNegativePeakDataset(
                fasta_file = fasta_file,
                factor_fasta_folder = factor_fasta_folder,
                numpy_folder_with_scoped_negatives = scoped_negs_path,
                exts = scoped_negs_exts,
                remap_bed_file = scoped_negs_remap_bed_path,
            )
            self.scoped_neg_dl = get_dataloader(self.scoped_neg_ds, cycle_iter = True, shuffle = shuffle, batch_size = batch_size)

        self.valid_dl = get_dataloader(self.valid_ds, cycle_iter = True, shuffle = shuffle, batch_size = batch_size)
        self.valid_neg_dl = get_dataloader(self.valid_neg_ds, cycle_iter = True, shuffle = shuffle, batch_size = batch_size)

        self.read_value_aux_loss = read_value_aux_loss

        self.optim = get_optimizer(model.parameters())

        self.grad_accum_every = grad_accum_every
        self.grad_clip_norm = grad_clip_norm

        self.validate_every = validate_every
        self.register_buffer('steps', torch.Tensor([0.]))

        self.checkpoint_filename = checkpoint_filename

    def forward(
        self,
        finetune_enformer_ln_only = True,
        **kwargs
    ):
        curr_step = int(self.steps.item())
        self.model.train()

        total_train_loss = 0
        for _ in range(self.grad_accum_every):
            dl_outputs = [next(self.dl), next(self.neg_dl)]

            if self.include_scoped_negs:
                dl_outputs.append(next(self.scoped_neg_dl))

            seq, tf_aa, contextual_texts, peaks_nr, read_value, binary_target = collate_dl_outputs(*dl_outputs)
            seq, binary_target, read_value, peaks_nr = seq.cuda(), binary_target.cuda(), read_value.cuda(), peaks_nr.cuda()

            loss, aux_loss = self.model(
                seq,
                target = binary_target,
                aa = tf_aa,
                contextual_free_text = contextual_texts,
                finetune_enformer_ln_only = finetune_enformer_ln_only,
                read_value = read_value,
                peaks_nr = peaks_nr,
                **kwargs
            )

            total_loss = self.model.combine_losses(loss, aux_loss)
            total_train_loss += total_loss.item()
            (total_loss / self.grad_accum_every).backward()

        avg_loss = total_train_loss / self.grad_accum_every
        logs = {'loss': avg_loss}
        print(f'{curr_step} loss: {avg_loss}')

        if exists(self.grad_clip_norm):
            nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip_norm)

        self.optim.step()
        self.optim.zero_grad()

        if (curr_step % self.validate_every) == 0:
            self.model.eval()

            total_valid_loss = 0
            total_valid_accuracies = 0

            for _ in range(self.grad_accum_every):
                seq, tf_aa, contextual_texts, peaks_nr, read_value, binary_target = collate_dl_outputs(next(self.valid_dl), next(self.valid_neg_dl))
                seq, binary_target = seq.cuda(), binary_target.cuda()

                valid_logits = self.model(
                    seq,
                    aa = tf_aa,
                    contextual_free_text = contextual_texts,
                )

                valid_loss = self.model.loss_fn(valid_logits, binary_target.float())
                valid_accuracy = ((valid_logits.sigmoid() > 0.5).int() == binary_target).sum() / (binary_target.numel())

                total_valid_loss += valid_loss.item()
                total_valid_accuracies += valid_accuracy.item()

            avg_valid_loss = total_valid_loss / self.grad_accum_every
            avg_valid_accuracy = total_valid_accuracies / self.grad_accum_every

            logs = {
                **logs,
                'valid_loss': avg_valid_loss,
                'valid_accuracy': avg_valid_accuracy
            }

            print(f'{curr_step} valid loss: {avg_valid_loss}')
            print(f'{curr_step} valid accuracy: {avg_valid_accuracy}')

            if curr_step > 0:
                torch.save(self.model.state_dict(), self.checkpoint_filename)

        self.steps += 1
        return logs
