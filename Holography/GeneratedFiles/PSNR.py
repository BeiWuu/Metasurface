import numpy as np


def func_PSNR(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Measure the similarity between two images using the PSNR metric.

    Parameters
    ----------
    image1 : np.ndarray
        First image with shape [512, 512, 3], values normalized to [0, 1].
    image2 : np.ndarray
        Second image with shape [512, 512, 3], values normalized to [0, 1].

    Returns
    -------
    float
        PSNR value in dB. A higher value indicates greater similarity.
        Returns infinity if the two images are identical (MSE == 0).
    """
    assert image1.shape == (512, 512, 3), "image1 must have shape [512, 512, 3]"
    assert image2.shape == (512, 512, 3), "image2 must have shape [512, 512, 3]"

    # Dynamic range is 1.0 because inputs are normalized to [0, 1]
    max_pixel_value = 1.0

    mse = np.mean((image1.astype(np.float64) - image2.astype(np.float64)) ** 2)

    if mse == 0:
        return float("inf")

    psnr = 10.0 * np.log10((max_pixel_value ** 2) / mse)

    return float(psnr)

