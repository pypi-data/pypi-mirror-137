import tensorflow as tf
import tensorflow.keras as keras
from hcai_models.core.abstract_model import assert_model
from hcai_models.core.abstract_audio_model import AudioModel
from hcai_models.core.keras_model import KerasModel
from tensorflow.python.keras.layers import VersionAwareLayers
from hcai_models.expansion.keras.layers import SmartResizing

layers = VersionAwareLayers()

_DESCRIPTION = """
We learn rich natural sound representations by capitalizing on large amounts of unlabeled sound data collected in the wild. We leverage the natural synchronization between vision and sound to learn an acoustic representation using two-million unlabeled videos. 
Unlabeled video has the advantage that it can be economically acquired at massive scales, yet contains useful signals about natural sound. 
We propose a student-teacher training procedure which transfers discriminative visual knowledge from well established visual recognition models into the sound modality using unlabeled video as a bridge. 
Our sound representation yields significant performance improvements over the state-of-the-art results on standard benchmarks for acoustic scene/object classification. 
Visualizations suggest some high-level semantics automatically emerge in the sound network, even though it is trained without ground truth labels.
"""

_CITATION = """
@article{aytar2016soundnet,
  title={Soundnet: Learning sound representations from unlabeled video},
  author={Aytar, Yusuf and Vondrick, Carl and Torralba, Antonio},
  journal={Advances in neural information processing systems},
  volume={29},
  pages={892--900},
  year={2016}
}
"""


class Soundnet(AudioModel, KerasModel):
    def __init__(self, *args, **kwargs):
        # Overwriting default parameters
        kwargs.setdefault("in_sr", 22050)
        kwargs.setdefault("n_channels", 1)

        # Init parents
        super().__init__(
            *args,
            **kwargs
        )

    def _build_model(self):
        # Build input
        inputs = tf.keras.Input((self.in_sr, self.n_channels))
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

    def _get_model(self) -> keras.Model:
        """
        Builds up the SoundNet model and loads the weights from a given model file (8-layer model is kept at models/sound8.npy).
        :return:
        """


        model = Sequential()
        model.add(InputLayer(batch_input_shape=(1, None, 1)))

        filter_parameters = [{'name': 'conv1', 'num_filters': 16, 'padding': 32,
                              'kernel_size': 64, 'conv_strides': 2,
                              'pool_size': 8, 'pool_strides': 8},

                             {'name': 'conv2', 'num_filters': 32, 'padding': 16,
                              'kernel_size': 32, 'conv_strides': 2,
                              'pool_size': 8, 'pool_strides': 8},

                             {'name': 'conv3', 'num_filters': 64, 'padding': 8,
                              'kernel_size': 16, 'conv_strides': 2},

                             {'name': 'conv4', 'num_filters': 128, 'padding': 4,
                              'kernel_size': 8, 'conv_strides': 2},

                             {'name': 'conv5', 'num_filters': 256, 'padding': 2,
                              'kernel_size': 4, 'conv_strides': 2,
                              'pool_size': 4, 'pool_strides': 4},

                             {'name': 'conv6', 'num_filters': 512, 'padding': 2,
                              'kernel_size': 4, 'conv_strides': 2},

                             {'name': 'conv7', 'num_filters': 1024, 'padding': 2,
                              'kernel_size': 4, 'conv_strides': 2},

                             {'name': 'conv8_2', 'num_filters': 401, 'padding': 0,
                              'kernel_size': 8, 'conv_strides': 2},
                             ]

        for x in filter_parameters:
            model.add(ZeroPadding1D(padding=x['padding']))
            model.add(Conv1D(x['num_filters'],
                             kernel_size=x['kernel_size'],
                             strides=x['conv_strides'],
                             padding='valid'))
            weights = model_weights[x['name']]['weights'].reshape(model.layers[-1].get_weights()[0].shape)
            biases = model_weights[x['name']]['biases']

            model.layers[-1].set_weights([weights, biases])

            if 'conv8' not in x['name']:
                gamma = model_weights[x['name']]['gamma']
                beta = model_weights[x['name']]['beta']
                mean = model_weights[x['name']]['mean']
                var = model_weights[x['name']]['var']

                model.add(BatchNormalization())
                model.layers[-1].set_weights([gamma, beta, mean, var])
                model.add(Activation('relu'))
            if 'pool_size' in x:
                model.add(MaxPooling1D(pool_size=x['pool_size'],
                                       strides=x['pool_strides'],
                                       padding='valid'))

