import tensorflow as tf
import tensorflow.keras as keras
from hcai_models.core.abstract_model import assert_model
from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.core.keras_model import KerasModel
from tensorflow.python.keras.layers import VersionAwareLayers
from hcai_models.expansion.keras.layers import SmartResizing

layers = VersionAwareLayers()

_DESCRIPTION = """
Convolutional networks are at the core of most state-of-the-art computer vision solutions for a wide variety of tasks. 
Since 2014 very deep convolutional networks started to become mainstream, yielding substantial gains in various benchmarks. 
Although increased model size and computational cost tend to translate to immediate quality gains for most tasks (as long as enough labeled data is provided for training), 
computational efficiency and low parameter count are still enabling factors for various use cases such as mobile vision and big-data scenarios. 
Here we explore ways to scale up networks in ways that aim at utilizing the added computation as efficiently as possible by suitably factorized convolutions and aggressive regularization. 
We benchmark our methods on the ILSVRC 2012 classification challenge validation set demonstrate substantial gains over the state of the art: 
21.2% top-1 and 5.6% top-5 error for single frame evaluation using a network with a computational cost of 5 billion multiply-adds per inference and with using less than 25 million parameters.
With an ensemble of 4 models and multi-crop evaluation, we report 3.5% top-5 error on the validation set (3.6% error on the tests set) and 17.3% top-1 error on the validation set.
"""

_CITATION = """
@inproceedings{szegedy2016rethinking,
  title={Rethinking the inception architecture for computer vision},
  author={Szegedy, Christian and Vanhoucke, Vincent and Ioffe, Sergey and Shlens, Jon and Wojna, Zbigniew},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={2818--2826},
  year={2016}
}
"""


class InceptionV3(ImageModel, KerasModel):
    def __init__(self, *args, **kwargs):
        # Overwriting default parameters
        kwargs.setdefault("input_height", 299)
        kwargs.setdefault("input_width", 299)
        kwargs.setdefault("input_channels", 3)

        # Init parents
        super().__init__(
            *args,
            #keras_build_func=keras.applications.inception_v3.InceptionV3,
            **kwargs
        )

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
            for ppl in self._get_default_preprocessing_layers():
                x = ppl(x)

        # Getting base model
        x = keras.applications.InceptionV3(
            input_tensor=x, include_top=False, weights=None
        ).output

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

    def _get_default_preprocessing_layers(self) -> list:
        """
        Returns: A list of preprocessing layers to apply. Might be empty.
        """
        return [
            SmartResizing(self.in_height, self.in_width),
            layers.Rescaling(1.0 / 127.0, offset=-1),
        ]
