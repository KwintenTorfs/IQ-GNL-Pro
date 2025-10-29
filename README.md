>[!IMPORTANT] 
> The contents of this tool remain under construction, so changes will keep getting committed

This repository contains the code to calculate global noise level and was used in the manuscript: _Insights, robustness and practical considerations of global noise level measurement in chest CT_ (doi: ). When using this toolbox in your work, please refer to this paper.

# IQ GNL Pro <img src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/LOGO%20Black.png" width=5% height=5% align='right'>

This toolbox allows to automatically assess image quality in phantom and patient CT images by calculating global noise level (GNL). Besides GNL, it is possible to use this tool to retrieve information available in the CT image .dicom header, or other calculated properties, e.g. _water-equivalent diameter_ WED, amount of image truncation, patient positioning offset,... \
The tool was developed by the _Medical Physics and Quality Assessment_ group of the KU Leuven. Funding was procured through a FWO Fellowship by _Kom op Tegen Kanker_ (reference number: G0B1922N).

It can be accessed publicly from [Github](https://github.com/KwintenTorfs/IQ-GNL-Pro) or [Gitlab](https://gitlab.kuleuven.be/medphysqa/deploy/iq-gnl-pro)

Development: [Kwinten Torfs](https://www.kuleuven.be/wieiswie/nl/person/00148621)

Supervision: [D. Petrov](https://www.kuleuven.be/wieiswie/nl/person/00101698), [H. Bosmans](https://www.kuleuven.be/wieiswie/nl/person/00009754)

<p align="center"> <image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/KOTK.png" height=40 title='Kom op Tegen Kanker' align='left'> <image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/KUL.png" height=40 title='KU Leuven'> <image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/UZ Leuven.png" height=40 title='KU Leuven' align='right'>

## Theoretical background

Global noise level **GNL** is a measure representing the amount of quantum noise within a single CT slice. The initial development of the metric can be traced back to work of [_Christianson et al._ (2015)](https://www.ajronline.org/doi/10.2214/AJR.14.13613). \
The calculation of GNL consists of three steps:

1. Identification of a _target tissue_ where GNL will be measured. The tissue is selected based on the Hounsfield Units of the material. Most important are soft tissue (0-170 HU) and lung/air tissue (<-600 HU).
2. Measurement of _local noise_ around each pixel, defined as the standard deviation in a specified region around that pixel. These values are then collected into a local noise map
3. Local noise values of the target tissue pixels are gathered in a local noise histogram of which the mode (most occurring value) is defined to be the _GNL_
<p align="center">
<image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/GNL%20Calculation.png" height=400 align='center' title="GNL calculation slide, presented at ECR 2025">

>[!IMPORTANT]
>Information about GNL calculation and choices made, will be expanded in the future

## Use of the tool

###  Title Screen
<p align="center">
<image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/Screen%20Initial.png" height=400 title="Title screen">

### Selection Menus
The selection menus are used to alter the default settings of the GNL calculation, determine which images will be measured and which measurements will be exported.

#### Folders
The _Folders_ menu is used to select data on which GNL is measured, which can be selected using the _Browse_ and afterwards _Add file_ buttons. The possible formats are:
1. **Individual CT slices** -> GNL is measured on each CT slice and results returned as such
2. **Stacks of CT slices** -> CT scans are inherently three dimensional and consist of multiple slices. With this option a folder of CT slices will be measured and results are returned both for all individually measured slices and as averages for each folder of CT slices
3. **Database of CT stacks** -> For processing of an entire map of CT stacks, use the database option

After addition of a new image/folder, the tool will ask if other images/folders on the same level as the selected source should be added as well.

#### GNL Settings
The _GNL Settings_ menu allows the user to alter the possible tissues in which to measure GNL. Default settings for soft, bone, fat and lung tissue are given. Newly added tissues will be stored for the user and can always be removed later on

#### Measurement
In the _Measurement_ menu, the user can select how GNL is reported. There is the option to _Measure per slice_ and then return the GNL measurements of the selected slices, or to _Measure per scan_ and on top of the slices also return averages over folders of images. For the _individual CT slices_ option in the _Folders_ menu, it is only possible to measure per slice.

The user can also determine in which slices of a folder to measure
- All slices
- 10 equidistant slices (= 10 CT slices of a folder, equally distributed along the scan-axis)
- x equidistant slices
- Mid axial slice (= middle slice along the scan-axis)

  #### Export
  The _Export_ menu allows to select which parameters and measurements are reported

  #### Save
  In the _Save_ menu, it is determined where to store the exported measurements and in which file type to do so.


### Calculate
After initialising the settings, measurements are started using this button


### Installed packages
Necessary packages can be installed through the _requirements.txt_ folder


>[!WARNING]
>This public repository is still in it's early development. Problems with implementation into your own work setting may occur.



