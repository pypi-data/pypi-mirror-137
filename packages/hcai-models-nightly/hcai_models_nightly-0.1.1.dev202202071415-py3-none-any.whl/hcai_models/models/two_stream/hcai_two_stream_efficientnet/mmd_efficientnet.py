from tensorflow import keras

from hcai_models.expansion.keras.losses import MaximumMeanDiscrepancyLoss
from hcai_models.models.two_stream.hcai_two_stream_efficientnet.abstract_two_stream_efficientnet import (
    AbstractTwoStreamEfficientnet,
)


class MMDEfficientnet(AbstractTwoStreamEfficientnet):
    """
    Two Efficientnets trained simultaneously on different datasets, with MMD-based losses between
    several equivalent layers.
    """

    def _get_loss_heads_by_layer(self) -> dict:
        pool_and_mmd = [keras.layers.GlobalMaxPooling2D(), MaximumMeanDiscrepancyLoss()]
        return {
            "block5c_add": pool_and_mmd,
            "block6d_add": pool_and_mmd,
            "top_activation": pool_and_mmd,
        }

    def _info(self):
        return ""  # TODO
