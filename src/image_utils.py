from os import listdir
from PIL import Image
import click

def resize_all_images(images_dir: str, width: int):
    # This will resize all images to fit a stardard thermal printer.
    for file in sorted(listdir(images_dir)): 
        with Image.open(images_dir + "/" + file) as image:
            if image.size[0] != 400:
                image = fit_width(image, width)
                image.save(images_dir + "/" + file)  

def fit_width(image: Image, width: int) -> Image:
    #  Resize image to fit width. 
    
    if (image.height > image.width):
        image = image.rotate(90, expand=1)

    wpercent = (width / float(image.width))
    hsize = int((float(image.height) * float(wpercent)))
    image = image.resize((width, hsize), Image.NEAREST)
    return image

def crop_fit_factor_of_recipet_width(image: Image, reciept_width: 400):
    #  Crops image width and height to be factors of the reciept width. This allows the image to be printed
    #  over multiple reciepts
    
    #  The width that needs to be removed on each side to make the image a factor of the reciept width
    extra_width = (image.width % reciept_width) / 2
    extra_height = (image.height % reciept_width) / 2
    
    image = image.crop((extra_width, extra_height, image.width - extra_width, image.height - extra_height))
    
    return image                
                
def slice_image(images_dir: str, slices: int, margin: int, receipt_width: int = 400):
    total_width = int(receipt_width + (2 * margin))

    for file in sorted(listdir(images_dir)): 
        name, extension = file.split(".")
        
        with Image.open(images_dir + "/" + file) as image:  
            image = fit_width(image, total_width * slices)
            image = crop_fit_factor_of_recipet_width(image, total_width)            
            
            horizontal_slices = image.width // total_width
            vertical_slices = image.height // total_width
            
            
            for si in range(vertical_slices):
                #  Get a vertical slice of the image
                slice = image.crop((0, total_width*si, image.width, total_width*(si + 1)))
                
                # Remove margin areas
                slice = slice.crop((margin, margin, slice.width - margin, slice.height - margin))
                
                #  Rotate so the image is printed in the correct orientation
                slice = slice.rotate(90, expand=1)
                
                slice.save(images_dir + "/" + "{}_vslice_{}".format(name, si) + "." + extension)
                
            for si in range(horizontal_slices):
                #  Get a horizontal slice of the image
                slice = image.crop((total_width*si, 0, total_width*(si + 1), image.height))
                
                #  Crop out the space where the margin is so the image fits correctly between slices
                slice = slice.crop((margin, margin, slice.width - margin, slice.height - margin))
                
                slice.save(images_dir + "/" + "{}_hslice_{}".format(name, si) + "." + extension)
                

if __name__ == "__main__":
    slice_image("output", 3, (0.4 / 5.5) * 400, 400)