# Versions and compatibility

Which firmware release works with which bootloader, Python library, PAR6 runtime and board revision. One row per firmware release, newest first.

| Firmware | Released | Bootloader | STEPFOC equivalent | Python library (Spectral-BLDC) | PAR6 runtime | Spectral Micro PCB | Docs |
|---|---|---|---|---|---|---|---|
| 107 | 2026-08-26 | required (installed on boards shipped with 105 or newer) | 108 | 1.20 or newer | 0.9 or newer | v2.0 | 107 |
| 106 | 2026-07-06 | required | 106 and 107 | 1.19 or newer | 0.9 or newer | v2.0 | not published |
| 105 | 2026-07-05 | required (the first release that needs it) | 105 | 1.19 or newer | 0.9 or newer | v2.0 | not published |
| 104 | 2026-06-19 | none (flashed with a programming adapter); the last release of the main branch | 104 | 1.19 or newer (1.20 for Send_Voltage_Limit) | 0.9 or newer | v2.0 | 101 applies; 104 adds the Send_Voltage_Limit message |
| 101 | 2025-09-29 | none (flashed with a programming adapter) | 103 | 1.17 or newer | 0.9 or newer | v2.0 | 101 |

`#Info` prints the firmware release a driver runs; `Send_Respond_Device_Info` returns it over CAN.
