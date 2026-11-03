# Versions and compatibility

Which firmware release works with which bootloader, Python library, PAR6 runtime and board revision. One row per firmware release, newest first.

| Firmware | Released | Bootloader | STEPFOC equivalent | Python library (Spectral-BLDC) | PAR6 runtime | Spectral Micro PCB | Docs |
|---|---|---|---|---|---|---|---|
| 107 | 2026-08-26 | required | 108 (STEPFOC 107 has the Send_Settings and PD changes of this release, without its calibration fix) | 1.20 or newer | 0.9 or newer | v2.0 | 107 |
| 106 | 2026-07-06 | required | 106 | 1.19 or newer | 0.9 or newer | v2.0 | not published |
| 105 | 2026-07-05 | required | 105 | 1.19 or newer | 0.9 or newer | v2.0 | not published |
| 104 | 2026-06-19 | required (the first release built for the bootloader, from Bootloader_main) | none (STEPFOC has no 104 release) | 1.19 or newer (1.20 for Send_Voltage_Limit) | 0.9 or newer | v2.0 | 101 applies; 104 adds Send_Respond_Kt, Send_Voltage_Limit (in the release image) and the bootloader |
| 101 | 2025-09-29 | none (flashed with a programming adapter) | 103 | 1.17 or newer | 0.9 or newer | v2.0 | 101 |

`#Info` prints the firmware release a driver runs; `Send_Respond_Device_Info` returns it over CAN.
