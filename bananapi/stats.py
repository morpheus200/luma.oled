
import time
import subprocess

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep

serial = i2c(port=2, address=0x3C)
device = ssd1306(serial,width=128, height=32)


# Clear display.
device.clear()


# First define some constants to allow easy resizing of shapes.
width = 128
height = 21
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

def stats(device):
        with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="black", fill="black")
                cmd = "hostname -I | cut -d' ' -f1"
                IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
                draw.text((x, top + 0), "IP: " + IP, fill="white")
                cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
                CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
                draw.text((x, top + 8), CPU, fill="white")
                cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB %.1f%%\", $3,$2,$3*100/$2 }'"
                MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
                draw.text((x, top + 16), MemUsage, fill="white")
                cmd = 'df -h | awk \'$NF=="/media/exthdd"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
                Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
                draw.text((x, top + 25), Disk, fill="white")

def main():
        while True:
                stats(device)
                sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

