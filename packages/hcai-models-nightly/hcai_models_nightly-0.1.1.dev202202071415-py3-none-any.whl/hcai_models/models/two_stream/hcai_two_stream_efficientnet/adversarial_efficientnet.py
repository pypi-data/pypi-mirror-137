from tensorflow import keras

from hcai_models.expansion.keras.layers import GradientReversalLayer, SourceLabelLayer
from hcai_models.models.two_stream.hcai_two_stream_efficientnet.abstract_two_stream_efficientnet import (
    AbstractTwoStreamEfficientnet,
)


class AdversarialEfficientnet(AbstractTwoStreamEfficientnet):
    """
    Two Efficientnets trained simultaneously on different datasets, with an adversarial
    loss included.
    """

    def _get_loss_heads_by_layer(self) -> dict:
        adversarial_stack = [
            keras.layers.GlobalMaxPooling2D(),
            GradientReversalLayer(),
            keras.layers.Dense(64, activation="sigmoid"),
            keras.layers.Dense(32, activation="sigmoid"),
            keras.layers.Dense(1, activation="softmax"),
            keras.losses.BinaryCrossentropy(),
        ]
        return {
            "top_activation": adversarial_stack,
        }

    def _make_distance_losses(self, model, prefixes: list):
        """
        Assuming a model with two identical streams or branches, a given loss is applied
        between layers of the same same within their models respective prefixed namespaces

        :param model: 2-streamed keras model
        :param prefixes: prefixes of the models two branches
        :return: None
        """
        losses = []

        loss_dict = self._get_loss_heads_by_layer()
        for block, layers in loss_dict.items():
            stream_src = model.get_layer(f"{prefixes[0]}{block}")
            if stream_src is None:
                raise ValueError(
                    f"unknown model layer {block} in the loss_heads definition. Check your implementation."
                )
            stream_src = stream_src.output
            stream_trg = model.get_layer(f"{prefixes[1]}{block}").output

            label_layer = SourceLabelLayer()(stream_src, stream_trg)
            batch = label_layer[0]
            labels = label_layer[1]

            for i, layer in enumerate(layers):
                # actual comparison layer
                if i == len(layers) - 1:
                    losses.append(layer(batch, labels))
                # transformations before comparison
                else:
                    batch = layer(batch)
        return losses

    def _info(self):
        return ""  # TODO
