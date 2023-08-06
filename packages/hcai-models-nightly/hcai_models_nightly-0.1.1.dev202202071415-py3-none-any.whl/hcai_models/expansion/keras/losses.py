import os

if __name__ == "__main__":
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from tensorflow import keras
from tensorflow.keras import backend as K
import tensorflow as tf


class MaximumMeanDiscrepancyLoss(keras.losses.Loss):
    """
    The MMD is a batchwise distance measure, which approximates that probability that tensor x and y
    are taken from different distributions by comparing in-batch differences with between-batch differences.
    This variant is implemented with a gaussian kernel as a distance measure.
    In practice, it can also be used as a loss.
    It is commonly used in transfer learning or teacher-student setups.
    """

    def __init__(self, name="mmd", *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)

    def _compute_kernel(self, x, y):
        # x and y are assumed to be of equal shape
        batch_size = K.shape(x)[0]
        embedding_dims = K.shape(x)[1]
        tiled_x = K.tile(
            K.reshape(x, [batch_size, 1, embedding_dims]), [1, batch_size, 1]
        )
        tiled_y = K.tile(
            K.reshape(y, [1, batch_size, embedding_dims]), [batch_size, 1, 1]
        )
        # gaussian kernel, downscaled by batch size. standard deviation in the gaussian has been omitted
        return K.exp(-K.square(tiled_x - tiled_y)) / K.cast(batch_size, tf.float32)

    def call(self, y_true, y_pred):
        x_kernel = self._compute_kernel(y_true, y_true)
        y_kernel = self._compute_kernel(y_pred, y_pred)
        xy_kernel = self._compute_kernel(y_true, y_pred)
        # MMD is essentially pointwise along the embedding dimension, comparing between batches
        return K.mean(x_kernel + y_kernel - (2 * xy_kernel))


if __name__ == "__main__":
    _batch_size = 3
    _embedding_size = 4
    _shape = (_batch_size, _embedding_size)

    # x = tf.random.normal(shape=_shape, mean=0.0, stddev=0.5)
    # y = tf.random.uniform(shape=_shape, minval=-1.0, maxval=1.0)

    # x = tf.random.normal(shape=_shape, mean=0.0, stddev=0.5)
    # y = tf.random.normal(shape=shape, mean=0.0, stddev=2.0)

    x = tf.ones(shape=_shape)
    y = tf.zeros(shape=_shape)

    mmd_loss = MaximumMeanDiscrepancyLoss()

    print("*** X ***")
    print(x.numpy())
    print("*** Y ***")
    print(y.numpy())
    print("*** Kernel X|X ***")
    x_kernel_val = mmd_loss._compute_kernel(x, x)
    print(x_kernel_val.numpy())
    print("*** Kernel Y|Y ***")
    y_kernel_val = mmd_loss._compute_kernel(y, y)
    print(y_kernel_val.numpy())
    print("*** Kernel X|Y ***")
    xy_kernel_val = mmd_loss._compute_kernel(x, y)
    print(xy_kernel_val.numpy())
    print("*** MMD ***")
    mmd = mmd_loss.call(x, y)
    print(mmd.numpy())
