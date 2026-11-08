# Python library

The `Spectral-BLDC` package ([Spectral-BLDC-Python](https://github.com/Source-Robotics/Spectral-BLDC-Python),
`pip install Spectral-BLDC`) has one method per CAN message in `Spectral_BLDC.SpectralCAN`, and
`Spectral_BLDC.CanCommunication` for the bus. [With Python](../06-operation/python.md) shows how they are used.

## Calls and messages

<!-- python-calls -->

The calls for the messages added in firmware 108 (Send_Parameter, Send_Get_Parameter, Send_Respond_Identity,
Send_Respond_Telemetry, Send_Buffer_Read, Send_Cogging_Harmonic, Send_Cogging_Table), and the actions 'Coast' and
'Descend' of Send_Watchdog, come with the library's release after 1.20. It also adds calls built on the
parameters, among them Send_Watchdog_Fallback, Send_Tool_ID, Send_Cogging_Mode, Send_Capture_Setup,
Send_Capture_Trigger, Send_Histogram, Send_Cogging_Calibrate and Send_Encoder_Calibrate. With 1.20, send those
frames with `python-can` in the layouts of the [CAN reference](can/index.md).

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
| Send_Respond_State_of_Errors | `error`, `temperature_error`, `encoder_error`, `vbus_error`, `driver_error`, `velocity_error`, `current_error`, `estop_error`, `calibrated`, `activated`, `watchdog_error`; from the release after 1.20 also `wrong_product` |
| Send_Respond_Identity (release after 1.20) | `product_id`, `product_name`, `tool_id`, `firmware_version`, `identity_hardware_version`, `pole_pairs`, `identity_calibrated`, `identity_flags` |
| Send_Respond_Telemetry (release after 1.20) | `temperature`, `voltage`, the error flags as above, `current` |
| Respond_Parameter (release after 1.20) | `parameters[number]` (floats for 8-16 and 20), `unknown_parameter`; `tool_id` and `watchdog_fallback` when those parameters come in |
| Respond_Buffer_Data (release after 1.20) | `capture[index]`, `histogram[bin]`, `cogging_harmonics[slot]`, `cogging_table[index]`, `encoder_table[index]` |
| Send_Respond_Kt | `Kt` |
| Respond_Gripper_data_pack | `gripper_position`, `gripper_current`, `gripper_activated`, `gripper_action_status`, `gripper_object_detection`, `gripper_temperature_error`, `gripper_timeout_error`, `gripper_estop_error`, `gripper_calibrated` |

!!! note "Object detection in the library"
    Library version 1.20 assembles `gripper_object_detection` with the two bits swapped relative to the firmware,
    so it reports 1 where the gripper sends 2 (object detected while opening) and 2 where it sends 1 (object
    detected while closing); 0 and 3 are unaffected. The library's release after 1.20 reads them right. With 1.20,
    swap the two values in your program, or read the bits yourself from the frame.
