# IQ GNL PRO <img src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/LOGO%20Black.png" width=5% height=5% align='right'>

This program allows to automatically assess image quality in phantom and patient CT images by calculating global noise level (GNL). The tool was developed by the _Medical Physics and Quality Assessment_ group of the KU Leuven. Funding was procured through a FWO Fellowship by _Kom op Tegen Kanker_.


Development: [Kwinten Torfs](https://www.kuleuven.be/wieiswie/nl/person/00148621)

Supervision: [D. Petrov](https://www.kuleuven.be/wieiswie/nl/person/00101698), [H. Bosmans](https://www.kuleuven.be/wieiswie/nl/person/00009754)

<p align="center"> <image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/KOTK.png" height=40 title='Kom op Tegen Kanker' align='left'> <image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/KUL.png" height=40 title='KU Leuven'> <image src="https://github.com/KwintenTorfs/GNL_GUI/blob/master/assets/UZ Leuven.png" height=40 title='KU Leuven' align='right'>

## Theoretical background

Global noise level **GNL** is a measure representing the amount of quantum noise within a single CT slice. The initial development of the metric can be traced back to work of [_Christianson et al._ (2015)](https://www.ajronline.org/doi/10.2214/AJR.14.13613). \
The calculation of GNL consists of three steps:

1. Identification of a _target tissue_ where GNL will be measured. The tissue is selected based on the Hounsfield Units of the material. Most important are soft tissue (0-170 HU) and lung/air tissue (<-600 HU).
2. Measurement of _local noise_ around each pixel, defined as the standard deviation in a specified region around that pixel. These values are then collected into a local noise map
3. Local noise values of the target tissue pixels are gathered in a local noise histogram of which the mode (most occurring value) is defined to be the _GNL_



>[!WARNING]
>This public repository is still in it's early development. Problems with implementation into your own work setting may occur.
