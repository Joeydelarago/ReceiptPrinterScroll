import click
from printer import RecieptPrinter
from image_utils import resize_all_images, slice_image


@click.command()
@click.argument("images_dir")
@click.option("--width", default=400, help="width of printable image in pixels")
@click.option("--margin", default = 30, help="width of the margin in pixels. Can be found using a ruler: (margin mm / reciept_width mm) * reciept_width_pixels")
@click.option('--slices', '-s', is_flag=True, help="Output images as slices of the original image to print larger multi reciept images")
def print_and_resize(images_dir: str, width: int, margin:int, slices: bool, cut_between_images: bool = False) -> None:
    
    
    
    if slices:
        slice_image(images_dir, 3, margin, width)
        cut_between_images = True
    else:
        resize_all_images(images_dir, width)
        
        
    printer = RecieptPrinter()
    
    printer.print_images(images_dir, cut_between_images)

if __name__ == "__main__":
    print_and_resize()