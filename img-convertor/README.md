# IMAGE convertor
    Simple python snippet to traverse a directory and convert the image files and resizing them into different sizes
    
## Configuration
* dir_location - parent directories to traverse and process image files
* from_extension - list of image file extensions to consider for conversion
* to_img_extension - the extension to which the image files will be converted

## Start
> python img_convertor.py

This service will traverse the directory and sub directories; once it founds the matching image file (those matched with the from_extension list), it will take that image file and convert it to target format and resizes it;
* The resize size has been hard coded to (500, 500) now;
