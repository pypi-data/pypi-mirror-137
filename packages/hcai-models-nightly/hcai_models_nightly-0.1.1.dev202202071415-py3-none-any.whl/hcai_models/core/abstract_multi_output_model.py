from abc import ABC, abstractmethod

from hcai_models.core.abstract_model import Model


class AbstractMultiOutputModel(Model, ABC):
    def __init__(self, output_shapes: dict = None, *args, **kwargs):

        # reject canonic shape settings
        if "output_shape" in kwargs:
            raise ValueError(
                f"output_shape is not well-defined in multi output models. use output_shapes instead."
            )

        if output_shapes is None:
            self.output_shapes = self.get_default_output_shapes()
        else:
            for key in self.get_default_output_shapes().keys():
                if key not in output_shapes.keys():
                    raise ValueError(f"output_shapes dict requires a value for {key}.")
            self.output_shapes = output_shapes

        super().__init__(*args, **kwargs)

    @abstractmethod
    def get_default_output_shapes(self) -> dict:
        """
        Returns: a dict mapping output tensor names to their expected shapes
        Used in model construction and input tensor verification
        """
        raise NotImplementedError()
