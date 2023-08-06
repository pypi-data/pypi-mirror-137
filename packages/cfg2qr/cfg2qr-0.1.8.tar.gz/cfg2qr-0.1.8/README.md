# Configure to QR-code 

## Description

This is a personal demo to get familiar with  python structuring and packaging. 

Specify a config file in json or yaml format and a QR code will be generated using existing  PyPI library. 

Specify an existing QR code image and the output file name (json or yaml) and the config file will be generated using existing PyPI library.


### Generating QR code from config file

* --input_directory: specify input directory 
* encoder 
* -input_text_name : 
specify the config file name (with file format)
* -result_text_name : specify the output image file name (with file format). The resulting config file will be saved in the same directory as the input


## Generating config file from QR code

* --input_directory: specify input directory 
* decoder 
* -input_image_name : specify the input image file name (with file format)
* -result_text_name :specify the output config file name. The resulting config file will be saved in the same directory as the input
