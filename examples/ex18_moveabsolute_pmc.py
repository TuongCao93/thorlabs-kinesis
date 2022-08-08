from ctypes import (
    c_char_p,
    byref,
    c_int,
    c_double,
    c_uint16
)

from thorlabs_kinesis import Polarizer as mpc
from thorlabs_kinesis.ext import expand_device

from time import sleep
import numpy as np

if __name__ == "__main__":
    milliseconds = c_int(100) # Polling duration

    if mpc.TLI_BuildDeviceList() == 0:
        num_devs = int(mpc.TLI_GetDeviceListSize())
        print(f"There are {num_devs} devices.")

        receive_buffer = c_char_p(bytes(" " * 250, "utf-8"))
        buffer_size = mpc.c_dword(250)
        mpc.TLI_GetDeviceListExt(receive_buffer, buffer_size)

        # Get device serial number
        serial_nos = receive_buffer.value.decode("utf-8").strip().split(',')

        # Get device description
        for i, serial_no in enumerate(serial_nos):
            if len(serial_no) > 0:
                dev = expand_device(serial_no)
                print(f"{i + 1}. {serial_no} - {dev.type}")

                serial_no_b = c_char_p(bytes(serial_no, "utf-8"))
                device_info = mpc.TLI_DeviceInfo() # container for device ifo
                mpc.TLI_GetDeviceInfo(serial_no_b, byref(device_info))
                
                print("Description: ", device_info.description)
                print("Serial No: ", device_info.serialNo)
                print("Motor Type: ", device_info.motorType)
                print("USB PID: ", device_info.PID)

                if mpc.MPC_Open(serial_no_b) == 0:
                   sleep(1.0)
                   mpc.MPC_StartPolling(serial_no_b, milliseconds)
                   mpc.MPC_ClearMessageQueue(serial_no_b)

                   sleep(1.0)
                   polarizer_params = mpc.PolarizerParameters()
                   mpc.MPC_GetPolParams(serial_no_b, byref(polarizer_params))
                   print("Velocity", polarizer_params.Velocity)
                   print("HomePosition", polarizer_params.HomePosition)
                   print("JogSize1", polarizer_params.JogSize1)
                   print("JogSize2", polarizer_params.JogSize2)
                   print("JogSize3", polarizer_params.JogSize3)

                   #step_per_deg = c_double()
                   step_per_deg =mpc.MPC_GetStepsPerDegree(serial_no_b) 
                   print("Steps per degree :", step_per_deg)
                   
                   homeoffset = c_double(0.0)
                   mpc.MPC_SetHomeOffset(serial_no_b, homeoffset)
                   homeoffset = mpc.MPC_GetHomeOffset(serial_no_b)
                   print("Home offset :", homeoffset)

                   # eanble all paddle:
                   
                   print(mpc.MPC_SetEnabledPaddles(serial_no_b, mpc.AllPaddles))
                   
                   paddles = np.array([1,2,3])

                   for idx, ipaddle in enumerate(paddles):
                       mpc.MPC_Home(serial_no_b, c_uint16(ipaddle))
                       sleep(1.0)
                       
                       position = mpc.MPC_GetPosition(serial_no_b, c_uint16(ipaddle))
                       print('Paddle %i current position is %d' %(idx+1, position))
                       
                       # move to next position
                       mpc.MPC_MoveToPosition(serial_no_b, c_uint16(ipaddle), c_double(30.0))
                       print('Padlle %i is moving' %idx)
                       sleep(1.0)

                       position = mpc.MPC_GetPosition(serial_no_b,  c_uint16(ipaddle))
                       print('Paddle %i current position is %d' %(idx+1, position))

                   mpc.MPC_StopPolling(serial_no_b)
                   mpc.MPC_Close(serial_no_b)

                else:
                    print("Can't open")
            
