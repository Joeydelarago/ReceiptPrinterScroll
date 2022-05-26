from os import listdir
from PIL import Image
import click

def resize_all_images(images_dir: str, width: int):
    # This will resize all images to fit a stardard thermal printer.
    for path in sorted(listdir(images_dir)): 
        with Image.open(images_dir + "/" + path) as image:
            if image.size[0] != 400:
                wpercent = (width / float(image.size[0]))
                hsize = int((float(image.size[1]) * float(wpercent)))
                image = image.resize((width, hsize), Image.NEAREST)
                image.save(images_dir + "/" + path)  