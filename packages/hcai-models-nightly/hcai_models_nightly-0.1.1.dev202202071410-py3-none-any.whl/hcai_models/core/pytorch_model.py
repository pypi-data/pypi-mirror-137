import time

import numpy as np
import torch
from pathlib import Path
from torch.utils.data import Dataset, TensorDataset, DataLoader
from hcai_models.core.abstract_model import Model, assert_model
import hcai_models.utils.data_utils as data_utils


class PyTorchModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if torch.cuda.is_available():
            self._device = torch.device("cuda")
        else:
            self._device = torch.device("cpu")

    @assert_model
    def save(self, filepath: str):
        torch.save(self._model.state_dict(), filepath)

    @assert_model
    def preprocessing(self, ds):
        pass

    # Public methods
    @assert_model
    def load_weights(self, weights: str = None, **kwargs) -> None:
        """
        Loading weights for the model either from filepath or by name. If weights argument is non self.weights is used instead.
        Args:
            weights:  Either the filename to the weight file or the weight name as specified in the weights.csv file in the models directory.
        """
        if weights:
            self.weights = weights

        if Path(self.weights).is_file():
            weight_file = weights
        else:
            weight_file = self._get_weight_file()

        self._model.load_state_dict(torch.load(weight_file))

    @assert_model
    def get_parameters(self):
        return self._model.parameters()

    @assert_model
    def predict(self, sample):
        with torch.no_grad():
            if isinstance(sample, np.ndarray):
                sample = torch.tensor(np.expand_dims(sample,0))
                sample.to(self._device)
            self._model.to(self._device)
            return self._model(sample)

    @assert_model
    def eval(
        self, x, input_keys: list = None, losses=None, metrics=None, y=None, batch_size=32
    ):
        """
        Args:
            x: inputs, list typed or pytorch dataset
            input_keys: list string or integer to use as model inputs, in order
            losses: list of losses extending torch_utils.AbstractMetric
            metrics: list of metrics extending torch_utils.AbstractMetric
            y: if x is list typed, list typed target values, else None
            batch_size: batch size to use

        Returns: dict of metric and loss results
        """

        if not input_keys:
            input_keys = [0]
        if not losses:
            losses = []
        if not metrics:
            metrics = []

        self._model.to(self._device)
        data = self._prep_loader(x, y, batch_size, self._device)

        with torch.no_grad():
            r = self._test_loop(
                data,
                losses=losses,
                metrics=metrics,
                input_keys=input_keys,
                verbose=True,
            )
        return r

    @assert_model
    def fit(
        self,
        x,
        losses,
        optimizer,
        input_keys: list = [0],
        metrics=None,
        batch_size=32,
        epochs=1,
        y=None,
        val_x=None,
        val_y=None,
        scheduler=None,
        *args,
        **kwargs,
    ):

        """
        Args:
            x: training set, list typed or pytorch dataset
            losses: list of losses extending torch_utils.AbstractMetric
            optimizer: pytorch optimizer
            input_keys: list string or integer to use as model inputs, in order
            metrics: list of metrics extending torch_utils.AbstractMetric
            batch_size: batch size to use
            epochs: epochs of training
            y: if x is list typed, list typed target values, else None
            val_x: validation set, list typed or pytorch dataset
            val_y: if val_x is list typed, list typed target values, else None
            scheduler: pytorch scheduler or None
            *args:
            **kwargs:

        Returns: None

        """

        data = self._prep_loader(x, y, batch_size, self._device)

        validation_loader = None
        if val_x is not None:
            validation_loader = self._prep_loader(
                val_x, val_y, batch_size, self._device
            )

        self._model.to(self._device)

        for i in range(epochs):
            self._train_loop(
                data,
                losses=losses,
                metrics=metrics,
                optimizer=optimizer,
                input_keys=input_keys,
            )
            if scheduler is not None:
                scheduler.step()
            if validation_loader is not None:
                with torch.no_grad():
                    r = self._test_loop(
                        data_loader=validation_loader,
                        input_keys=input_keys,
                        metrics=metrics,
                        losses=losses,
                    )
                str_out = f"Epoch {i}: "
                for s in [f" {k}: {r[k]:>7f}" for k in r.keys()]:
                    str_out = str_out + s
                print(str_out)
        pass

    # Private Methods

    def _prep_loader(self, x, y=None, batch_size: int = 32, device=None):
        """
        Either assert that x is a valid Dataset, or construct a Dataset from x,y

        Args:
            x: Input values or Dataset
            y: if x is raw values, raw target values
            batch_size: batch size for dataloader
            device: if constructing a dataset, torch device to use

        Returns: pytorch DataLoader based on inputs
        """
        if isinstance(x, Dataset):
            data_set = x
        elif x is not None and y is not None:
            t_x = torch.tensor(x, device=device)
            t_y = torch.tensor(y, device=device)
            data_set = TensorDataset(
                t_x,
                t_y,
            )
        else:
            raise ValueError(
                "data needs to be a torch.utils.data.Dataset as x, or matching "
                "iterables x and y "
            )
        return DataLoader(data_set, batch_size=batch_size)

    @assert_model
    def _train_loop(
        self, data, losses, optimizer, input_keys: list, metrics: list = []
    ):
        """

        Args:
            data: pytorch DataLoader
            losses: list of losses extending torch_utils.AbstractMetric
            optimizer: pytorch optimizer
            input_keys: indices to of data to use as model inputs, in order
            metrics: list of metrics extending torch_utils.AbstractMetric

        Returns: None

        """

        self._model.train()  # switch model to train mode, enabling dropouts ect.

        size = len(data)

        # reset result caches
        for m in metrics:
            m.reset()

        for batch, input_data in enumerate(data):

            model_inputs = [input_data[k].to(self._device) for k in input_keys]
            output = self._model(*model_inputs)

            loss_results = []
            for loss in losses:
                loss_results.append(loss.get_single(input_data, output))

            with torch.no_grad():
                for metric in metrics:
                    metric.process_batch(batch=input_data, model_outputs=output)

            # Backpropagation
            optimizer.zero_grad()
            for lr in loss_results:
                lr.backward()
            optimizer.step()

            if batch % 100 == 0:
                loss = sum([lr.item() for lr in loss_results])
                str_out = f"[{batch:>5d}/{size:>5d}] loss: {loss:>7f}"
                for s in [f" {m.name}: {m.get_result():>7f}" for m in metrics]:
                    str_out = str_out + s
                for m in metrics:
                    m.reset()
                print(str_out)

    @assert_model
    def _test_loop(
        self,
        data_loader: DataLoader,
        input_keys: list,
        losses: list = [],
        metrics: list = [],
        verbose: bool = False,
    ) -> dict:
        """

        Args:
            data_loader: The input data. Currently only pytorch data loaders are supported
            losses: list of PyTorch losses
            metrics: List of wrappers extending AbstractMetric
        Returns: dict of metric and loss results

        """

        self._model.eval()  # switch model to eval mode, disabling dropouts etc

        # reset result caches
        for m in metrics:
            m.reset()
        for loss in losses:
            loss.reset()

        size = len(data_loader)
        # process all batches
        t_b = time.time()
        for i, input_data in enumerate(data_loader):

            with torch.no_grad():

                if input_keys:
                    model_inputs = [input_data[k].to(self._device) for k in input_keys]
                    output = self._model(*model_inputs)

            for metric in metrics:
                metric.process_batch(batch=input_data, model_outputs=output)

            for loss in losses:
                loss.process_batch(batch=input_data, model_outputs=output)

            if verbose:
                t_f = time.time() - t_b
                t_b = time.time()
                print(f"[{i+1:>5d}/{size:>5d}, {t_f:>.2f} sec]")

        # calculate and collect averages
        ret = {}
        for loss in losses:
            ret[loss.name] = loss.get_result()
            loss.reset()
        for metric in metrics:
            ret[metric.name] = metric.get_result()
            metric.reset()

        return ret

    def _get_weight_file(self) -> Path:
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
            file_name = self.model_name + "_" + self.weights + ".pth"
            hash = weights.hash
            url = weights.download_url
        else:
            file_name = self.model_name + "_" + self.weights + "_notop.pth"
            hash = weights.hash_no_top
            url = weights.download_url_no_top
        return Path(
            data_utils.get_file(
                fname=file_name,
                origin=url,
                file_hash=hash,
                extract=not url.endswith(".pth"),
            )
        )
