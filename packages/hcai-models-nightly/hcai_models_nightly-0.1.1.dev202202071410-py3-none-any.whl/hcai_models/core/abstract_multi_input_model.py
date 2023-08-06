from abc import ABC, abstractmethod

from hcai_models.core.abstract_model import Model


class AbstractMultiInputModel(Model, ABC):
    def __init__(self, input_shapes: dict, *args, **kwargs):

        # reject one-dimensional shape settings
        if "input_shape" in kwargs:
            raise ValueError(
                f"input_shape is not well-defined in multi input output models. use input_shapes instead."
            )

        # set either the default input/output shape dict OR assert that all keys are present in the user param
        if input_shapes is None:
            self.input_shapes = self.get_default_input_shapes()
        else:
            for key in self.get_default_input_shapes().keys():
                if key not in input_shapes.keys():
                    raise ValueError(f"input_shapes dict requires a value for {key}.")
            self.input_shapes = input_shapes

        super().__init__(*args, **kwargs)

    @abstractmethod
    def get_default_input_shapes(self) -> dict:
        """
        Returns: a dict mapping input tensor names to their expected shapes
        Used in model construction and input tensor verification
        """
        raise NotImplementedError()
