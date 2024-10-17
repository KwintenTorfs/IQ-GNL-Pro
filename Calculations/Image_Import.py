import os
import numpy as np
import pydicom
from pydicom.multival import MultiValue
from pydicom.errors import InvalidDicomError
from skimage.morphology import binary_erosion
from scipy import ndimage


# According to Ahmad (2021) -> take soft tissue upper to be 170, not 100 HU
# Upper bound of lung tissue is taken as -600 =>
#     https://books.google.be/books?id=IJwZHPrDQYUC&pg=PA379&redir_esc=y#v=onepage&q&f=false
tissue_hounsfield_units = {'soft': [0, 170], 'bone': [300, np.infty], 'fat': [-300, 0], 'lung': [-np.infty, -600],
                           'soft_qaelum': [-300, 300]}
# Threshold list as used in the original Resolution paper by Sanders
sanders_threshold_list = [-475, -400, -200, -190, -175, -165, -155, -150]
# Anam (2017) Truncation correction Factor - TP is not in % but from 0-1
anam_truncation_correction = 1.15
# I did a small-scale study on the effect of thresholds for masking.
# SEE: C:\Users\ktorfs5\KU Leuven\PhD\Projects\Patient Image Quality\Minor\Speed up Masking\Small Project - Body Masking
# From there, I concluded to use only -400 HU and -200 HU as thresholds
kwinten_threshold_list = [-400, -200]


def radial_distance_xy(vector1, vector2):
    # Calculates distance on xy plane between two vectors in 3D
    z1, y1, x1 = vector1
    z2, y2, x2 = vector2
    return np.sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2)


def conversion_factor(dw, phantom):
    a, b = ssde_coefficients[phantom]
    return a * np.exp(-b * dw)


def process_kernel(kernel):
    # This method deals with iterative kernels that are given as lists e.g; ['Br40', '3']
    #       and returns one single 'Br40-3'. We use a dash '-' as seperator
    separator = '-'
    if isinstance(kernel, MultiValue):
        kernel = separator.join(list(kernel))
    return kernel


def remove_truncation(image):
    image = image.astype(float)
    dimensions = image.shape
    radius_circle = dimensions[0] / 2
    corner_size = np.floor(0.75 * radius_circle * (1 - 1 / np.sqrt(2)))
    radius_corner = int(np.floor((corner_size - 1) / 2))
    corner_x_max, corner_y_max = dimensions[0] - radius_corner - 1, dimensions[1] - radius_corner - 1
    image_minimum = np.nanmin(image)
    corner_truncated = []
    for corner_mask_center_x in [radius_corner, corner_x_max]:
        for corner_mask_center_y in [radius_corner, corner_y_max]:
            corner = image[corner_mask_center_x - radius_corner:corner_mask_center_x + radius_corner + 1,
                           corner_mask_center_y - radius_corner:corner_mask_center_y + radius_corner + 1]
            corner_max = np.nanmax(corner)
            corner_truncated.append(corner_max == image_minimum)
    circular_truncation = all(corner_truncated)
    if circular_truncation:
        positions = np.arange(-radius_circle + 0.5, radius_circle, 1)
        nx, ny = np.meshgrid(positions, positions)
        distance_to_center = np.sqrt(nx ** 2 + ny ** 2)
        outside_truncation = distance_to_center > radius_circle
        image[outside_truncation] = np.nan
    return image


def body_segmentation(image, threshold_list):
    # Step 1: the image (in HU) is processed with multiple thresholds (in HU). Pixels that
    #       pass all thresholds will have value = No. thresholds
    threshold_image = np.zeros(image.shape, dtype=np.uint8)
    for threshold in threshold_list:
        threshold_image += np.array(ndimage.binary_fill_holes(image > threshold))
    nb_thresholds = len(threshold_list)
    # If pixel passes all thresholds, it is part of the binary image
    binary_image = np.array(threshold_image == nb_thresholds, dtype=np.uint8)
    # Next each pixel is numbered: background = 0, structure 1 = 1, structure 2 = 2, ...
    labels, label_nb = ndimage.label(binary_image)
    # Then count the amount of pixels per structure. Don't include background
    label_count = np.bincount(labels.ravel().astype(int))
    label_count[0] = 0
    # Body segmentation will assume that largest structure is body and thus use it for mask
    mask = np.array(labels == label_count.argmax(), dtype=np.uint8)
    mask = np.multiply(mask, 1, dtype=np.uint8)
    segment = mask.astype(np.float32)
    segment[segment == 0] = np.nan
    body = np.array(image * segment, dtype=np.float32)
    return mask, body


