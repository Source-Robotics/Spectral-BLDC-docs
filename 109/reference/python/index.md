# Python library

The `Spectral-BLDC` package ([Spectral-BLDC-Python](https://github.com/Source-Robotics/Spectral-BLDC-Python),
`pip install Spectral-BLDC`) has one method per CAN message in `Spectral_BLDC.SpectralCAN`, and
`Spectral_BLDC.CanCommunication` for the bus. [With Python](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/python/) shows how they are used.

## Calls and messages

| Library call | Sends | Answered with | Reference |
|---|---|---|---|
| `Send_data_pack_1()` | Send_data_pack_1 (ID 2) | Respond_data_pack_1 | [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/motion/#send_data_pack_1) |
| `Send_data_pack_PD()` | Send_data_pack_PD (ID 4) | Respond_data_pack_1 | [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/motion/#send_data_pack_pd) |
| `Send_PD_Gains()` | Send_PD_Gains (ID 16) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_pd_gains) |
| `Send_Current_Gains()` | Send_Current_Gains (ID 17) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_current_gains) |
| `Send_Velocity_Gains()` | Send_Velocity_Gains (ID 18) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_velocity_gains) |
| `Send_Position_Gains()` | Send_Position_Gains (ID 19) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_position_gains) |
| `Send_Limits()` | Send_Limits (ID 20) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_limits) |
| `Send_Kt()` | Send_Kt (ID 22) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_kt) |
| `Send_Voltage_Limit()` | Send_Voltage_Limit (ID 34) | — | [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_voltage_limit) |
| `Send_Respond_Ping()` | Send_Respond_Ping (ID 10) | Send_Respond_Ping (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_ping) |
| `Send_Respond_Temperature()` | Send_Respond_Temperature (ID 23) | Send_Respond_Temperature (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_temperature) |
| `Send_Respond_Voltage()` | Send_Respond_Voltage (ID 24) | Send_Respond_Voltage (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_voltage) |
| `Send_Respond_Device_Info()` | Send_Respond_Device_Info (ID 25) | Send_Respond_Device_Info (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_device_info) |
| `Send_Respond_State_of_Errors()` | Send_Respond_State_of_Errors (ID 26) | Send_Respond_State_of_Errors (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_state_of_errors) |
| `Send_Respond_Iq_data()` | Send_Respond_Iq_data (ID 27) | Send_Respond_Iq_data (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_iq_data) |
| `Send_Respond_Encoder_data()` | Send_Respond_Encoder_data (ID 28) | Send_Respond_Encoder_data (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_encoder_data) |
| `Send_Respond_Kt()` | Send_Respond_Kt (ID 33) | Send_Respond_Kt (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_kt) |
| `Send_Respond_Identity()` | Send_Respond_Identity (ID 39) | Send_Respond_Identity (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_identity) |
| `Send_Respond_Telemetry()` | Send_Respond_Telemetry (ID 40) | Send_Respond_Telemetry (data frame) | [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_telemetry) |
| `Send_CAN_ID()` | Send_CAN_ID (ID 11) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_can_id) |
| `Send_ESTOP()` | Send_ESTOP (ID 0) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_estop) |
| `Send_Idle()` | Send_Idle (ID 12) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_idle) |
| `Send_Save_config()` | Send_Save_config (ID 13) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_save_config) |
| `Send_Reset()` | Send_Reset (ID 14) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_reset) |
| `Send_Clear_Error()` | Send_Clear_Error (ID 1) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_clear_error) |
| `Send_Watchdog()` | Send_Watchdog (ID 15) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_watchdog) |
| `Send_Heartbeat_Setup()` | Send_Heartbeat_Setup (ID 30) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_heartbeat_setup) |
| `Send_Settings()` | Send_Settings (ID 35) | — | [System](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/system/#send_settings) |
| `Send_Parameter()` | Send_Parameter (ID 36) | — | [Parameters and buffers](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#send_parameter) |
| `Send_Get_Parameter()` | Send_Get_Parameter (ID 37) | Respond_Parameter | [Parameters and buffers](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#send_get_parameter) |
| `Send_Buffer_Read()` | Send_Buffer_Read (ID 41) | — | [Parameters and buffers](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#send_buffer_read) |
| `Send_Cogging_Harmonic(), Send_Cogging_Table()` | Send_Buffer_Write (ID 43) | — | [Parameters and buffers](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#send_buffer_write) |
| `Send_Sound()` | Send_Sound (ID 44) | — | [Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/sound/#send_sound) |
| `Send_Samples()` | Send_Sound_Samples (ID 45) | — | [Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/sound/#send_sound_samples) |
| `Send_gripper_data_pack()` | Send_gripper_data_pack (ID 61) | Respond_Gripper_data_pack | [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gripper/#send_gripper_data_pack) |
| `Send_gripper_calibrate()` | Send_gripper_calibrate (ID 62) | — | [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gripper/#send_gripper_calibrate) |

The calls for the messages added in firmware 109 (Send_Parameter, Send_Get_Parameter, Send_Respond_Identity,
Send_Respond_Telemetry, Send_Buffer_Read, Send_Cogging_Harmonic, Send_Cogging_Table, Send_Sound, Send_Samples),
Send_Settings and Send_Brake_Coast for the idle behaviour, and the actions 'Coast' and
'Descend' of Send_Watchdog, come with library 1.21. It also adds calls built on the
parameters, among them Send_Watchdog_Fallback, Send_Tool_ID, Send_Cogging_Mode, Send_Capture_Setup,
Send_Capture_Trigger, Send_Histogram, Send_Cogging_Calibrate and Send_Encoder_Calibrate; the sound calls Send_Tone,
Send_Sound_Stop, Send_Sound_Event, Send_Sound_Play, Send_Sound_Clear, Send_Samples_Play and Send_Samples_Stop on top
of Send_Sound and Send_Samples; and the module `Spectral_BLDC.music` (note names, ringtone melodies, MIDI and WAV
files as queue events and samples, see [Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/sound/)).

The same release adds `Spectral_BLDC.helpers`, blocking functions that send a request and wait for the answer:
`get_parameter` and `set_parameter` (which reads the value back), `read_identity`, `read_telemetry`, `features`,
`read_buffer`, `capture`, `wait_for_state` (for the encoder table, the anti-cogging and other runs), and
`play_events` and `stream_samples` for sound. They are for setting up and diagnostics, not for the inside of a fast
control loop. The library's `examples` folder shows them at work: `parameters_and_status.py`, `capture.py`,
`calibration_features.py`, `watchdog.py` and `sound.py`.

The same release is stricter about what it sends and reads:

- `Send_Parameter` takes the value itself. Parameters 8 to 16 and 20 are sent as floats
  (`Send_Parameter(16, 1500)` is 1500 mA); every other parameter takes a whole number, and anything else raises
  `ValueError`.
- A position or a speed that does not fit 24 bits, or a current that does not fit 16 bits, raises `ValueError`;
  1.20 wrapped it round. `Send_Voltage_Limit` raises `ValueError` outside 0 to 60000 mV.
- A node ID must be 0 to 15.
- `UnpackData` ignores frames from other nodes, remote frames and extended frames.
- Parameters 79, 80 and 84 to 87 read as unsigned numbers.
- A send that fails returns `False` and is logged once.

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
| Send_Respond_State_of_Errors | `error`, `temperature_error`, `encoder_error`, `vbus_error`, `driver_error`, `velocity_error`, `current_error`, `estop_error`, `calibrated`, `activated`, `watchdog_error`; from 1.21 also `wrong_product` |
| Send_Respond_Identity (1.21 and newer) | `product_id`, `product_name`, `tool_id`, `firmware_version`, `identity_hardware_version`, `pole_pairs`, `identity_calibrated`, `identity_flags` |
| Send_Respond_Telemetry (1.21 and newer) | `temperature`, `voltage`, the error flags as above, `current` |
| Respond_Parameter (1.21 and newer) | `parameters[number]` (floats for 8-16 and 20), `unknown_parameter`; `tool_id` and `watchdog_fallback` when those parameters come in |
| Respond_Buffer_Data (1.21 and newer) | `capture[index]`, `histogram[bin]`, `cogging_harmonics[slot]`, `cogging_table[index]`, `encoder_table[index]` |
| Send_Respond_Kt | `Kt` |
| Respond_Gripper_data_pack | `gripper_position`, `gripper_current`, `gripper_activated`, `gripper_action_status`, `gripper_object_detection`, `gripper_temperature_error`, `gripper_timeout_error`, `gripper_estop_error`, `gripper_calibrated` |

!!! note "Object detection in the library"
    Library 1.20 and older assemble `gripper_object_detection` with the two bits swapped relative to the
    firmware, so they report 1 where the gripper sends 2 (object detected while opening) and 2 where it sends 1
    (object detected while closing); 0 and 3 are unaffected. 1.21 and newer read them right.
