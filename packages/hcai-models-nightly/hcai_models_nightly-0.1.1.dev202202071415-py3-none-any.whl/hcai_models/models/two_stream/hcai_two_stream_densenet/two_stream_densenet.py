from pathlib import Path

from hcai_models.expansion.keras.losses import MaximumMeanDiscrepancyLoss
from hcai_models.models.two_stream.abstract_two_stream_model import (
    AbstractTwoStreamModel,
)
from tensorflow import keras


class TwoStreamDensenet(AbstractTwoStreamModel):
    VARIANTS = ["121"]

    DISTANCE_LOSSES = ["mmd"]

    def __init__(
        self,
        input_shapes: dict = None,
        output_shapes: dict = None,
        densenet_variant: str = "121",
        distance_loss: str = "mmd",
        **kwargs,
    ):
        if distance_loss not in TwoStreamDensenet.DISTANCE_LOSSES:
            raise ValueError(f"unknown distance loss {distance_loss}")
        self.distance_loss = distance_loss
        if densenet_variant not in TwoStreamDensenet.VARIANTS:
            raise ValueError(f"unknown efficientnet variant {densenet_variant}")
        self.efficientnet_variant = densenet_variant
        super().__init__(input_shapes, output_shapes, **kwargs)

    def get_default_input_shapes(self) -> dict:
        return {
            "label_source": (1),
            "label_target": (1),
            "image_source": (224, 224, 3),  # TODO adapt size for variants
            "image_target": (224, 224, 3),
        }

    def get_default_output_shapes(self) -> dict:
        return {"prediction_source": (6), "prediction_target": (6)}

    def preprocessing(self, ds):
        pass

    def load_weights(self, filepath: str = None, **kwargs):
        if filepath:
            self.weights = filepath

        if Path(self.weights).is_file():
            weight_file = filepath
        else:
            weight_file = self._get_weight_file()
        self._model.load_weights(filepath=weight_file, **kwargs)

    def _get_loss_heads_by_layer(self) -> dict:
        return {}  # TODO

    def _make_baseline_model(self, input_tensor):
        return keras.applications.DenseNet121(
            include_top=True,
            weights="imagenet",
            input_tensor=input_tensor,
        )

    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        raise NotImplementedError()

    def _info(self):
        return ""  # TODO
