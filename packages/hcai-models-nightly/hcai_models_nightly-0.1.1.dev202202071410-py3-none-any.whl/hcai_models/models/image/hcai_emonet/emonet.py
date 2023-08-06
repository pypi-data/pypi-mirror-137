from typing import Union

from hcai_models.core.abstract_multi_output_model import AbstractMultiOutputModel
from hcai_models.core.pytorch_model import PyTorchModel
from hcai_models.models.image.hcai_emonet.emonet_source import _EmoNet


class EmoNet8(PyTorchModel, AbstractMultiOutputModel):
    def __init__(self, *args, **kwargs):
        super().__init__(output_shapes=None, *args, **kwargs)

    # Public
    def postprocessing(self, sample):
        return sample

    def get_default_output_shapes(self) -> dict:
        return {
            "heatmap": (68, 64, 64),
            "expression": 8,
            "valence": 1,
            "arousal": 1,
        }

    def _build_model(self):
        return _EmoNet()

    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        pass

    def _info(self):
        pass

class EmoNet5(PyTorchModel, AbstractMultiOutputModel):
    def __init__(self, *args, **kwargs):
        super().__init__(output_shapes=None, *args, **kwargs)

    # Public
    def postprocessing(self, sample):
        return sample

    def get_default_output_shapes(self) -> dict:
        return {
            "heatmap": (68, 64, 64),
            "expression": 5,
            "valence": 1,
            "arousal": 1,
        }

    def _build_model(self):
        return _EmoNet(n_expression=5)

    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        pass

    def _info(self):
        pass
