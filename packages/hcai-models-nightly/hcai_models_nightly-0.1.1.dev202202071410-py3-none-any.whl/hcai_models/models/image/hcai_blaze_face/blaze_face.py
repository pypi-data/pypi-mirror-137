from hcai_models.core.pytorch_model import PyTorchModel
from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.models.image.hcai_blaze_face.blaze_face_source import _BlazeFace
from hcai_models.utils.image_utils import resize_and_crop_image
from hcai_models.utils import data_utils
from pathlib import Path
import torch
import numpy as np


class BlazeFace(PyTorchModel, ImageModel):
    @property
    def reference_scale(self):
        return 195

    @property
    def reference_x_shift(self):
        return 0

    @property
    def reference_y_shift(self):
        return 0

    def __init__(self, *args, min_score_thres=0.5, min_supression_thresh=0.3, **kwargs):
        """

        Args:
            *args: Optional args for parent classes
            min_score_thres: Minimum confidence score for a bounding box to be returned
            min_supression_thresh: Minimum confidence score for a bounding box candidate not be suppressed
            **kwargs: *args: Optional kargs for parent classes
        """
        super().__init__(*args, **kwargs)
        self.min_score_thresh = min_score_thres
        self.min_suppression_thresh = min_supression_thresh

    # Public
    def postprocessing(self, prediction: list, shifts, orig_size) -> np.ndarray:
        """
        Converts a single prediction of the blazeface model to the corresponding bounding boxes in the original image
        Args:
            prediction:
            shifts:
            orig_size:

        Returns: Numpy array containing the bounding boxes of detected faces. The first dimension represents the number of faces found. The second dimension are the coordinates and the confidence score for the detection (x_upper_left, y_upper_left, x_lower_right, y_lower_right, score)
        """
        prediction = prediction[0]
        xshift, yshift = shifts
        shift = np.array([xshift, yshift] * 2)
        scores = prediction[:, -1:]
        locs = np.concatenate(
            (
                prediction[:, 1:2],
                prediction[:, 0:1],
                prediction[:, 3:4],
                prediction[:, 2:3],
            ),
            axis=1,
        )

        detected_faces = np.concatenate((locs * orig_size + shift, scores), axis=1)
        return detected_faces

    def preprocessing(self, sample):
        """
        Crops the image to fit the 128 x 128 x 3 dimensions required by the blaze face model and normalizes the pixelvalues to be in the range of [-1,1]
        Args:
            sample: Numpy array with the shape (heights,width,channel)

        Returns: the cropped image, tuple of x and y offsets for the cropping window, the original image size
        """

        # Resizing and cropping
        H, W, C = sample.shape
        orig_size = min(H, W)
        cropped_img, (xshift, yshift) = resize_and_crop_image(sample, 128)

        # Scaling
        cropped_img = np.ndarray.astype(cropped_img, dtype=np.float32) / 127.5 - 1.0

        return cropped_img, (xshift, yshift), orig_size

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
            x: a NumPy array of shape (b, H, W, C) or a PyTorch tensor of
               shape (b, 3, H, C). The height and width should be 128 pixels.

        Returns:
            A list containing a tensor of face detections for each image in
            the batch. If no faces are found for an image, returns a tensor
            of shape (0, 17).

        Each face detection is a PyTorch tensor consisting of 17 numbers:
            - ymin, xmin, ymax, xmax
            - x,y-coordinates for the 6 keypoints
            - confidence score
        """
        self._model.to(self._device)

        if isinstance(sample, np.ndarray):
            sample = torch.from_numpy(sample).permute((0, 3, 1, 2))

        assert sample.shape[1] == 3
        assert sample.shape[2] == 128
        assert sample.shape[3] == 128

        # 1. Preprocess the images into tensors:
        sample = sample.to(self._device)

        # 2. Run the neural network:
        with torch.no_grad():
            out = self._model(sample)

        # 3. Postprocess the raw predictions:
        detections = self._model._tensors_to_detections(
            out[0], out[1], self._model.anchors
        )

        # 4. Apply weighted non-maximum suppression to remove overlapping detections:
        filtered_detections = []
        for i in range(len(detections)):
            faces = self._model._weighted_non_max_suppression(detections[i])
            faces = torch.stack(faces) if len(faces) > 0 else torch.zeros((0, 17))
            filtered_detections.append(faces)

        return filtered_detections

    def load_weights(self, weights: str = None, anchors: str = None, **kwargs) -> None:
        """
        Loading weights for the model either from filepath or by name. If weights argument is none self.weights is used instead.
        If a path to the weight file is passed the path to the anchor file needs to be passed as well
        Args:
            weights: Either the filename to the weight file or the weight name as specified in the weights.csv file in the models directory.
            anchors: Path to the anchor file of the model.
            **kwargs:
        """
        if weights:
            self.weights = weights
        if not self.weights:
            raise ValueError("No weights have been specified")

        if Path(self.weights).is_file():
            if not anchors:
                raise ValueError(
                    "Path to the weight file but missing path to the anchor file."
                )
            weight_file = weights
            anchor_file = anchors
        else:
            weights = self._available_weights[self.weights]
            weight_file = Path(
                data_utils.get_file(
                    fname=self.model_name + "_" + self.weights + ".pth",
                    origin=weights.download_url,
                    file_hash=weights.hash,
                    extract=False,
                )
            )
            anchor_file = Path(
                data_utils.get_file(
                    fname=self.model_name + "_" + self.weights + "_anchors.npy",
                    origin=weights.url_add,
                    file_hash=weights.url_add_hash,
                    extract=False,
                )
            )

        # Loading weights
        self._model.load_state_dict(torch.load(weight_file))
        self._model.eval()

        # Loading anchors
        self._model.anchors = torch.tensor(
            np.load(anchor_file), dtype=torch.float32, device=self._device
        )

    # Private
    def _build_model(self):
        model = _BlazeFace()
        # Optionally change the thresholds:
        model.min_score_thresh = self.min_score_thresh
        model.min_suppression_thresh = self.min_suppression_thresh
        return model

    def _add_top_layers(self, model_heads: dict = None, **kwargs) -> object:
        pass

    def _info(self):
        pass
