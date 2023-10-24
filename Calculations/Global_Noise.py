import numpy as np
from Calculations.Image_Import import tissue_hounsfield_units


# Also according to Samei2020, bin width should be 1 HU
samei_bin_width = 1
# Also according to Samei2020, kernel size should be 7 x 7
samei_kernel = 7


def extend_matrix_2d(matrix, radius):
    # For any convolution calculation, the matrix needs to be extended to allow convolution in the image borders
    #   Radius is the radius of the mask array (e.g. for 3x3, radius = 1)
    [dy, dx] = matrix.shape
    extended_image = np.zeros([dy + 2 * radius, dx + 2 * radius])

    # Center ofr the extended image is the current image
    extended_image[radius:dy + radius, radius:dx + radius] = matrix

    # Each corner is extended as the current corner pixel
    extended_image[0:radius, 0:radius] = matrix[0, 0]
    extended_image[radius + dy:, 0:radius] = matrix[dy - 1, 0]
    extended_image[0:radius, radius + dx:] = matrix[0, dx - 1]
    extended_image[radius + dy:, radius + dx:] = matrix[dy - 1, dx - 1]

    # The borders are extended outwards with the corresponding values of
    for i in range(radius):
        extended_image[radius:radius + dy, i] = matrix[0:dy, 0]
        extended_image[i, radius:radius + dx] = matrix[0, 0:dx]
        extended_image[radius:radius + dy, i + radius + dx] = matrix[0:dy, dx - 1]
        extended_image[i + radius + dy, radius:radius + dx] = matrix[dy - 1, 0:dx]
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

####
#
#  GNL Correction for Slice Thickness   SD ~ 1 / sqrt(ST)
#
#  Use Correction to normalise GNL
#
###
