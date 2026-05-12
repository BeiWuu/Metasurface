import numpy as np

def func_FWHM(waveform):
    """
    Calculate the full width at half maximum (FWHM) of a waveform.

    Parameters:
    waveform (array-like): A one-dimensional waveform array.

    Returns:
    float: The FWHM value in nanometers.
    """
    # Spacing between adjacent points (nm)
    spacing = 160.0

    # Find the maximum value and the half-maximum value
    max_val = np.max(waveform)
    half_max = max_val / 2.0

    # Find indices where the waveform crosses the half-maximum
    # on the rising edge
    rising_crossings = []
    for i in range(len(waveform) - 1):
        if waveform[i] < half_max <= waveform[i + 1]:
            # Linear interpolation for more accurate crossing point
            fraction = (half_max - waveform[i]) / (waveform[i + 1] - waveform[i])
            rising_crossings.append(i + fraction)

    # Find indices where the waveform crosses the half-maximum
    # on the falling edge
    falling_crossings = []
    for i in range(len(waveform) - 1):
        if waveform[i] >= half_max > waveform[i + 1]:
            # Linear interpolation for more accurate crossing point
            fraction = (half_max - waveform[i + 1]) / (waveform[i] - waveform[i + 1])
            falling_crossings.append(i + 1 - fraction)

    # If crossing points are found, calculate FWHM
    if rising_crossings and falling_crossings:
        # Use the first rising crossing and the last falling crossing
        left_idx = rising_crossings[0]
        right_idx = falling_crossings[-1]
        width_in_indices = right_idx - left_idx
        fwhm = width_in_indices * spacing
        return fwhm
    else:
        # If no crossing points found (e.g., flat waveform), return 0
        return 0.0

