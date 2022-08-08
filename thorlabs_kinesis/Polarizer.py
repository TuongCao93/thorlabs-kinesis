"Bindings for Thorlabs Polarizer DLL MPCx20"
# flake8: noqa
from ctypes import (
    Structure,
    cdll,
    c_bool,
    c_short,
    c_int,
    c_uint,
    c_int16,
    c_int32,
    c_int64,
    c_char,
    c_byte,
    c_long,
    c_float,
    c_double,
    POINTER,
    CFUNCTYPE,
    c_ushort,
    c_uint16,
)
from thorlabs_kinesis._utils import (
    c_word,
    c_dword,
    bind
)

lib = cdll.LoadLibrary("Thorlabs.MotionControl.Polarizer.dll")

# enum FT_Status
FT_OK = c_short(0x00)
FT_InvalidHandle = c_short(0x01)
FT_DeviceNotFound = c_short(0x02)
FT_DeviceNotOpened = c_short(0x03)
FT_IOError = c_short(0x04)
FT_InsufficientResources = c_short(0x05)
FT_InvalidParameter = c_short(0x06)
FT_DeviceNotPresent = c_short(0x07)
FT_IncorrectDevice = c_short(0x08)
FT_Status = c_short

# enum MOT_MotorTypes
MOT_NotMotor = c_int(0)
MOT_DCMotor = c_int(1)
MOT_StepperMotor = c_int(2)
MOT_BrushlessMotor = c_int(3)
MOT_CustomMotor = c_int(100)
MOT_MotorTypes = c_int

#enum POL_Paddles 
paddle1 = c_uint16(1)
paddle2 = c_uint16()
paddle3 = c_uint16()
POL_Paddles = c_uint16

#enum POL_PaddleBits
NONE = c_ushort(0x00)
PaddleBit1  = c_ushort(0x01)
PaddleBit2  = c_ushort(0x02)
PaddleBit3  = c_ushort(0x03)
PaddleBit4  = c_ushort(0x04)
AllPaddles  =  c_ushort(0x07)
POL_PaddleBits = c_ushort

#enum MOT_TravelDirection
MOT_TravelDirectionDisabled = c_short(0x00)
MOT_Forwards = c_short(0x01)
MOT_Reverse = c_short(0x02)
MOT_TravelDirection = c_short

#enum MPC_IOModes
MPC_ToggleOnPositiveEdge = c_word(0x01)
MPC_SetPositionOnPositiveEdge = c_word(0x02)
MPC_OutputHighAtSetPosition = c_word(0x04)
MPC_OutputHighWhemMoving = c_word(0x08)
MPC_IOModes = c_word

#enum MOC_SignalModes
MPC_InputButton = c_word(0x01)
MPC_InputLogic = c_word(0x02)
MPC_InputSwap = c_word(0x04)
MPC_OutputLevel = c_word(0x10)
MPC_OutputPulse = c_word(0x20)
MPC_OutputSwap = c_word(0x40)
MPC_SignalModes = c_word

class PolarizerParameters(Structure):
    _fields_ = [("Velocity", c_ushort),
                ("HomePosition", c_double),
                ("JogSize1", c_double),
                ("JogSize2", c_double),
                ("JogSize3", c_double)]

class TLI_DeviceInfo(Structure):
    _fields_ = [("typeID", c_dword),
                ("description", (65 * c_char)),
                ("serialNo", (16 * c_char)),
                ("PID", c_dword),
                ("isKnownType", c_bool),
                ("motorType", MOT_MotorTypes),
                ("isPiezoDevice", c_bool),
                ("isLaser", c_bool),
                ("isCustomType", c_bool),
                ("isRack", c_bool),
                ("maxPaddles", c_short)]

class TLI_HardwareInformation(Structure):
    _fields_ = [("serialNumber", c_dword),
                ("modelNumber", (8 * c_char)),
                ("type", c_word),
                ("firmwareVersion", c_dword),
                ("notes", (48 * c_char)),
                ("deviceDependantData", (12 * c_byte)),
                ("hardwareVersion", c_word),
                ("modificationState", c_word),
                ("numChannels", c_short)]
        
class MPC_IOSettings(Structure):
    _fields_ = [("transitTime",c_uint),
                ("ADCspeedValue", c_uint),
                ("digIO1OperMode", MPC_IOModes),
                ("digIO1SignalMode",MPC_SignalModes),
                ("digIO1PulseWidth", c_uint),
                ("digIO2OperMode", MPC_IOModes),
                ("digIO2SignalMode", MPC_SignalModes),
                ("digIO2PulseWidth", c_uint),
                ("reserved1", c_int),
                ("reserved2", c_uint)]

# TLI_BuildDeviceList: This function builds an internal collection of all devices found on the USB that are not currently open.
TLI_BuildDeviceList = bind(lib, "TLI_BuildDeviceList", None, c_short)

# TLI_GetDeviceListSize: Gets the device list size.
TLI_GetDeviceListSize = bind(lib, "TLI_GetDeviceListSize", None, c_short)