def tissue_fractions(image):
    # This function will calculate the fractions of different tissues in an image
    total_pixels = len(image[np.logical_not(np.isnan(image))])
    hu_soft = tissue_hounsfield_units['soft']
    hu_fat = tissue_hounsfield_units['fat']
    hu_bone = tissue_hounsfield_units['bone']
    hu_lung = tissue_hounsfield_units['lung']
    soft = len(image[np.logical_and(hu_soft[1] > image, image >= hu_soft[0])]) / total_pixels
    fat = len(image[np.logical_and(hu_fat[1] > image, image >= hu_fat[0])]) / total_pixels
    bone = len(image[np.logical_and(hu_bone[1] > image, image >= hu_bone[0])]) / total_pixels
    lung = len(image[np.logical_and(hu_lung[1] > image, image >= hu_lung[0])]) / total_pixels
    return lung, fat, soft, bone


def normalize_image(image, center, width):
    img_min = center - width // 2
    img_max = center + width // 2
    window_image = image.copy()
    window_image[window_image < img_min] = img_min
    window_image[window_image > img_max] = img_max
    return window_image


def fraction_truncation(image, mask):
    contour = mask.copy()
    fov_contour = np.logical_not(np.isnan(image))
    fov_erosion = binary_erosion(fov_contour)
    except_edges_fov = np.logical_xor(fov_contour, fov_erosion)
    fov_contour[1:-1, 1:-1] = except_edges_fov[1:-1, 1:-1]
    erosion = binary_erosion(mask)
    except_edges = np.logical_xor(mask, erosion)
    contour[1:-1, 1:-1] = except_edges[1:-1, 1:-1]

    truncated_pixels = np.logical_and(fov_contour, contour).sum()
    non_truncated_pixels = contour.sum() - truncated_pixels

    truncated_length = truncated_pixels - 1
    non_truncated_length = non_truncated_pixels - 1

    truncated_fraction = truncated_length / (non_truncated_length + truncated_length)
    return truncated_fraction, contour, fov_contour


def wed_truncation_correction(wed, truncation_percentage, scaling_parameter=anam_truncation_correction):
    truncation_correction = np.exp(scaling_parameter * truncation_percentage ** 3)
    corrected_wed = truncation_correction * wed
    return corrected_wed, truncation_correction


# Coefficients to calculate the f conversion factor for the SSDE as seen in AAPM report in 2014
ssde_coefficients = {'Body': [3.704369, 0.03671937], 'Head': [1.874799, 0.03871313]}

