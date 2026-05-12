import numpy as np
from scipy.ndimage import uniform_filter

def func_SSIM(img1, img2):
    """
    Computes the Structural Similarity Index (SSIM) between two images.

    Parameters:
    img1 : numpy.ndarray
        First image with dimensions [512, 512, 3].
    img2 : numpy.ndarray
        Second image with dimensions [512, 512, 3].

    Returns:
    float
        The SSIM value (a scalar between -1 and 1, typically close to 1 for similar images).
    """
    # Constants from the SSIM paper
    K1 = 0.01
    K2 = 0.03
    L = 255  # dynamic range of pixel values

    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2

    # Convert to float for computation
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    # Compute means using uniform filter (Gaussian window is also common)
    window_size = 11
    mu1 = uniform_filter(img1, size=window_size, mode='constant')
    mu2 = uniform_filter(img2, size=window_size, mode='constant')

    # Compute variances and covariance
    sigma1_sq = uniform_filter(img1 ** 2, size=window_size, mode='constant') - mu1 ** 2
    sigma2_sq = uniform_filter(img2 ** 2, size=window_size, mode='constant') - mu2 ** 2
    sigma12 = uniform_filter(img1 * img2, size=window_size, mode='constant') - mu1 * mu2

    # SSIM map per pixel
    ssim_map = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / \
               ((mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2))

    # Return mean SSIM across all pixels and channels
    return np.mean(ssim_map)