# TLI_GetDeviceListExt: Get the entire contents of the device list.
TLI_GetDeviceListExt = bind(lib, "TLI_GetDeviceListExt", [POINTER(c_char), c_dword], c_short)

# TLI_GetDeviceListByTypeExt: Get the contents of the device list which match the supplied typeID
TLI_GetDeviceListByTypeExt = bind(lib, "TLI_GetDeviceListByTypeExt", [POINTER(c_char), c_dword, c_int], c_short)

# TLI_GetDeviceListByTypesExt: Get the contents of the device list which match the supplied typeIDs
TLI_GetDeviceListByTypesExt = bind(lib, "TLI_GetDeviceListByTypesExt", [POINTER(c_char), c_dword, POINTER(c_int), c_int], c_short)

# TLI_GetDeviceInfo: Get the device information from the USB port.
TLI_GetDeviceInfo = bind(lib, "TLI_GetDeviceInfo", [POINTER(c_char), POINTER(TLI_DeviceInfo)], c_short)

# MPC_Open: Open the device for communications.
MPC_Open = bind(lib, "MPC_Open", [POINTER(c_char)], c_short)

# MPC_Close: Disconnect and close the device.
MPC_Close = bind(lib, "MPC_Close", [POINTER(c_char)])

# MPC_CheckConnection: Check connection.
MPC_CheckConnection = bind(lib, "MPC_CheckConnection", [POINTER(c_char)], c_bool)

# MPC_Identify: Sends a command to the device to make it identify iteself.
MPC_Identify =  bind(lib, "MPC_Identify", [POINTER(c_char)])

# MPC_GetHardwareInfo: Gets the hardware information from the device
MPC_GetHardwareInfo = bind(lib, "MPC_GetHardwareInfo", [POINTER(c_char), POINTER(c_char), c_dword, POINTER(c_word), POINTER(c_word), POINTER(c_char), c_dword, POINTER(c_dword), POINTER(c_word), POINTER(c_word)], c_short)

# MPC_GetFirmwareVersion: Get  version number of firmware 
MPC_GetFirmwareVersion = bind(lib, "MPC_GetFirmwareVersion", [POINTER(c_char)], c_dword)

# MPC_GetSoftwareVersion: Gets version number of the device software.
MPC_GetSoftwareVersion = bind(lib, "MPC_GetSoftwareVersion", [POINTER(c_char)], c_dword)

# MPC_LoadSettings: Update device with stored settings.
MPC_LoadSettings = bind(lib, "MPC_LoadSettings", [POINTER(c_char)], c_bool)

# MPC_LoadNamedSettings:  Update device with named settings
MPC_LoadNamedSettings = bind(lib, "MPC_LoadNamedSettings", [POINTER(c_char), POINTER(c_char)], c_bool)

# MPC_PersistSettings: Persist the devices current settings.
MPC_PersistSettings = bind(lib, "MPC_PersistSettings", [POINTER(c_char)], c_bool)

# MPC_ResetParameters: Mpc reset parameters
MPC_ResetParameters = bind(lib, "MPC_ResetParameters", [POINTER(c_char)], c_bool)

# MPC_GetPaddleCount: Get number of polarizer paddles
MPC_GetPaddleCount = bind(lib, "MPC_GetPaddleCount", [POINTER(c_char)], c_int)

# MPC_GetEnabledPaddles: Gets enabled paddles.
MPC_GetEnabledPaddles = bind(lib, "MPC_GetEnabledPaddles", [POINTER(c_char)], POL_PaddleBits)

# MPC_IsPaddleEnabled:  Queries if a paddle is enabled
MPC_IsPaddleEnabled = bind(lib, "MPC_IsPaddleEnabled", [POINTER(c_char),POL_Paddles], c_bool)

# MPC_SetEnabledPaddles: Enables the specified paddles
MPC_SetEnabledPaddles = bind(lib, "MPC_SetEnabledPaddles", [POINTER(c_char),POL_PaddleBits], c_bool)

# MPC_GetMaxTravel:  Get the maximum travel in encoder steps
MPC_GetMaxTravel = bind(lib, "MPC_GetMaxTravel", [POINTER(c_char)], c_double)

# MPC_GetStepsPerDegree: Get the Ratio of encoder steps per degree.
MPC_GetStepsPerDegree = bind(lib, "MPC_GetStepsPerDegree", [POINTER(c_char)], c_double)

# MPC_Home: Home the device
MPC_Home = bind(lib, "MPC_Home", [POINTER(c_char), POL_Paddles], c_short)

# MPC_MoveToPosition:  Move the device to the specified position (index).
MPC_MoveToPosition = bind(lib, "MPC_MoveToPosition", [POINTER(c_char), POL_Paddles, c_double], c_short)

# MPC_Stop:  Stop the device
MPC_Stop = bind(lib, "MPC_Stop", [POINTER(c_char), POL_Paddles], c_short)

