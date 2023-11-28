import numpy as np
from Calculations.Image_Import import tissue_hounsfield_units


# Also according to Samei2020, bin width should be 1 HU
samei_bin_width = 1
# Also according to Samei2020, kernel size should be 7 x 7
samei_kernel = 7
samei_mask_size = 6  # mm

standard_slice = {'3mm': 3}


def get_kernel_in_pixel(pixel_in_mm: float, kernel_in_mm: float):
    """
                For a kernel size in mm, return the kernel size in (odd) number of pixels

                Parameters
                ----------
                pixel_in_mm : float
                    Size of one pixel in mm
                kernel_in_mm: float
                    Size of the noise mask in mm

                Returns
                -------
                int:
                    Noise mask expressed as an odd number of pixels (int)
        """
    pixels_in_kernel = kernel_in_mm / pixel_in_mm
    odd_kernels = (pixels_in_kernel - 1) / 2
    odd_pixel_kernel = (np.round(odd_kernels, 0) * 2 + 1).astype(int)
    return odd_pixel_kernel


def extend_matrix_2d(matrix: np.ndarray, extend_px: int):
    """
        For any convolution calculation, the matrix needs to be extended to allow convolution in the image borders.
        Therefore, a border is added to the image with values comparable to the nearest pixel in the original image

        Parameters
        ----------
        matrix : ndarray
            Current image
        extend_px: int
            Amount of pixels that the matrix extends at all sides

        Returns
        -------
        ndarray: extended_image
            -extended_image (np.ndarray): Matrix with the extended image
    """
    [dy, dx] = matrix.shape
    extended_image = np.zeros([dy + 2 * extend_px, dx + 2 * extend_px])

    # Center ofr the extended image is the current image
    extended_image[extend_px:dy + extend_px, extend_px:dx + extend_px] = matrix

    # Each corner is extended as the current corner pixel
    extended_image[0:extend_px, 0:extend_px] = matrix[0, 0]
    extended_image[extend_px + dy:, 0:extend_px] = matrix[dy - 1, 0]
    extended_image[0:extend_px, extend_px + dx:] = matrix[0, dx - 1]
    extended_image[extend_px + dy:, extend_px + dx:] = matrix[dy - 1, dx - 1]

    # The borders are extended outwards with the corresponding values of
    for i in range(extend_px):
        extended_image[extend_px:extend_px + dy, i] = matrix[0:dy, 0]
        extended_image[i, extend_px:extend_px + dx] = matrix[0, 0:dx]
        extended_image[extend_px:extend_px + dy, i + extend_px + dx] = matrix[0:dy, dx - 1]
        extended_image[i + extend_px + dy, extend_px:extend_px + dx] = matrix[dy - 1, 0:dx]
    return extended_image


def construct_noise_map(image, mask_size=samei_kernel):
    # This method has the same result of taking a convolution of the image with a 3 x 3 matrix and calculating STD in
    #     each masked region. However, the shift matrix approach is 4-5 times faster!
    # R is the radius of the mask
    r = int((mask_size - 1) // 2)
    image_shape = image.shape
    y_dim, x_dim = image_shape

    # There will be the same number of shift matrices as the total number of pixels in one mask
    kernel_pixels = (2 * r + 1) ** 2
    shift_matrices = [[]] * kernel_pixels

    # The shift matrix calculation is done in a matrix with size of the image + r at both sides
    extended_image = extend_matrix_2d(image, r)

    # The first step towards calculating the SD, is calculating the average and shift matrices
    average = np.zeros(image_shape)
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            shift_matrix_x = np.roll(extended_image, i, axis=1)
            shift_matrix = np.roll(shift_matrix_x, j, axis=0)[r: r + y_dim, r: r + x_dim]

            average = average + shift_matrix / kernel_pixels
            index = (i + r) * (2 * r + 1) + (j + r)
            shift_matrices[index] = shift_matrix

    # The next step is calculating the variance, and later SD
    variance = np.zeros(image_shape)
    for shift_matrix in shift_matrices:
        variance = variance + np.square(shift_matrix - average) / kernel_pixels
    noise_map = np.sqrt(variance)
    return noise_map


def histogram_mode(values, bin_width=samei_bin_width):
    # This function takes an array of positive values (STD measurements), bins them with a certain bin width, constructs
    #       a histogram and returns the mode of that histogram
    noise_bins = np.arange(0, max(values) + bin_width, bin_width)
    histogram, noise_bins = np.histogram(values, bins=noise_bins)
    mode_index = histogram.argmax()
    noise_mode = noise_bins[mode_index]
    noise_median = np.median(values)
    return noise_mode, noise_median


def noise_values_per_tissue(noise_map, hu_image, hounsfield_range):
    # Returns all noise values in the noise map that correspond to pixels of the same tissue
    lower_hu, upper_hu = hounsfield_range
    tissue_noise = np.extract((hu_image < upper_hu) & (lower_hu <= hu_image), noise_map)
    tissue_noise = tissue_noise[~np.isnan(tissue_noise)]
    return tissue_noise


def tissue_noise_map(noise_map, hu_image, tissue='soft', hounsfield_range=None):
    # Create a noise map for the pixels that coincide with a certain tissue
    if not hounsfield_range:
        hounsfield_range = tissue_hounsfield_units[tissue]
    lower_hu, upper_hu = hounsfield_range
    tissue_noise = np.where((hu_image < upper_hu) & (lower_hu <= hu_image), noise_map, np.nan)
    return np.where(np.isnan(hu_image), np.nan, tissue_noise)


def global_noise_2d(image, kernel_size=samei_kernel, tissue='soft', hounsfield_range=None):
    noise_map = construct_noise_map(image, mask_size=kernel_size)
    if not hounsfield_range:
        hounsfield_range = tissue_hounsfield_units[tissue]
    noise_values = noise_values_per_tissue(noise_map, image, hounsfield_range)
    try:
        gnl_mode, gnl_median = histogram_mode(noise_values)
    except ValueError:
        gnl_mode, gnl_median = None, None
    return gnl_mode, gnl_median


def global_noise_from_noise_map(image, noise_map, hounsfield_range):
    noise_values = noise_values_per_tissue(noise_map, image, hounsfield_range)
    try:
        gnl_mode, gnl_median = histogram_mode(noise_values)
    except ValueError:
        gnl_mode, gnl_median = None, None
    return gnl_mode, gnl_median
