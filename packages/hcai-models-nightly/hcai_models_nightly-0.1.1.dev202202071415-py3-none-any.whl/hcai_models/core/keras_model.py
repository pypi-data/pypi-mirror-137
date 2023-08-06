"""Class to forward the abstract functions required by the abstract_model class to the keras api.
Keras models can inherit the methods implemented by this class to avoid duplicating boilerplate code.
"""

import tensorflow.keras as keras
from pathlib import Path
from hcai_models.core.abstract_model import Model, assert_model
from tensorflow.python.keras.layers import VersionAwareLayers


layers = VersionAwareLayers()


class KerasModel(Model):
    def __init__(self, *args, input_tensor=None, include_preprocessing=False, **kwargs):
        self.input_tensor = input_tensor
        self.include_preprocessing = include_preprocessing
        super().__init__(*args, **kwargs)

    # Public methods
    @assert_model
    def load_weights(self, weights: str = None, **kwargs) -> None:
        """
        Loading weights for the model either from filepath or by name. If weights argument is non self.weights is used instead.
        Args:
            *args: Additional arguments for the keras load weight function
            weights:  Either the filename to the weight file or the weight name as specified in the weights.csv file in the models directory.
            **kwargs: Additional keyword argument for the keras load weight function
        """
        if weights:
            self.weights = weights

        if Path(self.weights).is_file():
            weight_file = weights
        else:
            weight_file = self._get_weight_file()

        self._model.load_weights(filepath=weight_file, **kwargs)

    @assert_model
    def add_preprocessing_layers(self, preprocessing_layers: dict = None):
        """
        In keras models we can add the preprocessing layers directly to the network: https://www.tensorflow.org/guide/keras/preprocessing_layers#benefits_of_doing_preprocessing_inside_the_model_at_inference_time
        Adding preprocessing layers at the input of the model. If none, this will add the default preprocessing for the respective model will be added to the beginning.

        Args:
            preprocessing_layers: A dict of lists, of preprocessing layers to add before the built model. dict keys must match input tensors.
        """
        if preprocessing_layers is None:
            preprocessing_layers = self._get_default_preprocessing_layers()

        preprocessing_model_inputs = []
        preprocessing_model_outputs = []
        for m_input in self._model.inputs:
            new_input = keras.Input(shape=m_input.shape[1:], name=m_input.name)
            preprocessing_model_inputs.append(new_input)

            if new_input.name not in preprocessing_layers.keys():
                # plain Layer is used for identity
                output = keras.layers.Layer()(new_input)
            else:
                # thread input through provided layers
                pp_layers = preprocessing_layers[new_input.name]
                output = new_input
                for layer in pp_layers:
                    output = layer(output)
            preprocessing_model_outputs.append(output)

        pp_model = keras.Model(
            inputs=preprocessing_model_inputs, outputs=preprocessing_model_outputs
        )

        outputs = self._model(pp_model.outputs)
        inference_model = keras.Model(pp_model.inputs, outputs)
        inference_model.compile()
        return inference_model

    @assert_model
    #TODO: do we really want to keep the preprocessing fixed to keras preprocessing layers until overwritten?
    def preprocessing(self, ds):
        """
        Returns the preprocessing function for the model data. Might be empty.
        :param ds: The data to apply the preprocessing to
        :return: The preprocessed data
        """

        pp_layers = self._get_default_preprocessing_layers()
        for ppl in pp_layers:
            ds = ppl(ds)

        return ds

    # Private methods
    def _get_default_preprocessing_layers(self) -> dict:
        print(
            "WARNING: _get_default_preprocessing_layers has been called but no preprocessing layers have been specified"
        )
        return {}

    def _get_top_layers(self):
        top_layers = []
        if self.dropout_rate > 0:
            top_layers.append(layers.Dropout(self.dropout_rate, name="top_dropout"))

        if type(self.output_shape) == int:
            self.output_shape = (self.output_shape,)
        if not len(self.output_shape) == 1:
            raise ValueError("Outputshape should have exactly one dimension.")

        top_layers.append(
            layers.Dense(
                self.output_shape[0],
                activation=self.output_activation_function,
                name="predictions",
            )
        )

        return top_layers

    def _add_top_layers(
        self, model_heads: dict = None, outputs_as_list: object = False
    ) -> Model:
        """
        Adding the provided top to the model. If none, this will add the default top for the respective model.
        Args:
            model_heads: A dictionary containing an identifier for the model-head and a list of layers. Each list of layers will be added as separate top to the model in the given order.
            outputs_as_list: Indicates whether the output should be appended as dictionary or list. The keras models outputs can be accessed later using either name_identifiers (dict) or indices (list).
        """

        x = self._model.output
        outputs = {}

        if model_heads is None:
            layers = self._get_top_layers()
            for layer in layers:
                x = layer(x)
            outputs["prediction"] = x

        else:
            for name, layer_list in model_heads.items():
                # Connect the first layer of the new head
                h = layer_list[0](x)
                for layer in layer_list[1:]:
                    h = layer(h)
                outputs[name] = h

        if outputs_as_list:
            outputs = list(outputs.values())

        self._model = keras.Model(
            inputs=self._model.inputs, outputs=outputs, name=self.name
        )

    # Pass-through functions to Keras Model API
    def compile(self, *args, **kwargs):
        return self._model.compile(*args, **kwargs)

    def fit(self, *args, **kwargs):
        return self._model.fit(*args, **kwargs)

    def predict(self, *args, **kwargs):
        return self._model.predict(*args, **kwargs)

    def summary(self, *args, **kwargs):
        return self._model.summary(*args, **kwargs)

    def save(self, *args, **kwargs):
        return self._model.save(*args, **kwargs)
