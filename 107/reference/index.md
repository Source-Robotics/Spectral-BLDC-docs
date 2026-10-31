# API reference

Every CAN message and every UART command of the firmware release this site describes, the defaults the firmware
starts with, the error flags, and the map from the Python library's calls to the messages they send.

## Where the facts come from

The command IDs, the frame lengths the firmware accepts, the responses it sends, the list of UART commands with
their kind (Set/Get, Get or action), their argument type, the mode each enters and what it prints, and the
defaults are read from the firmware's source at its release tag by `tools/sync_firmware.py` in the documentation
repository, and the pages are built from that at every build. The descriptions, units and byte layouts are
written by hand, and the build fails when they name a command the firmware does not have, or miss one it has, or
when a byte layout does not fit the frame. The firmware version is in the version box on the
[landing page](https://docs.source-robotics.com/Spectral-BLDC-docs/107/).

## Conventions

- **Bytes** are numbered from 0, the first byte on the bus (`data[0]`). Multi-byte values are **big-endian**: the
  most significant byte first. Floats are IEEE 754 single precision in 4 bytes.
- **Bits** inside a byte are numbered from the most significant bit: bit 7 is the first flag the firmware packs
  into the byte, bit 0 the last.
- **Encoder ticks**: 16384 per revolution; speeds in ticks per second; currents in mA; voltages in mV.
- UART command names are **case-sensitive** and spelled exactly as the firmware compares them.

## In the API reference

- [CAN protocol](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/): the identifier, the three kinds of message, every message by group
- [UART commands](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/): the syntax and every command by group
- [Defaults](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/defaults/)
- [Errors and LED states](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/errors/)
- [Python library](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/python/): library call → message
