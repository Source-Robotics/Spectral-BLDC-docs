# CAN protocol

CAN 2.0, 1 Mbit/s, 11-bit identifiers. The identifier carries the node ID (bits 10 to 7, 0 to 15), the command ID
(bits 6 to 1, 0 to 63) and, in frames from the driver, the error bit (bit 0). [Over CAN](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/can/)
explains how the pieces are used; this page lists them.

Three kinds of message:

- **Send_…** — the host sends data to the driver. A few are answered (the motion commands with
  Respond_data_pack_1, the gripper command with Respond_Gripper_data_pack); most are not.
- **Send_Respond_…** — the host asks for data with a **remote frame** (RTR bit set, no data) under the command ID;
  the driver answers with a data frame under the same command ID.
- **Respond_…** — frames only the driver sends.

Multi-byte values are big-endian (data[0] first); floats are IEEE 754 single precision; bits inside a byte are
numbered from the most significant bit (bit 7 first).

## Every message

| ID | Message | Direction | Length | Group |
|---|---|---|---|---|
| 0 | [Send_ESTOP](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_estop) | host → driver | 0 | System |
| 1 | [Send_Clear_Error](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_clear_error) | host → driver | 0 | System |
| 2 | [Send_data_pack_1](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_data_pack_1) | host → driver | 2, 5, 8 | Motion |
| 3 | [Respond_data_pack_1](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#respond_data_pack_1) | driver → host | 8 | Motion |
| 4 | [Send_data_pack_PD](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_data_pack_pd) | host → driver | 8 | Motion |
| 5 | [Respond_data_pack_2](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#respond_data_pack_2) | driver → host | 0 | Motion |
| 6 | [Send_data_pack_2](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_data_pack_2) | host → driver | not implemented | Motion |
| 7 | [Respond_data_pack_3](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#respond_data_pack_3) | driver → host | 0 | Motion |
| 8 | [Send_data_pack_3](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_data_pack_3) | host → driver | not implemented | Motion |
| 9 | [Respond_Heartbeat](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#respond_heartbeat) | driver → host | 0 | Status requests |
| 10 | [Send_Respond_Ping](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_ping) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 0 | Status requests |
| 11 | [Send_CAN_ID](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_can_id) | host → driver | 1 | System |
| 12 | [Send_Idle](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_idle) | host → driver | 0 | System |
| 13 | [Send_Save_config](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_save_config) | host → driver | 0 | System |
| 14 | [Send_Reset](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_reset) | host → driver | 0 | System |
| 15 | [Send_Watchdog](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_watchdog) | host → driver | 5 | System |
| 16 | [Send_PD_Gains](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_pd_gains) | host → driver | 8 | Gains and limits |
| 17 | [Send_Current_Gains](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_current_gains) | host → driver | 8 | Gains and limits |
| 18 | [Send_Velocity_Gains](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_velocity_gains) | host → driver | 8 | Gains and limits |
| 19 | [Send_Position_Gains](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_position_gains) | host → driver | 4 | Gains and limits |
| 20 | [Send_Limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_limits) | host → driver | 8 | Gains and limits |
| 21 | [Send_Iq](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/#send_iq) | host → driver | not implemented | Motion |
| 22 | [Send_Kt](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_kt) | host → driver | 4 | Gains and limits |
| 23 | [Send_Respond_Temperature](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_temperature) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 2 | Status requests |
| 24 | [Send_Respond_Voltage](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_voltage) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 2 | Status requests |
| 25 | [Send_Respond_Device_Info](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_device_info) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 7 | Status requests |
| 26 | [Send_Respond_State_of_Errors](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_state_of_errors) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 2 | Status requests |
| 27 | [Send_Respond_Iq_data](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_iq_data) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 2 | Status requests |
| 28 | [Send_Respond_Encoder_data](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_encoder_data) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 8 | Status requests |
| 29 | [Send_Cyclic_command](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_cyclic_command) | host → driver | not implemented | System |
| 30 | [Send_Heartbeat_Setup](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_heartbeat_setup) | host → driver | 4 | System |
| 33 | [Send_Respond_Kt](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/#send_respond_kt) | host → driver as a remote frame, driver → host as a data frame | 0 (remote) / 4 | Status requests |
| 34 | [Send_Voltage_Limit](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/#send_voltage_limit) | host → driver | 4 | Gains and limits |
| 35 | [Send_Settings](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/#send_settings) | host → driver | 2 | System |
| 60 | [Respond_Gripper_data_pack](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gripper/#respond_gripper_data_pack) | driver → host | 4 | Gripper |
| 61 | [Send_gripper_data_pack](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gripper/#send_gripper_data_pack) | host → driver | 0, 5 | Gripper |
| 62 | [Send_gripper_calibrate](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gripper/#send_gripper_calibrate) | host → driver | 0 | Gripper |

## By group

- [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/motion/): the motion commands and their answers
- [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gains-and-limits/): the loop gains, the limits, Kt
- [Status requests](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/status/): temperature, voltage, identity, errors, current, encoder, Kt, the heartbeat
- [System](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/system/): node ID, E-stop, idle, save, reset, clear, watchdog, heartbeat setup, settings
- [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/gripper/): the gripper command, calibration and the gripper state

## The Python library

Every message the host can send has a method of the same name in `Spectral_BLDC.SpectralCAN`, listed in
[Python library](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/python/).

## Tools and downloads

[Build or decode a CAN frame, and download this firmware's JSON and DBC definitions](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can-tools/).
