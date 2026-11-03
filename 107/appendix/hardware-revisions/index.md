# Hardware revisions

What changed in each revision of the Spectral Micro board, and which firmware and which revision of this manual go
with it. The board reports its hardware revision in `#Info` (`Hardware version`) and in Send_Respond_Device_Info;
the silkscreen on the bottom of the board carries the board's name and date.

| Revision | Marked | Changes | Firmware | Manual |
|---|---|---|---|---|
| v2.0 | Spectral motor controller micro v2.0, 10.1.2024 | the production board | 101 and newer; 104 and newer run on the bootloader | this manual |

A board that runs firmware 101 or older has no bootloader; [Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/bootloader/)
brings it to the current firmware.
