import click
from printer import RecieptPrinter
from resize_images import resize_all_images


@click.command()
@click.argument("images_dir")
@click.option("--width", default=400)
def print_and_resize(images_dir: str, width: int) -> None:
    resize_all_images(images_dir, width)
    printer = RecieptPrinter()
    printer.print_images(images_dir)

if __name__ == "__main__":
    print_and_resize()