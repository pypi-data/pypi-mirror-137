from abc import ABC, abstractmethod


class SSIModel(ABC):

    # TODO check if we need to make this static
    @abstractmethod
    def get_options(self):
        raise NotImplemented()

    @abstractmethod
    def train(self, data, label_score, opts, vars):
        raise NotImplemented()

    @abstractmethod
    def forward(self, data, probs_or_score, opts, vars):
        raise NotImplemented()

    @abstractmethod
    def load(self, path, opts, vars):
        raise NotImplemented()

    @abstractmethod
    def save(self, path, opts, vars):
        raise NotImplemented()


class SSIBridgeModel(ABC):
    ...
