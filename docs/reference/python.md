# Python library

The `Spectral-BLDC` package ([Spectral-BLDC-Python](https://github.com/Source-Robotics/Spectral-BLDC-Python),
`pip install Spectral-BLDC`) has one method per CAN message in `Spectral_BLDC.SpectralCAN`, and
`Spectral_BLDC.CanCommunication` for the bus. [With Python](../06-operation/python.md) shows how they are used.

## Calls and messages

<!-- python-calls -->

## Receiving

`CanCommunication.receive_can_messages(timeout)` returns `(message, ids)`: the raw `python-can` message and a tuple
`ids` with `node_id`, `command_id` and `error_bit` from the identifier, or `(None, None)` after the timeout.
`SpectralCAN.UnpackData(message, ids)` decodes the message into the object's attributes:

| Message | Attributes |
|---|---|
| Respond_data_pack_1 | `position`, `speed`, `current` |

| Send_Respond_Encoder_data | `position`, `speed` |
| Send_Respond_Iq_data | `current` |
| Send_Respond_Temperature | `temperature` |
| Send_Respond_Voltage | `voltage` |
| Send_Respond_Device_Info | `HARDWARE_VERSION`, `BATCH_DATE`, `SOFTWARE_VERSION`, `SERIAL_NUMBER` |
| Send_Respond_State_of_Errors | `error`, `temperature_error`, `encoder_error`, `vbus_error`, `driver_error`, `velocity_error`, `current_error`, `estop_error`, `calibrated`, `activated`, `watchdog_error` |
| Send_Respond_Kt | `Kt` |
| Respond_Gripper_data_pack | `gripper_position`, `gripper_current`, `gripper_activated`, `gripper_action_status`, `gripper_object_detection`, `gripper_temperature_error`, `gripper_timeout_error`, `gripper_estop_error`, `gripper_calibrated` |

!!! note "Object detection in the library"
    Library version 1.20 assembles `gripper_object_detection` with the two bits swapped relative to the firmware,
    so it reports 1 where the gripper sends 2 (object detected while opening) and 2 where it sends 1 (object
    detected while closing); 0 and 3 are unaffected. Until the library is fixed, swap the two values in your
    program, or read the bits yourself from the frame.