# MPC_Jog: Move the device to the specified position (index)
MPC_Jog = bind(lib, "MPC_Jog", [POINTER(c_char), POL_Paddles, MOT_TravelDirection], c_short)

# MPC_MoveRelative: Move the device to the specified position (index)
MPC_MoveRelative = bind(lib, "MPC_MoveRelative", [POINTER(c_char), POL_Paddles, c_double], c_short)

# MPC_GetPosition: Get the current position.
MPC_GetPosition = bind(lib, "MPC_MoveRelative", [POINTER(c_char), POL_Paddles], c_double)

# MPC_RequestPolParams:  Request polarizer parameters
MPC_RequestPolParams = bind(lib, "MPC_RequestPolParams",[POINTER(c_char)], c_short)

# MPC_GetPolParams:  Gets the polarizer parameters.
MPC_GetPolParams = bind(lib, "MPC_GetPolParams", [POINTER(c_char), POINTER(PolarizerParameters)], c_short)

# MPC_SetPolParams: Sets the polarizer parameters
MPC_SetPolParams = bind(lib, "MPC_SetPolParams", [POINTER(c_char), POINTER(PolarizerParameters)], c_short)

# MPC_SetJogSize: Sets jog size
MPC_SetJogSize = bind(lib, "MPC_SetJogSize", [POINTER(c_char), POL_Paddles, c_double], c_short)

# MPC_GetJogSize: Gets step size
MPC_GetJogSize = bind(lib, "MPC_GetJogSize", [POINTER(c_char), POL_Paddles], c_double)

# MPC_SetHomeOffset: Sets home offset.
MPC_SetHomeOffset = bind(lib, "MPC_SetHomeOffset", [POINTER(c_char), c_double], c_short)

# MPC_GetHomeOffset: Gets home offset
MPC_GetHomeOffset = bind(lib, "MPC_GetHomeOffset", [POINTER(c_char)], c_double)

# MPC_SetVelocity: Sets a velocity
MPC_SetVelocity = bind(lib, "MPC_SetVelocity", [POINTER(c_char), c_short], c_short)

# MPC_GetVelocity: Gets the velocity
MPC_GetVelocity = bind(lib, "MPC_GetVelocity", [POINTER(c_char)], c_short)

# MPC_RequestStatus: Request status bits.
MPC_RequestStatus = bind(lib, "MPC_RequestStatus", [POINTER(c_char)], c_short)

# MPC_GetStatusBits: Get the current status bits.
MPC_GetStatusBits = bind(lib, "MPC_GetStatusBits", [POINTER(c_char), POL_Paddles], c_dword)

# MPC_StartPolling: Starts the internal polling loop which continuously requests position and status.
MPC_StartPolling = bind(lib, "MPC_StartPolling", [POINTER(c_char), c_int], c_bool)

# MPC_PollingDuration: Gets the polling loop duration.
MPC_PollingDuration = bind(lib, "MPC_PollingDuration", [POINTER(c_char)], c_long)

# MPC_StopPolling: Stops the internal polling loop.
MPC_StopPolling = bind(lib, "MPC_StopPolling",[POINTER(c_char)])

# MPC_TimeSinceLastMsgReceived: Enables the last message monitoring timer. 
MPC_TimeSinceLastMsgReceived = bind(lib, "MPC_TimeSinceLastMsgReceived", [POINTER(c_char), c_int64], c_bool)

# MPC_EnableLastMsgTimer: Enables the last message monitoring timer
MPC_EnableLastMsgTimer = bind(lib, "MPC_EnableLastMsgTimer", [POINTER(c_char), c_bool, c_int32], c_bool)

# MPC_HasLastMsgTimerOverrun: Queries if the time since the last message has exceeded the lastMsgTimeout
MPC_HasLastMsgTimerOverrun = bind(lib, "MPC_HasLastMsgTimerOverrun", [POINTER(c_char)], c_bool)

# MPC_RequestSettings: Requests that all settings are download from device
MPC_RequestSettings = bind(lib, "MPC_RequestSettings", [POINTER(c_char)], c_short)

# MPC_ClearMessageQueue: Clears the device message queue
MPC_ClearMessageQueue = bind(lib, "MPC_ClearMessageQueue", [POINTER(c_char)])

# MPC_RegisterMessageCallback: Registers a callback on the message queue
MPC_RegisterMessageCallback = bind(lib, "MPC_RegisterMessageCallback",[POINTER(c_char), c_short, CFUNCTYPE(None)] )

# MPC_MessageQueueSize:  Gets the MessageQueue size
MPC_MessageQueueSize = bind(lib, "MPC_MessageQueueSize", [POINTER(c_char)], c_int)

# MPC_GetNextMessage: Get the next MessageQueue item
MPC_GetNextMessage = bind(lib, "MPC_GetNextMessage", [POINTER(c_char), POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool )

# MPC_WaitForMessage: Wait for next MessageQueue item.
MPC_WaitForMessage = bind(lib, "MPC_WaitForMessage", [POINTER(c_char), POINTER(c_word), POINTER(c_word), POINTER(c_dword)], c_bool )


