class Image:
    minimum_value = -1800

    def __init__(self, directory, file, process=True, thresholds=None):

        self.AcquisitionType = None
        self.BodyPart = None
        self.COLLECTION_CENTER = None
        self.COLLECTION_DIAMETER = None
        self.Columns = None
        self.CTDI_vol = None
        self.ExposureModulationType = None
        self.ExposureTime = None
        self.FilterType = None,
        self.FIRST_PIXEL = None
        self.InStackPositionNumber = None
        self.ImageComments = None
        self.MATRIX_CENTER = None
        self.OFF_CENTER = None
        self.OffsetHorizontal = None
        self.OffsetVertical = None
        self.OffsetRadial = None
        self.ORIENTATION = None
        self.PatientAge = None
        self.PATIENT_CENTER = None
        self.PatientID = None
        self.PatientSex = None
        self.Pitch = None
        self.PixelSize = None
        self.Procedure = None
        self.Protocol = None
        self.RECONSTRUCTION_CENTER = None
        self.RECONSTRUCTION_DIAMETER = None
        self.Rows = None
        self.RevolutionTime = None
        self.SeriesDescription = None
        self.SliceNumber = None
        self.SliceThickness = None
        self.SoftwareVersion = None
        self.SSDE = None
        self.StudyComments = None
        self.StudyDescription = None
        self.StudyDate = None
        self.Study_ID = None
        self.WED = None
        self.WED_correction_factor = None
        self.WED_uncorrected = None

        self.area = None
        self.array = None
        self.average_hu = None
        self.body = None
        self.body_contour = None
        self.channels = None
        self.collection_center = None
        self.collection_diameter = None
        self.ctdi_phantom = 'Body'
        self.dicom = None
        self.dimensions = None
        self.dx = None
        self.dy = None
        self.f = None
        self.first_pixel = None
        self.fov_contour = None
        self.intercept = None
        self.kernel = None
        self.kVp = None
        self.mA = None
        self.mAs = np.nan
        self.manufacturer = None
        self.mask = None
        self.matrix_center = None
        self.matrix_coordinate_to_real = None
        self.matrix_real_to_coordinate = None
        self.model = None
        self.patient_center = None
        self.raw_hu = None
        self.reconstruction_center = None
        self.reconstruction_diameter = None
        self.singleCollimation = None
        self.slice_location = None
        self.slope = None
        self.station = None
        self.totalCollimation = None
        self.truncated_fraction = None

        if thresholds is None:
            thresholds = kwinten_threshold_list
        self.thresholds = thresholds
        self.file = file
        self.path = os.path.join(directory, file)
        self.filename = os.path.basename(self.path)
        self.folder = os.path.basename(directory)
        self.valid = True

        if self.valid:
            self._get_dicom_file()
            if process:
                self.set_basic_dicom_info()
                self.set_array()
                self.mask_and_body_segmentation()
                self.calculate_ssde()
                self.calculate_contours_and_off_center()

    def _transform_to_hu(self, array):
        return array * self.slope + self.intercept

    def _get_dicom_file(self):
        if self.valid:
            try:
                self.dicom = pydicom.dcmread(self.path)
            except (AttributeError, InvalidDicomError, PermissionError):
                self.valid = False

    def set_basic_dicom_info(self):
        if self.valid:
            try:
                self.kVp = int(np.round(self.dicom.KVP, 0))
            except (AttributeError, TypeError):
                self.kVp = None
            try:
                self.PixelSize = self.dicom.PixelSpacing[0]
            except AttributeError:
                self.PixelSize = None
            try:
                self.SliceThickness = self.dicom.SliceThickness
            except AttributeError:
                self.SliceThickness = None
            try:
                self.mAs = int(np.round(self.dicom.Exposure, 0))
            except (AttributeError, TypeError):
                self.mAs = np.nan
            try:
                self.Pitch = self.dicom.SpiralPitchFactor
            except (AttributeError, TypeError):
                self.Pitch = None
            try:
                self.kernel = process_kernel(self.dicom.ConvolutionKernel)
            except AttributeError:
                self.kernel = None
            try:
                self.CTDI_vol = np.round(self.dicom.CTDIvol, 2)
            except (AttributeError, TypeError):
                self.CTDI_vol = np.nan
            try:
                self.manufacturer = self.dicom.Manufacturer
            except AttributeError:
                self.manufacturer = None
            try:
                self.model = self.dicom.ManufacturerModelName
            except AttributeError:
                self.model = None
            try:
                self.SliceNumber = int(self.dicom.InstanceNumber)
            except (AttributeError, TypeError):
                self.SliceNumber = None
            try:
                self.Rows = int(self.dicom.Rows)
            except (AttributeError, TypeError):
                self.Rows = None
            try:
                self.Columns = int(self.dicom.Columns)
            except (AttributeError, TypeError):
                self.Columns = None
            try:
                self.SeriesDescription = self.dicom.SeriesDescription
            except AttributeError:
                self.SeriesDescription = None
            try:
                self.COLLECTION_DIAMETER = self.dicom.COLLECTION_DIAMETER
            except AttributeError:
                self.COLLECTION_DIAMETER = None
            try:
                self.ExposureTime = self.dicom.ExposureTime
            except AttributeError:
                self.ExposureTime = None
            try:
                self.singleCollimation = self.dicom.SingleCollimationWidth
            except AttributeError:
                self.singleCollimation = None
            try:
                self.station = self.dicom.StationName
            except AttributeError:
                self.station = None
            try:
                self.mA = int(np.round(self.dicom.XRayTubeCurrent, 0))
            except (AttributeError, TypeError):
                self.mA = np.nan
            try:
                self.totalCollimation = self.dicom.TotalCollimationWidth
            except AttributeError:
                self.totalCollimation = None
            try:
                self.channels = int(np.round(self.totalCollimation / self.singleCollimation, 0))
            except (AttributeError, TypeError):
                self.channels = None
            try:
                self.slice_location = self.dicom.SliceLocation
            except AttributeError:
                self.slice_location = None
            try:
                self.StudyDate = self.dicom.StudyDate
            except AttributeError:
                self.StudyDate = None
            try:
                self.SoftwareVersion = self.dicom.SoftwareVersions
            except AttributeError:
                self.SoftwareVersion = None
            try:
                self.Protocol = self.dicom.ProtocolName
            except AttributeError:
                self.Protocol = None
            try:
                self.PatientSex = self.dicom.PatientSex
            except AttributeError:
                self.PatientSex = None
            try:
                self.PatientAge = self.dicom.PatientAge
            except AttributeError:
                self.PatientAge = None
            try:
                self.PatientID = self.dicom.PatientID
            except AttributeError:
                self.PatientID = None
            try:
                self.BodyPart = self.dicom.BodyPartExamined
            except AttributeError:
                self.BodyPart = None
            try:
                self.Procedure = self.dicom.RequestedProcedureDescription
            except AttributeError:
                self.Procedure = None
            try:
                self.Study_ID = self.dicom.AccessionNumber
            except AttributeError:
                self.Study_ID = None
            try:
                self.COLLECTION_CENTER = np.array(self.dicom.DataCollectionCenterPatient)
            except AttributeError:
                self.COLLECTION_CENTER = None
            try:
                self.RECONSTRUCTION_CENTER = np.array(self.dicom.ReconstructionTargetCenterPatient)
            except AttributeError:
                self.RECONSTRUCTION_CENTER = None
            try:
                self.AcquisitionType = self.dicom.AcquisitionType
            except AttributeError:
                self.AcquisitionType = None
            try:
                self.ExposureModulationType = self.dicom.ExposureModulationType
            except AttributeError:
                self.ExposureModulationType = None
            try:
                self.FilterType = self.dicom.FilterType
            except AttributeError:
                self.FilterType = None
            try:
                self.InStackPositionNumber = self.dicom.InStackPositionNumber
            except AttributeError:
                self.InStackPositionNumber = None
            try:
                self.RevolutionTime = self.dicom.RevolutionTime
            except AttributeError:
                self.RevolutionTime = None
            try:
                self.StudyComments = self.dicom.StudyComments
            except AttributeError:
                self.StudyComments = None
            try:
                self.StudyDescription = self.dicom.StudyDescription
            except AttributeError:
                self.StudyDescription = None
            try:
                self.ImageComments = self.dicom.ImageComments
            except AttributeError:
                self.ImageComments = None
            try:
                ctdi_phantom_code = self.dicom.CTDIPhantomTypeCodeSequence[0].CodeValue
            except AttributeError:
                ctdi_phantom_code = None
            if ctdi_phantom_code == 113691:
                self.ctdi_phantom = 'Body'
            elif ctdi_phantom_code == 113690:
                self.ctdi_phantom = 'Head'
            else:
                self.ctdi_phantom = 'Body'
            try:
                self.dimensions = np.array(self.dicom.PixelSpacing)
                self.dy, self.dx = np.multiply(self.raw_hu.shape, self.dimensions)
            except (AttributeError, IndexError, TypeError):
                pass


    def set_array(self):
        if self.valid:
            try:
                self.array = self.dicom.pixel_array.astype(float)
                try:
                    if self.ImageComments != 'MASK IMAGE':
                        self.array = remove_truncation(self.array)
                except AttributeError:
                    self.array = remove_truncation(self.array)
                self.slope = self.dicom.RescaleSlope
                self.intercept = self.dicom.RescaleIntercept
                self.raw_hu = self._transform_to_hu(self.array)
                self.raw_hu[self.raw_hu < self.minimum_value] = np.nan
            except (AttributeError, InvalidDicomError, PermissionError):
                self.valid = False

    def mask_and_body_segmentation(self):
        if self.valid and self.ImageComments != 'MASK IMAGE':
            try:
                self.mask, self.body = body_segmentation(self.raw_hu, self.thresholds)
            except (AttributeError, PermissionError):
                self.valid = None
            try:
                self.area = np.sum(self.mask) * (self.PixelSize / 10) ** 2  # Cross-sectional area of patient in cm²
            except (AttributeError, TypeError):
                self.area = np.nan
        elif self.valid and self.ImageComments == 'MASK IMAGE':
            self.mask = self.raw_hu

    def calculate_ssde(self):
        try:
            self.average_hu = np.nanmean(self.body)
        except (AttributeError, TypeError):
            self.average_hu = np.nan
        try:
            self.WED_uncorrected = 2 * np.sqrt((1 + self.average_hu / 1000) * self.area / np.pi)  # water equivalent
            # diameter in cm
        except (AttributeError, TypeError):
            self.WED_uncorrected = np.nan
        try:
            self.truncated_fraction, self.body_contour, self.fov_contour = fraction_truncation(self.raw_hu, self.mask)
        except (AttributeError, TypeError):
            self.truncated_fraction, self.body_contour, self.fov_contour = np.nan, np.nan, np.nan
        try:
            self.WED, self.WED_correction_factor = \
                wed_truncation_correction(self.WED_uncorrected, self.truncated_fraction)
        except (AttributeError, TypeError):
            self.WED, self.WED_correction_factor = self.WED_uncorrected, np.nan
        try:
            self.f = conversion_factor(self.WED, self.ctdi_phantom)  # ssde conversion factor in cm-1
            self.SSDE = self.f * self.CTDI_vol
        except (AttributeError, TypeError, KeyError):
            self.f, self.SSDE = np.nan, np.nan

    def calculate_contours_and_off_center(self):
        # PATIENT ORIENTATION AND LOCATION
        try:
            self.FIRST_PIXEL = np.array(self.dicom.ImagePositionPatient[:-1], dtype=float)
        except AttributeError:
            self.FIRST_PIXEL = None
        try:
            self.ORIENTATION = self.dicom.ImageOrientationPatient
            x_x, x_y, x_z, y_x, y_y, y_z = self.ORIENTATION
            px, py = self.dicom.PixelSpacing
            self.matrix_coordinate_to_real = np.array([[x_x * px, y_x * py], [x_y * px, y_y * py]])
        except (TypeError, AttributeError, ValueError):
            self.ORIENTATION, self.matrix_coordinate_to_real = None, None
        try:
            self.matrix_real_to_coordinate = np.linalg.inv(self.matrix_coordinate_to_real)
        except (TypeError, AttributeError, ValueError):
            self.matrix_real_to_coordinate = None

        # REAL SPACE COORDINATES
        try:
            self.COLLECTION_DIAMETER = self.dicom.DataCollectionDiameter
        except AttributeError:
            self.COLLECTION_DIAMETER = None
        try:
            self.RECONSTRUCTION_DIAMETER = self.dicom.ReconstructionDiameter
        except AttributeError:
            self.RECONSTRUCTION_DIAMETER = None
        try:
            self.COLLECTION_CENTER = np.array(self.dicom.DataCollectionCenterPatient)[:-1]
        except AttributeError:
            self.COLLECTION_CENTER = None
        try:
            self.RECONSTRUCTION_CENTER = np.array(self.dicom.ReconstructionTargetCenterPatient)[:-1]
        except AttributeError:
            self.RECONSTRUCTION_CENTER = None

        # MATRIX PIXEL COORDINATES
        self.first_pixel = np.array([0, 0])
        self.reconstruction_diameter = np.max(self.array.shape)
        self.matrix_center = np.flip((np.array(self.array.shape) - 1) // 2)
        try:
            self.MATRIX_CENTER = self.coordinate_to_real_space(self.matrix_center)
        except (TypeError, ValueError, AttributeError):
            self.MATRIX_CENTER = None
        try:
            self.reconstruction_center = self.real_to_coordinate_space(self.RECONSTRUCTION_CENTER)
        except (TypeError, ValueError, AttributeError):
            self.reconstruction_center = None
        try:
            self.collection_diameter = self.COLLECTION_DIAMETER / self.PixelSize
        except (TypeError, ValueError, AttributeError):
            self.collection_diameter = None
        try:
            self.collection_center = self.real_to_coordinate_space(self.COLLECTION_CENTER)
        except (TypeError, ValueError, AttributeError):
            self.collection_center = None

        try:
            self.patient_center = np.flip(np.argwhere(self.mask == 1).sum(0) / (self.mask == 1).sum())
        except (AttributeError, ValueError, TypeError):
            self.patient_center = None
        try:
            self.PATIENT_CENTER = self.coordinate_to_real_space(self.patient_center)
        except (TypeError, ValueError, AttributeError):
            self.PATIENT_CENTER = None

        try:
            self.OFF_CENTER = self.PATIENT_CENTER - self.COLLECTION_CENTER
            self.OffsetHorizontal, self.OffsetVertical = self.OFF_CENTER
            self.OffsetRadial = np.sqrt(np.sum(self.OFF_CENTER ** 2))
        except (AttributeError, ValueError, TypeError):
            self.OFF_CENTER, self.OffsetHorizontal, self.OffsetVertical, self.OffsetRadial = np.nan, np.nan, np.nan, np.nan

    def coordinate_to_real_space(self, coordinate):
        return np.matmul(self.matrix_coordinate_to_real, coordinate) + self.FIRST_PIXEL

    def real_to_coordinate_space(self, point):
        return np.matmul(self.matrix_real_to_coordinate, point - self.FIRST_PIXEL)

    def set_slice_number(self, new_slice_number):
        self.SliceNumber = new_slice_number

    def get_tissue_measurements(self, tissue_hu):
        image = self.body
        tissue_area = len(image[np.logical_and(tissue_hu[1] > image, image >= tissue_hu[0])]) * \
                         (self.PixelSize / 10) ** 2  # in cm²
        tissue_percentage = tissue_area / self.area
        return tissue_area, tissue_percentage