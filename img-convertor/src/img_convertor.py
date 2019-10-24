import os
import time
import json
from PIL import Image
import PIL.Image

# To handle pil.image.decompression bomb error image size exceeds limit
PIL.Image.MAX_IMAGE_PIXELS = None

start_time = time.time()

number_of_files_processed = 0
number_of_exceptions = 0

script_dir = os.path.dirname(__file__)
configuration = json.load(open(os.path.join(script_dir, 'config.json'),"r"))
dir_location = configuration["dir_location"]
img_extensions = configuration["from_extension"]
to_img_extension = configuration["to_img_extension"]

def get_file_extension(file_name):
    if len(file_name.split(os.extsep,1)) < 2:
        return None
    else:
        return file_name.split(os.extsep,1)[-1]

def get_out_file_name(file_name):
    name = file_name.split(os.extsep, 1)[0]
    return name


def start_image_conversion(root, file, to_ext):
    path = os.path.join(root, file)
    im = Image.open(path)
    out = im.convert("RGB")
    out_file = get_out_file_name(file) + "." + to_ext
    out.save(os.path.join(root, out_file), to_ext, quality=100)
    return out_file

def resize_file(root, file, size):
    path = os.path.join(root, file)
    im = Image.open(path)
    img_size = size, size
    file_ext = get_file_extension(file)
    im_resized = im.resize(img_size, Image.ANTIALIAS)
    im_resized.save(os.path.join(root, get_out_file_name(file) + "_" + str(size) + "." + file_ext), file_ext)


def main():
    global number_of_files_processed, number_of_exceptions

    for input in dir_location:
        for root, dirs, files in os.walk(input["path"], topdown=True):
            for file in files:
                file_extension = get_file_extension(file)
                if file_extension in img_extensions:
                    try:
                        out_file = start_image_conversion(root, file, to_img_extension)
                        resize_file(root, out_file, 500)
                        number_of_files_processed = number_of_files_processed + 1
                    except Exception as e:
                        number_of_exceptions = number_of_exceptions + 1
                        print(str(e))

        print("Processed the dir - " + input["path"])


print("Starting the img_convertor service!")
main()
print("Number of IMAGES processed - " + str (number_of_files_processed))
print("Number of exceptions occurred - " + str(number_of_exceptions))
print("Total time took for the execution - "+ str((time.time() - start_time)/60) + " minutes")