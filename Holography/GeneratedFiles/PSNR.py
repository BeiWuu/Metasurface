import numpy as np

def func_PSNR(image1, image2):
    """
    Compute the Peak Signal-to-Noise Ratio (PSNR) between two images.

    Parameters:
    image1 (numpy.ndarray): First image with shape [512, 512, 3].
    image2 (numpy.ndarray): Second image with shape [512, 512, 3].

    Returns:
    float: PSNR value in dB.
    """
    # Ensure the images are of type float64 for accurate computation
    image1 = image1.astype(np.float64)
    image2 = image2.astype(np.float64)

    # Compute Mean Squared Error (MSE)
    mse = np.mean((image1 - image2) ** 2)

    # If MSE is zero, the images are identical; return infinity (or a large number)
    if mse == 0:
        return float('inf')

    # Maximum possible pixel value (assuming 8-bit images, range [0, 255])
    max_pixel = 255.0

    # Compute PSNR
    psnr = 10 * np.log10((max_pixel ** 2) / mse)

    return psnr

