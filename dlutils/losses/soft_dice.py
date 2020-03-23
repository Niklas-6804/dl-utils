from typing import Callable
import torch
from dlutils.utils.tensor_ops import make_onehot, reduce

__all__ = [
    'SoftDiceLoss',
    'soft_dice_loss'
]


def soft_dice_loss(predictions, targets, weight: torch.Tensor = None,
                   non_lin: Callable = None, square_nom: bool = False,
                   square_denom: bool = False, smooth: float = 1.,
                   reduction: str = 'elementwise_mean'):
    # number of classes for onehot
    n_classes = predictions.shape[1]
    with torch.no_grad():
        targets_onehot = make_onehot(targets, n_classes=n_classes)
    # sum over spatial dimensions
    dims = tuple(range(2, predictions.dim()))

    # apply nonlinearity
    if non_lin is not None:
        predictions = non_lin(predictions)

    # compute nominator
    if square_nom:
        nom = torch.sum((predictions * targets_onehot.float()) ** 2, dim=dims)
    else:
        nom = torch.sum(predictions * targets_onehot.float(), dim=dims)
    nom = 2 * nom + smooth

    # compute denominator
    if square_denom:
        i_sum = torch.sum(predictions ** 2, dim=dims)
        t_sum = torch.sum(targets_onehot ** 2, dim=dims)
    else:
        i_sum = torch.sum(predictions, dim=dims)
        t_sum = torch.sum(targets_onehot, dim=dims)

    denom = i_sum + t_sum.float() + smooth

    # compute loss
    frac = nom / denom

    # apply weight for individual classesproperly
    if weight is not None:
        frac = weight * frac

    # average over classes
    frac = - torch.mean(frac, dim=1)

    return reduce(frac, reduction)


class SoftDiceLoss(torch.nn.Module):
    def __init__(self, square_nom=False, square_denom=False, weight=None,
                 smooth=1., reduction="elementwise_mean", non_lin=None):
        """
        SoftDice Loss
        Parameters
        ----------
        square_nom : bool
            square nominator
        square_denom : bool
            square denominator
        weight : iterable
            additional weighting of individual classes
        smooth : float
            smoothing for nominator and denominator
        """
        super().__init__()
        self.square_nom = square_nom
        self.square_denom = square_denom

        self.smooth = smooth

        if weight is not None:
            self.register_buffer("weight", torch.tensor(weight))
        else:
            self.weight = None

        self.reduction = reduction
        self.non_lin = non_lin

    def forward(self, predictions, targets):
        """
        Compute SoftDice Loss
        Parameters
        ----------
        inp : torch.Tensor
            prediction
        targets : torch.Tensor
            ground truth tensor
        Returns
        -------
        torch.Tensor
            loss
        """

        return soft_dice_loss(predictions=predictions,
                              targets=targets,
                              weight=self.weight,
                              non_lin=self.non_lin,
                              square_nom=self.square_nom,
                              square_denom=self.square_denom,
                              smooth=self.smooth,
                              reduction=self.reduction)