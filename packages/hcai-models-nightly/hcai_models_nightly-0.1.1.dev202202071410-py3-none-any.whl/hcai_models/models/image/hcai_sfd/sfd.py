from hcai_models.core.pytorch_model import PyTorchModel
from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.models.image.hcai_sfd.sfd_source import _S3FD
from hcai_models.utils import data_utils
from pathlib import Path
import torch
import numpy as np
import torch.nn.functional as F
import cv2
from hcai_models.utils.bbox_utils import nms


class S3FD(PyTorchModel, ImageModel):
    @property
    def reference_scale(self):
        return 195

    @property
    def reference_x_shift(self):
        return 0

    @property
    def reference_y_shift(self):
        return 0

    def __init__(self, *args, filter_thresh=0.5, **kwargs):
        kwargs.setdefault("include_top", True)
        super().__init__(*args, **kwargs)
        self.filter_threshold = filter_thresh

    # Public
    def postprocessing(self, prediction: object) -> np.ndarray:
        """
        Converts a single prediction of the s3fd model to the corresponding bounding boxes in the original image
        Args:
            prediction:
        Returns: Numpy array containing the bounding boxes of detected faces. The first dimension represents the number of faces found. The second dimension are the coordinates and the confidence score for the detection (x_upper_left, y_upper_left, x_lower_right, y_lower_right, score)
        """
        return prediction

    def preprocessing(self, sample, channel_order="RGB") -> np.ndarray:
        """
        Converts image from RGB to BGR and subtract mean values
        Args:
            sample: Numpy array with the shape (heights,width,channel)

        Returns: the cropped image, tuple of x and y offsets for the cropping window, the original image size
        """
        if channel_order == "RGB":
            sample = cv2.cvtColor(sample, cv2.COLOR_RGB2BGR)
        sample = sample.astype(np.float32)
        sample -= np.array([104.0, 117.0, 123.0])
        return sample

    # Overwrite inherited functions
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
        raise NotImplementedError("Blazeface does currently only support inference")

    def predict(self, sample):
        """Makes a prediction on a batch of images.
        Arguments:
            x: a NumPy array of shape (b, H, W, 3) or a PyTorch tensor of
               shape (b, 3, H, W).

        Returns:
            A list containing a tensor of face detections for each image in
            the batch. If no faces are found for an image, returns a tensor
            of shape (0,5).

        """

        self._model.to(self._device)

        # 1. Convert the images into tensors:
        if isinstance(sample, np.ndarray):
            sample = torch.from_numpy(sample).permute((0, 3, 1, 2))

        sample = sample.to(self._device)

        # 2. Run the neural network:
        with torch.no_grad():
            olist = self._model(sample)

        # 3. Postprocess raw predictions
        for i in range(len(olist) // 2):
            olist[i * 2] = F.softmax(olist[i * 2], dim=1)

        olist = [oelem.data.cpu().numpy() for oelem in olist]

        detections = self._get_predictions(olist, 1)
        filtered_detections = self._filter_bboxes(np.squeeze(detections))

        return filtered_detections

    # Private
    def _build_model(self):
        return _S3FD()

    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        pass

    def _info(self):
        pass

    def _decode(self, loc, priors, variances):
        """Decode locations from predictions using priors to undo
        the encoding we did for offset regression at train time.
        Args:
            loc (tensor): location predictions for loc layers,
                Shape: [num_priors,4]
            priors (tensor): Prior boxes in center-offset form.
                Shape: [num_priors,4].
            variances: (list[float]) Variances of priorboxes
        Return:
            decoded bounding box predictions
        """

        boxes = np.concatenate(
            (
                priors[:, :2] + loc[:, :2] * variances[0] * priors[:, 2:],
                priors[:, 2:] * np.exp(loc[:, 2:] * variances[1]),
            ),
            1,
        )
        boxes[:, :2] -= boxes[:, 2:] / 2
        boxes[:, 2:] += boxes[:, :2]
        return boxes

    def _get_predictions(self, olist, batch_size=1):
        bboxlists = []
        variances = [0.1, 0.2]
        for j in range(batch_size):
            bboxlist = []
            for i in range(len(olist) // 2):
                ocls, oreg = olist[i * 2], olist[i * 2 + 1]
                stride = 2 ** (i + 2)  # 4,8,16,32,64,128
                poss = zip(*np.where(ocls[:, 1, :, :] > 0.05))
                for Iindex, hindex, windex in poss:
                    axc, ayc = (
                        stride / 2 + windex * stride,
                        stride / 2 + hindex * stride,
                    )
                    score = ocls[j, 1, hindex, windex]
                    loc = oreg[j, :, hindex, windex].copy().reshape(1, 4)
                    priors = np.array(
                        [[axc / 1.0, ayc / 1.0, stride * 4 / 1.0, stride * 4 / 1.0]]
                    )
                    box = self._decode(loc, priors, variances)
                    x1, y1, x2, y2 = box[0]
                    bboxlist.append([x1, y1, x2, y2, score])

            bboxlists.append(bboxlist)

        bboxlists = np.array(bboxlists)
        return bboxlists

    def _filter_bboxes(self, bboxlist):
        if len(bboxlist) > 0:
            keep = nms(bboxlist, 0.3)
            bboxlist = bboxlist[keep, :]
            bboxlist = [x for x in bboxlist if x[-1] > self.filter_threshold]

        return bboxlist
