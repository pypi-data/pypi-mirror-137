import tensorflow as tf
import tensorflow.keras.applications.efficientnet as keras_efficient_net
import tensorflow.keras as keras

from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.core.keras_model import KerasModel
from tensorflow.python.keras.layers import VersionAwareLayers

layers = VersionAwareLayers()

_DESCRIPTION = """
Convolutional Neural Networks (ConvNets) are commonly developed at a fixed resource budget, and then scaled up for better accuracy if more resources are available. 
In this paper, we systematically study model scaling and identify that carefully balancing network depth, width, and resolution can lead to better performance. 
Based on this observation, we propose a new scaling method that uniformly scales all dimensions of depth/width/resolution using a simple yet highly effective compound coefficient. We demonstrate the effectiveness of this method on scaling up MobileNets and ResNet. 
To go even further, we use neural architecture search to design a new baseline network and scale it up to obtain a family of models, called EfficientNets, which achieve much better accuracy and efficiency than previous ConvNets.
"""

_CITATION = """
@inproceedings{tan2019efficientnet,
  title={Efficientnet: Rethinking model scaling for convolutional neural networks},
  author={Tan, Mingxing and Le, Quoc},
  booktitle={International Conference on Machine Learning},
  pages={6105--6114},
  year={2019},
  organization={PMLR}
}
"""

DENSE_KERNEL_INITIALIZER = {
    "class_name": "VarianceScaling",
    "config": {"scale": 1.0 / 3.0, "mode": "fan_out", "distribution": "uniform"},
}


class EfficientNet(ImageModel, KerasModel):
    def __init__(self, *args, default_input_size, keras_build_func, **kwargs):
        # Overwriting default parameters
        kwargs.setdefault("input_height", default_input_size)
        kwargs.setdefault("input_width", default_input_size)
        kwargs.setdefault("input_channels", 3)

        # Init parents
        super().__init__(*args, **kwargs)

        # Init
        self.keras_build_func = keras_build_func

    # Public
    def postprocessing(self, sample, **kwargs):
        return sample

    # Private
    def _build_model(self):
        # Build input
        inputs = tf.keras.Input((None, None, self.n_channels))
        x = inputs

        # (Optional) Add preprocessing layers
        if self.include_preprocessing:
            for ppl in self._get_preprocessing_layers():
                x = ppl(x)

        # Getting base model
        x = self.keras_build_func(input_tensor=x, include_top=False, weights=None).output

        # Apply pooling
        if self.pooling == "avg":
            x = layers.GlobalAveragePooling2D()(x)
        elif self.pooling == "max":
            x = layers.GlobalMaxPooling2D()(x)

        # (Optional) Adding top
        if self.include_top:
            for tl in self._get_top_layers():
                x = tl(x)

        x = keras.Model(inputs=inputs, outputs=x, name=self.name)
        return x

    def _info(self):
        return ""

    def _get_preprocessing_layers(self) -> list:
        """
        Returns: A list of preprocessing layers to apply. Might be empty.
        """
        return [
            layers.Resizing(self.in_height, self.in_width),
        ]


class EfficientNetB0(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=224,
            keras_build_func=keras_efficient_net.EfficientNetB0,
            **kwargs
        )


class EfficientNetB1(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=240,
            keras_build_func=keras_efficient_net.EfficientNetB1,
            **kwargs
        )


class EfficientNetB2(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=260,
            keras_build_func=keras_efficient_net.EfficientNetB2,
            **kwargs
        )


class EfficientNetB3(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=300,
            keras_build_func=keras_efficient_net.EfficientNetB3,
            **kwargs
        )


class EfficientNetB4(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=380,
            keras_build_func=keras_efficient_net.EfficientNetB4,
            **kwargs
        )


class EfficientNetB5(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=456,
            keras_build_func=keras_efficient_net.EfficientNetB5,
            **kwargs
        )


class EfficientNetB6(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=528,
            keras_build_func=keras_efficient_net.EfficientNetB6,
            **kwargs
        )


class EfficientNetB7(EfficientNet):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            default_input_size=600,
            keras_build_func=keras_efficient_net.EfficientNetB7,
            **kwargs
        )
