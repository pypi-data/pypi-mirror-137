import csv
import sys
import ast
import hcai_models.utils.data_utils as data_utils
from abc import ABC, abstractmethod
from pathlib import Path
from hcai_models.core.registered_model import RegisteredModel
from hcai_models.core.ssi_compat import SSIModel, SSIBridgeModel
from hcai_models.core.weights import Weights


def assert_model(func):
    """
    Decorator to assert that the model has been set before calling the function
    """

    def inner(self, *args, **kwargs):
        assert self._model is not None
        return func(self, *args, **kwargs)

    return inner


class Model(ABC, RegisteredModel):
    """
    Abstract base class for all models.
    Specifies general functionality of the models and ensures compatibility with the interface for external calls.
    """

    def __init__(
        self,
        *args,
        model_name=None,
        input_shape=None,
        output_shape=None,
        include_top=False,
        dropout_rate=0.2,
        weights=None,
        output_activation_function="softmax",
        optimizer="adam",
        loss="categorical_crossentropy",
        pooling="avg",
        **kwargs
    ):

        self._available_weights = self._init_weights()
        self.info = self._info()
        self._model = None

        self.model_name = model_name if model_name else self.__class__.__name__
        self.input_shape = input_shape
        self.include_top = include_top
        self.dropout_rate = dropout_rate
        self.weights = weights
        self.output_shape = (
            output_shape if output_shape else self._determine_output_shape()
        )
        self.output_activation_function = output_activation_function
        self.pooling = pooling
        self.optimizer = optimizer
        self.loss = loss

    # Public
    def build_model(self):
        self._model = self._build_model()
        if self.weights:
            self.load_weights()

    @assert_model
    def add_top_layers(self, model_heads=None):
        self._add_top_layers(model_heads)

    def is_ssi_model(self):
        return issubclass(self.__class__, SSIModel)

    def is_ssi_bridge_model(self):
        return issubclass(self.__class__, SSIBridgeModel)

    # Private
    def _init_weights(self):
        # Loading entries from the weights.csv file from the directory of the model module
        module_path = sys.modules[self.__module__].__file__
        weights_path = Path(module_path).parent / "weights.csv"
        weight_dict = {}
        if not weights_path.exists():
            return weight_dict
        with open(weights_path, encoding="UTF-8") as csv_file:
            csv_dict = csv.DictReader(csv_file, delimiter=";", )
            list_of_rows = [dict_row for dict_row in csv_dict]

        for row in list_of_rows:
            if row["ModelClass"].lower() == self.__class__.__name__.lower():
                name = row.get("Name", None)
                shape = ast.literal_eval(row.get("OutputShape", None))
                url = row.get("Download URL", None)
                hash = row.get("Hash", None)
                url_no_top = row.get("Download URL without top", None)
                hash_no_top = row.get("Hash without top", None)
                url_add = row.get('Download URL additional', None)
                url_add_hash = row.get('Hash URL additional', None)

                # Clean inputs
                hash = None if not hash else hash
                hash_no_top = None if not hash_no_top else hash_no_top

                weight_dict[name] = Weights(
                    download_url=url,
                    hash=hash,
                    output_shape=shape,
                    download_url_no_top=url_no_top,
                    hash_no_top=hash_no_top,
                    url_add=url_add,
                    url_add_hash=url_add_hash
                )

        return weight_dict

    def _get_weight_file(self) -> Path:
        #TODO: This default case only makes sense when dealing with keras models. Refactor accordingly
        """
        Retrieves the weights for pretrained models. The weights will be loaded from the url specified in the _available_weights for the respective weights of the model.
        Once downloaded the data will be cached at `~/.hcai_models/weights` unless specified otherwise.
        :return: Path to the downloaded weights
        """
        if not self.weights:
            raise ValueError("No weights have been specified")
        if self.weights not in self._available_weights.keys():
            raise ValueError("Specified weights not found in available weights")
        weights = self._available_weights[self.weights]

        if self.include_top:
            file_name = self.model_name + "_" + self.weights + ".h5"
            hash = weights.hash
            url = weights.download_url
        else:
            file_name = self.model_name + "_" + self.weights + "_notop.h5"
            hash = weights.hash_no_top
            url = weights.download_url_no_top
        return Path(
            data_utils.get_file(
                fname=file_name,
                origin=url,
                file_hash=hash,
                extract=not url.endswith(".h5"),
            )
        )

    def _determine_output_shape(self):
        if not self.weights:
            return None
        else:
            if self.weights not in self._available_weights.keys():
                print(
                    "Cannot automatically infer shape.{} not found in available weights.".format(
                        self.weights
                    )
                )
                return None
            else:
                return self._available_weights[self.weights].output_shape

    # Public Abstract
    @abstractmethod
    def preprocessing(self, sample: object) -> object:
        """
        Preprocesses the input data. Only use for static preprocessing that should be replicated once the model is fully trained (e.g input normalization)
        :return:

        Args:
            sample: One input sample for the model to process
        """
        raise NotImplemented()


    @abstractmethod
    def postprocessing(self, prediction: object, **kwargs) -> object:
        """
        Postprocessing function of the the model output (e.g. output smoothing, or bounding box coordinate conversion)
        :return:

        Args:
            sample: One input sample for the model to process
        """
        raise NotImplemented()

    @abstractmethod
    def load_weights(self, filepath):
        """
        Loads weights.csv the weights.csv of a model
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def predict(self, sample):
        """
        Predict the given sample
        Args:
            sample:
        """
        raise NotImplementedError()

    @abstractmethod
    def fit(
        self,
        *args,
        x=None,
        y=None,
        batch_size=None,
        epochs=1,
        validation_split=0.0,
        validation_data=None,
        **kwargs
    ):
        """
        Fits the model on the provided data. The parameter
        :return:
        """
        raise NotImplemented()

    # Private Abstract Methods
    @abstractmethod
    def _build_model(self):
        """
        Builds the model as specified by the set class parameters and returns it
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        """
        Adding the provided top to the model. If none, this will add the default top for the respective model.
        Args:
            model_heads: A dictionary containing an identifier for the model-head and a list of layers. Each list of layers will be added as separate top to the model in the given order.
            **kwargs: The specific implementation might contain additional function arguments
        """
        raise NotImplemented()

    @abstractmethod
    def _info(self):
        """
        Returns additional information for the model as markdown formatted string
        :return:
        """
        raise NotImplemented()
