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
    return image.DataCollectionDiameter


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
    return image.ReconstructionDiameter


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
                'Body Area (cm²)': area
                }
