from ctypes import (
    c_char_p,
)

from thorlabs_kinesis import Polarizer as pmc
from thorlabs_kinesis.ext import expand_device

if __name__ == "__main__":
    if pmc.TLI_BuildDeviceList() == 0:
        num_devs = int(pmc.TLI_GetDeviceListSize())
        print(f"There are {num_devs} devices.")