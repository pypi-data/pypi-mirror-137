import numpy as np
import torch


class AbstractMetric:
    """
    Abstract superclass for use with instances of PyTorchModel which can be used to
    implement losses or metrics
    """

    def __init__(self, metric_fn, name: str):
        self.metric_fn = metric_fn
        self.name = name
        self._result_cache = []

    def get_single(self, batch, model_outputs):
        """
        Args:
            batch: whole batch of dataset, any format
            model_outputs: whole model outputs, any format

        Returns: single scalar result of metric or pytorch loss
        """
        raise NotImplementedError()

    def process_batch(self, batch, model_outputs):
        self._result_cache.append(self.get_single(batch, model_outputs))

    def get_result(self):
        return np.average(self._result_cache)

    def reset(self):
        self._result_cache = []


class MetricByIndex(AbstractMetric):
    """
    Wraps any scalar-valued function for use as a metric in PyTorchModel,
    for cases where data indices in the dataset match model outputs
    Can handle dict keys or list indices
    """

    def __init__(self, metric_fn, name: str, index):
        """
        Args:
            metric_fn: Scalar-valued function
            name: Display name
            index: string key or index of data and model output to compare
        """
        super().__init__(metric_fn, name)
        self.index = index

    def get_single(self, batch, model_outputs):
        batch_pred = np.squeeze(model_outputs[self.index].cpu().numpy())
        batch_gt = np.squeeze(batch[self.index].cpu().numpy())
        return self.metric_fn(batch_pred, batch_gt)


class MetricMapping(AbstractMetric):
    """
    Wraps any scalar-valued function for use as a metric in PyTorchModel,
    for cases where data indices in the dataset do not match model outputs
    Can handle dict keys or list indices
    """

    def __init__(self, metric_fn, name: str, index_data, index_output):
        """
        Args:
            metric_fn: Scalar-valued function
            name: Display name
            index_data: string key or index of data
            index_output: string key or index of model output. None for single-output models
        """
        super().__init__(metric_fn, name)
        self.index_output = index_output
        self.index_data = index_data

    def get_single(self, batch, model_outputs):
        if self.index_output is None:
            batch_pred = np.squeeze(model_outputs.cpu().numpy())
        else:
            batch_pred = np.squeeze(model_outputs[self.index_output].cpu().numpy())
        batch_gt = np.squeeze(batch[self.index_data].cpu().numpy())
        return self.metric_fn(batch_gt, batch_pred)


class LossMapping(AbstractMetric):
    """
    Wraps Pytorch losses for use in Pytorch models,
    and maps model outputs and data indices
    """

    def __init__(self, loss_fn, name: str, index_data, index_output):
        """
        Args:
            loss_fn: Pytorch loss function
            name: Display name
            index_data: string key or index of data
            index_output: string key or index of model output. None for single-output models
        """
        super().__init__(loss_fn, name)
        self.index_output = index_output
        self.index_data = index_data
        if torch.cuda.is_available():
            self._device = torch.device("cuda")
        else:
            self._device = torch.device("cpu")

    def process_batch(self, batch, model_outputs):
        self._result_cache.append(self.get_single(batch, model_outputs).item())

    def get_single(self, batch, model_outputs):
        if self.index_output is not None:
            out = model_outputs[self.index_output]
        else:
            out = model_outputs
        return self.metric_fn(
            out.to(self._device), batch[self.index_data].to(self._device)
        )
