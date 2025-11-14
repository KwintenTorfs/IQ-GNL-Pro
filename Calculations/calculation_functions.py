def procedure(image):
    return image.Procedure


def study_date(image):
    return image.StudyDate


def software_version(image):
    return image.SoftwareVersion


def protocol(image):
    return image.Protocol


def patient_sex(image):
    return image.PatientSex


def body_part(image):
    return image.BodyPart


def wed(image):
    return image.WED


def f(image):
    return image.f


def wed_correction_factor(image):
    return image.WED_correction_factor


def truncation_fraction(image):
    return image.truncated_fraction


def wed_uncorrected(image):
    return image.WED_uncorrected


def area(image):
    return image.area


def ctdi_phantom(image):
    return image.ctdi_phantom


def average_hu(image):
    return image.average_hu


def total_collimation(image):
    return image.totalCollimation


def single_collimation(image):
    return image.singleCollimation


def series_description(image):
    return image.SeriesDescription


def data_collection_diameter(image):
    return image.COLLECTION_DIAMETER


def manufacturer(image):
    return image.manufacturer


def model(image):
    return image.model


def station(image):
    return image.station


def slice_number(image):
    return image.SliceNumber


def kernel(image):
    return image.kernel


def slice_thickness(image):
    return image.SliceThickness


def channels(image):
    return image.channels


def exposure_time(image):
    return image.ExposureTime


def study_id(image):
    return image.Study_ID


def mas(image):
    return image.mAs


def ma(image):
    return image.mA


def kvp(image):
    return image.kVp


def ctdi_vol(image):
    return image.CTDI_vol


def ssde(image):
    return image.SSDE


def pitch(image):
    return image.Pitch


def pixel_size(image):
    return image.PixelSize


def slice_location(image):
    return image.slice_location


def fov(image):
    return image.RECONSTRUCTION_DIAMETER


def file(image):
    return image.file


def path(image):
    return image.path


def patient_age(image):
    return image.PatientAge


def patient_id(image):
    return image.PatientID


def matrix_size(image):
    return '%sx%s' % (image.Rows, image.Columns)


def acquisition_type(image):
    return image.AcquisitionType


def exposure_modulation_type(image):
    return image.ExposureModulationType


def filter_type(image):
    return image.FilterType


def in_stack_position_number(image):
    return image.InStackPositionNumber


def revolution_time(image):
    return image.RevolutionTime


def study_comments(image):
    return image.StudyComments


def study_description(image):
    return image.StudyDescription


def folder(image):
    return image.folder


def reconstruction_diameter(image):
    return image.RECONSTRUCTION_DIAMETER


def collection_diameter(image):
    return image.COLLECTION_DIAMETER


def offset_horizontal(image):
    return image.OffsetHorizontal


def offset_vertical(image):
    return image.OffsetVertical


def offset_radial(image):
    return image.OffsetRadial


def body_perimeter(image):
    return image.body_perimeter


calculations = {'Channels': channels,
                'Manufacturer': manufacturer,
                'Model': model,
                'Software Version': software_version,
                'Station': station,
                'Body Part Examined': body_part,
                'PACSID': study_id,
                'Patient Age (y)': patient_age,
                'Patient ID': patient_id,
                'Patient Sex': patient_sex,
                'FOV (mm)': fov,
                'Kernel': kernel,
                'kVp': kvp,
                'Pitch': pitch,
                'Pixel Size (mm)': pixel_size,
                'Procedure': procedure,
                'Protocol': protocol,
                'Slice Thickness (mm)': slice_thickness,
                'Study Date': study_date,
                'CTDI (mGy)': ctdi_vol,
                'File': file,
                'mA': ma,
                'mAs': mas,
                'Exposure Time (ms)': exposure_time,
                'Folder': folder,
                'Path': path,
                'Slice Number': slice_number,
                'SSDE (mGy)': ssde,
                'Truncation Fraction': truncation_fraction,
                'WED (cm)': wed,
                'Truncation Correction': wed_correction_factor,
                'Total Collimation (mm)': total_collimation,
                'Single Collimation (mm)': single_collimation,
                'Matrix Size': matrix_size,
                'Acquisition Type': acquisition_type,
                'Exposure Modulation Type': exposure_modulation_type,
                'Filter Type': filter_type,
                'Position in Stack': in_stack_position_number,
                'Revolution Time (s)': revolution_time,
                'Study Comments': study_comments,
                'Study Description': study_description,
                'Body Area (cm²)': area,
                'Reconstruction Diameter (mm)': reconstruction_diameter,
                'Collection Diameter (mm)': collection_diameter,
                'Offset Horizontal (mm)': offset_horizontal,
                'Offset Vertical (mm)': offset_vertical,
                'Offset Radial (mm)': offset_radial,
                'Body Perimeter (mm)': body_perimeter
                }


image_processing = {'Channels': 'BASIC',
                    'Manufacturer': 'BASIC',
                    'Model': 'BASIC',
                    'Software Version': 'BASIC',
                    'Station': 'BASIC',
                    'Body Part Examined': 'BASIC',
                    'PACSID': 'BASIC',
                    'Patient Age (y)': 'BASIC',
                    'Patient ID': 'BASIC',
                    'Patient Sex': 'BASIC',
                    'FOV (mm)': 'BASIC',
                    'Kernel': 'BASIC',
                    'kVp': 'BASIC',
                    'Pitch': 'BASIC',
                    'Pixel Size (mm)': 'BASIC',
                    'Procedure': 'BASIC',
                    'Protocol': 'BASIC',
                    'Slice Thickness (mm)': 'BASIC',
                    'Study Date': 'BASIC',
                    'CTDI (mGy)': 'BASIC',
                    'File': 'BASIC',
                    'mA': 'BASIC',
                    'mAs': 'BASIC',
                    'Exposure Time (ms)': 'BASIC',
                    'Folder': 'BASIC',
                    'Path': 'BASIC',
                    'Slice Number': 'BASIC',
                    'SSDE (mGy)': 'WED',
                    'Truncation Fraction': 'WED',
                    'WED (cm)': 'WED',
                    'Truncation Correction': 'WED',
                    'Total Collimation (mm)': 'BASIC',
                    'Single Collimation (mm)': 'BASIC',
                    'Matrix Size': 'BASIC',
                    'Acquisition Type': 'BASIC',
                    'Exposure Modulation Type': 'BASIC',
                    'Filter Type': 'BASIC',
                    'Position in Stack': 'BASIC',
                    'Revolution Time (s)': 'BASIC',
                    'Study Comments': 'BASIC',
                    'Study Description': 'BASIC',
                    'Body Area (cm²)': 'MASK',
                    'Reconstruction Diameter (mm)': 'CONTOUR',
                    'Collection Diameter (mm)': 'CONTOUR',
                    'Offset Horizontal (mm)': 'CONTOUR',
                    'Offset Vertical (mm)': 'CONTOUR',
                    'Offset Radial (mm)': 'CONTOUR',
                    'Body Perimeter (mm)': 'CONTOUR'
                    }


def basic_dicom(image):
    image.set_basic_dicom_info()


def initialise_image(image):
    image.set_array()


def set_masking(image):
    image.mask_and_body_segmentation()


def set_wed(image):
    image.calculate_ssde()


def set_contours_and_off_center(image):
    image.calculate_contours_and_off_center()


image_processing_operations = {'1 Basic dicom': basic_dicom,
                               '2 Initialize image': initialise_image,
                               '3 Masking': set_masking,
                               '4 WED': set_wed,
                               '5 Contour and Off Center': set_contours_and_off_center}
