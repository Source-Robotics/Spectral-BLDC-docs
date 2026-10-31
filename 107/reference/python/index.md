# Python library

The `Spectral-BLDC` package ([Spectral-BLDC-Python](https://github.com/Source-Robotics/Spectral-BLDC-Python),
`pip install Spectral-BLDC`) has one method per CAN message in `Spectral_BLDC.SpectralCAN`, and
`Spectral_BLDC.CanCommunication` for the bus. [With Python](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/python/) shows how they are used.

## Calls and messages

| Library call | Sends | Answered with | Reference |
|---|---|---|---|
| `Send_data_pack_1()` | Send_data_pack_1 (ID 2) | Respond_data_pack_1 | [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_data_pack_1) |
| `Send_data_pack_PD()` | Send_data_pack_PD (ID 4) | Respond_data_pack_1 | [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_data_pack_pd) |
| `Send_PD_Gains()` | Send_PD_Gains (ID 16) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_pd_gains) |
| `Send_Current_Gains()` | Send_Current_Gains (ID 17) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_current_gains) |
| `Send_Velocity_Gains()` | Send_Velocity_Gains (ID 18) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_velocity_gains) |
| `Send_Position_Gains()` | Send_Position_Gains (ID 19) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_position_gains) |
| `Send_Limits()` | Send_Limits (ID 20) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_limits) |
| `Send_Kt()` | Send_Kt (ID 22) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_kt) |
| `Send_Voltage_Limit()` | Send_Voltage_Limit (ID 34) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_voltage_limit) |
| `Send_Respond_Ping()` | Send_Respond_Ping (ID 10) | Send_Respond_Ping (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_ping) |
| `Send_Respond_Temperature()` | Send_Respond_Temperature (ID 23) | Send_Respond_Temperature (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_temperature) |
| `Send_Respond_Voltage()` | Send_Respond_Voltage (ID 24) | Send_Respond_Voltage (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_voltage) |
| `Send_Respond_Device_Info()` | Send_Respond_Device_Info (ID 25) | Send_Respond_Device_Info (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_device_info) |
| `Send_Respond_State_of_Errors()` | Send_Respond_State_of_Errors (ID 26) | Send_Respond_State_of_Errors (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_state_of_errors) |
| `Send_Respond_Iq_data()` | Send_Respond_Iq_data (ID 27) | Send_Respond_Iq_data (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_iq_data) |
| `Send_Respond_Encoder_data()` | Send_Respond_Encoder_data (ID 28) | Send_Respond_Encoder_data (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_encoder_data) |
| `Send_Respond_Kt()` | Send_Respond_Kt (ID 33) | Send_Respond_Kt (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_kt) |
| `Send_CAN_ID()` | Send_CAN_ID (ID 11) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_can_id) |
| `Send_ESTOP()` | Send_ESTOP (ID 0) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_estop) |
| `Send_Idle()` | Send_Idle (ID 12) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_idle) |
| `Send_Save_config()` | Send_Save_config (ID 13) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_save_config) |
| `Send_Reset()` | Send_Reset (ID 14) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_reset) |
| `Send_Clear_Error()` | Send_Clear_Error (ID 1) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_clear_error) |
| `Send_Watchdog()` | Send_Watchdog (ID 15) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_watchdog) |
| `Send_Heartbeat_Setup()` | Send_Heartbeat_Setup (ID 30) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_heartbeat_setup) |
| `Send_gripper_data_pack()` | Send_gripper_data_pack (ID 61) | Respond_Gripper_data_pack | [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gripper/#send_gripper_data_pack) |
| `Send_gripper_calibrate()` | Send_gripper_calibrate (ID 62) | — | [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gripper/#send_gripper_calibrate) |

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
