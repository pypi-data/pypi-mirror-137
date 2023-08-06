from hcai_models.core.abstract_model import Model


class AudioModel(Model):
    """
    Abstract base class for audio models.
    Specifies specific functionality of audio models and ensures compatibility with the interface for external calls.
    """

    def __init__(self, *args, in_sr=16000, n_channels=1, **kwargs):

        self.in_sr = in_sr
        self.n_channels = n_channels
        kwargs.setdefault("input_shape", (in_sr, n_channels))
        assert len(kwargs["input_shape"]) == 2
        super().__init__(*args, **kwargs)

    def get_input_sample_rate(self):
        return self.input_shape[0]

    def get_n_channels(self):
        return self.input_shape[1]
