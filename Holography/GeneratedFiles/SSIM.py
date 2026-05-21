import numpy as np
from scipy.ndimage import uniform_filter, gaussian_filter


def func_SSIM(img1, img2):
    """
    Calculate the Structural Similarity Index (SSIM) between two images.
    
    Args:
        img1: First image with shape [512, 512, 3], normalized to [0, 1]
        img2: Second image with shape [512, 512, 3], normalized to [0, 1]
    
    Returns:
        ssim_value: A scalar representing the mean SSIM across all channels
    """
    # Constants for SSIM calculation
    # K1 and K2 are small constants to avoid instability
    K1 = 0.01
    K2 = 0.03
    
    # Dynamic range is 1.0 since images are normalized to [0, 1]
    L = 1.0
    
    # Calculate C1 and C2
    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2
    
    # Convert to float64 for precision
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    
    # Use Gaussian filter with sigma=1.5 and window size 11x11
    # This is the standard configuration for SSIM
    sigma = 1.5
    
    # Calculate means using Gaussian filter
    mu1 = gaussian_filter(img1, sigma=sigma, mode='reflect')
    mu2 = gaussian_filter(img2, sigma=sigma, mode='reflect')
    
    # Calculate squared means
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    
    # Calculate variances and covariance
    sigma1_sq = gaussian_filter(img1 ** 2, sigma=sigma, mode='reflect') - mu1_sq
    sigma2_sq = gaussian_filter(img2 ** 2, sigma=sigma, mode='reflect') - mu2_sq
    sigma12 = gaussian_filter(img1 * img2, sigma=sigma, mode='reflect') - mu1_mu2
    
    # Calculate SSIM map
    numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
    
    ssim_map = numerator / denominator
    
    # Return the mean SSIM value across all pixels and channels
    ssim_value = np.mean(ssim_map)
    
    return ssim_value

