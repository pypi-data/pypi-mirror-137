# https://github.com/tensorflow/datasets/blob/2a97ad01378f5e63c410aa3eb36aa688aab62bdd/tensorflow_datasets/core/registered.py#L109
# Internal registry containing <str registered_name, Model subclass>
import inspect

_MODEL_REGISTRY = {}
_ABSTRACT_MODEL_REGISTRY = {}


class RegisteredModel:
    """
    Abstract base class for all weights.csv.
    Registers models upon import.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Set the name if the dataset does not define it.
        # Use __dict__ rather than getattr so subclasses are not affected.
        if not cls.__dict__.get("name"):
            cls.name = cls.__name__

        elif cls.name in _MODEL_REGISTRY:
            raise ValueError(f"Dataset with name {cls.name} already registered.")
        is_abstract = inspect.isabstract(cls)
        if is_abstract:
            _ABSTRACT_MODEL_REGISTRY[cls.name] = cls
        else:
            _MODEL_REGISTRY[cls.name] = cls

    def list_available_models(self):
        all_models = [model_name for model_name, model_class in _MODEL_REGISTRY.items()]
        return sorted(all_models)
