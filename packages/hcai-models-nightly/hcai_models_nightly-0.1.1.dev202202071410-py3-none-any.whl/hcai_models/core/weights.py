import numpy as np


class Weights:

    # Overwrite to include a description of the weights.csv in the documentation
    _DESCRIPTION = ""

    def __init__(
        self,
        download_url,
        hash,
        output_shape=None,
        download_url_no_top=None,
        hash_no_top=None,
        url_add=None,
        url_add_hash=None
    ):
        """
        Args:
            download_url: The url from where to download the weights.csv
            hash: The sha256 hash of the weight file
            output_shape: Shape of the outputs of the network. Only necessary if the model is build with the original top
            download_url_no_top: Download path for the weightfile with no model top
            hash_no_top: The sha256 hash of the weight file with no model top
            url_add: Comma separated string of additional URLS that are specific to the model code
            url_add_hash: Comma separated string of sha256 hashes for the additional download urls

        """
        self.download_url = download_url
        self.hash = hash
        self.download_url_no_top = download_url_no_top
        self.hash_no_top = hash_no_top
        self.output_shape = (
            (output_shape,) if np.isscalar(output_shape) else output_shape
        )
        self.url_add = url_add
        self.url_add_hash = url_add_hash
