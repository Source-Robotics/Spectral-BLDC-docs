# CAN protocol

CAN 2.0, 1 Mbit/s, 11-bit identifiers. The identifier carries the node ID (bits 10 to 7, 0 to 15), the command ID
(bits 6 to 1, 0 to 63) and, in frames from the driver, the error bit (bit 0). [Over CAN](../../06-operation/can.md)
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

<!-- can-overview -->

## By group

- [Motion](motion.md): the motion commands and their answers
- [Gains and limits](gains-and-limits.md): the loop gains, the limits, Kt
- [Status requests](status.md): temperature, voltage, identity, errors, current, encoder, Kt, the heartbeat
- [System](system.md): node ID, E-stop, idle, save, reset, clear, watchdog, heartbeat setup, settings
- [Gripper](gripper.md): the gripper command, calibration and the gripper state

## The Python library

Every message the host can send has a method of the same name in `Spectral_BLDC.SpectralCAN`, listed in
[Python library](../python.md).

## Tools and downloads

[Build or decode a CAN frame, and download this firmware's JSON and DBC definitions](../can-tools.md).
