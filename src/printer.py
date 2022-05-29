import os
import time
import re
from typing import Tuple
import click
from escpos.printer import Usb
import subprocess


@click.command()
@click.argument("images_dir")
def connect_and_print_all(images_dir: str) -> None:
    printer = RecieptPrinter()
    printer.print_images(images_dir)

class RecieptPrinter():
    def __init__(self, vendor_id: hex = "", product_id: hex = "", iinterface: int = 1):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.iinterface = iinterface
        if not vendor_id or not product_id:
            self.connect_printer()
            pass
                    
    def connect_printer(self) -> None:
        """ Connect to a usb printer automatically by inserting it into your computer. """
        
        print("Start with your printer disconnected, then connect and turn it on.")
        
        usb_devices = None
        
        #  Find vendor id, product id and iinterface from lsusb
        while True:
            process = subprocess.Popen("lsusb", stdout=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                print(error)
                print("Failed to run lsusb. Try running with sudo.")
                exit()
                
            usb_devices_latest = str(output).split("\\n")    
            
            #  If a new device has been connect attempt extract details
            if usb_devices != None and len(usb_devices_latest) > len(usb_devices):
                new_device = (set(usb_devices_latest) - set(usb_devices)).pop()
                self.vendor_id, self.product_id = self.parse_ids(new_device)
                break  
            
            time.sleep(0.5)
            usb_devices = usb_devices_latest
        
            
    def parse_ids(self, lsusb_text: str) -> Tuple[int, int]:
        id = re.findall("...[0-9a-f]:[0-9a-f]...", lsusb_text, flags=re.IGNORECASE)[0]
        return id.split(":") 
        
    def print_images(self, images_dir: str, cut_between_images: bool) -> None:    
        p = Usb(int(self.vendor_id, 16), int(self.product_id, 16))
        
        for path in sorted(os.listdir(images_dir)): 
            p.image(images_dir + "/" + path)
            
            if cut_between_images:
                p.cut()
        
        p.cut()
        


if __name__ == "__main__":
    connect_and_print_all()
    