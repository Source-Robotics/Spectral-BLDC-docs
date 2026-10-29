# Hardware revisions

What changed in each revision of the Spectral Micro board, and which firmware and which revision of this manual go
with it. The board reports its hardware revision in `#Info` (`Hardware version`) and in Send_Respond_Device_Info;
the silkscreen on the bottom of the board carries the board's name and date.

| Revision | Marked | Changes | Firmware | Manual |
|---|---|---|---|---|
| v2.0 | Spectral motor controller micro v2.0, 10.1.2024 | the production board | 101 and newer; 105 and newer ship with the bootloader | this manual |

Boards shipped before firmware 105 have no bootloader; [Installing the bootloader on an older board](../07-firmware/bootloader.md)
brings them to the current firmware.
