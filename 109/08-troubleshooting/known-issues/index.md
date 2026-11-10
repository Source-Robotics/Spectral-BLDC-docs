# Known issues

The faults in the Spectral Micro firmware that are known and not yet fixed, and what to do until they are. The pages that
describe each part say the same where it matters; this page collects them in one place. Which releases work
together is in [Versions and compatibility](https://docs.source-robotics.com/Spectral-BLDC-docs/109/appendix/compatibility/).

### Spectral Micro firmware

Seen in: 109.

| | What happens | What to do | More |
|---|---|---|---|
| KI-3 | The serial number is not read back from the EEPROM at power-up, so `#SERNUM`, Motor GUI and Send_Respond_Device_Info report 1, and every `#Save` writes that 1 over the stored number. | Tell drivers apart by their CAN node ID. To keep a serial number stored, set it with `#SERNUM` before every `#Save`. | [Saving: what is not saved](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/saving/#what-is-not-saved) |
| KI-4 | For anyone reading or changing the source, the start values in `common.h` are not the factory defaults (the gripper flag starts at 1, the pole pairs at 11, `Max_Vbus` at 29500 mV). The EEPROM replaces them at power-up, so a running driver does not show them. | Take the defaults from the Defaults page, which lists what `#Default` writes, or from `Set_Default_config()` in `EEPROM.cpp`. | [Defaults](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/defaults/) |
| KI-5 | While the E-stop bit of the last Send_gripper_data_pack (or `#Gripstop 1`) is 1, the driver raises the gripper E-stop error again on every control cycle, so Send_Clear_Error or `#Clear` alone does not clear it. | Send a gripper frame with the E-stop bit 0 (or `#Gripstop 0`) first, then clear the error. | [Gripper mode: moving](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/gripper-mode/#moving) |
| KI-6 | The answer to a 5-byte Send_gripper_data_pack goes out before the driver has acted on the command, so its object detection and error bits are those of the moment before, for example 3 (position reached) from the previous move. | Judge the new move by the answers to later frames, or poll with an empty Send_gripper_data_pack. | [Gripper mode: moving](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/gripper-mode/#moving) |
| KI-7 | A 5-byte Send_gripper_data_pack, Send_Clear_Error or `#Clear` during the gripper calibration stops it without a message and leaves its counters as they were, so the next calibration starts part way through; it may skip the opening or give up early. | Send only empty status polls while the gripper calibrates (up to about 30 s). After an interrupted calibration, switch the driver off and on before you calibrate again. | [Gripper mode: calibrating](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/gripper-mode/#calibrating-the-gripper) |
| KI-8 | The action bit in Respond_Gripper_data_pack is a copy of the last command's action bit; the driver never clears it, so it stays 1 after the move has ended. | Tell the end of a move by the object detection, 3 position reached, 1 or 2 stopped on an object. | [Respond_Gripper_data_pack](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gripper/#respond_gripper_data_pack) |
| KI-9 | Open loop (`#Openloop`) puts the voltage `#Openv` (5000 mV by default) on the phases without a current limit; `#Ilim` does not apply, so a low-resistance motor draws far more than its limit. | Lower `#Openv` before you run a low-resistance motor in open loop, and keep the test short. | [Control modes](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/modes/) |
| KI-10 | The velocity error trips only above a fixed 20,000,000 ticks/s, about 1220 revolutions per second and far above the speeds the driver can follow; `#Vlimit` does not change it, so it does not catch a motor that runs away. | Watch the speed in your host and send Send_Idle or Send_ESTOP when it is wrong. | [Errors and recovery](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/errors/) |
| KI-11 | Only motion frames and answered status requests reset the watchdog. Setting frames (gains, limits, Idle, Clear) and UART commands do not, so a host that only configures the driver, or a terminal session with a saved watchdog, ends in a watchdog error. | While the watchdog runs, send a status request such as Send_Respond_Encoder_data within every watchdog period. Before you work over UART alone, set the watchdog to 0 and save (`#Par 6,0`, then `#Save`). | [The watchdog](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/errors/#the-watchdog) |
| KI-12 | The current a turned motor drives through its shorted phases while the driver brakes in idle (`#Brake 1`) is not limited. | Brake only a motor whose resistance keeps that current under 2.8 A at the speeds it is turned at, and do not let a load drive a braking motor fast. | [Braking in idle](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/modes/#braking-in-idle) |
| KI-13 | `#Save` does not keep the idle behaviour: after every power-up the driver coasts in idle again, whatever `#Brake` or Send_Settings set before. | Send `#Brake 1` (or Send_Settings) after every power-up when the motor must brake in idle. | [Braking in idle](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/modes/#braking-in-idle) |
| KI-14 | Send_Respond_Device_Info carries the batch date in one byte, its lowest 8 bits, so a host reading it over CAN gets 120 for the 24092024 that `#Default` stores. | Read the batch date with `#Info` over UART, which prints the whole number. | [Send_Respond_Device_Info](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/status/#send_respond_device_info) |
| KI-19 | The encoder table holds a field current of 80 % of the current limit for about 20 s, also in the run that follows every `#Cal`. With a limit above the motor's rating (1000 mA after `#Default`), the run is above the rating too. | Set `#Ilim` for the motor before `#Encal` and before every `#Cal` (calibration puts the limit that was in force back before the runs that follow). | [Encoder table and anti-cogging: running them](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/anti-cogging/#running-them) |

### Release 104

Seen in: the image of the GitHub release V104.

| | What happens | What to do | More |
|---|---|---|---|
| KI-16 | For anyone who builds or reads the source of release 104, the tag `V104` is not what its image was built from. The image comes from commit `20765c9` on `Bootloader_main`, which adds Send_Voltage_Limit; the tag lacks it. | Check out `20765c9` to see or rebuild the 104 image's source; better, update the board to the current release. | [Releases: the two branches](https://docs.source-robotics.com/Spectral-BLDC-docs/109/07-firmware/releases/#the-two-branches) |

### Fixed

| | What happened | Fixed in | More |
|---|---|---|---|
| KI-1 | The current limit of Send_Limits over CAN is used as sent, also above the driver's 2800 mA; only `#Ilim` over UART clamps it. | 109: Send_Limits stops the current limit at 2800 mA and ignores a negative value | [Send_Limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/gains-and-limits/#send_limits) |
| KI-2 | Calibration sets the current limit to 1600 mA and leaves it there, whatever it was before; a `#Save` right after calibration stores the 1600 mA. | 109: calibration puts back the current limit that was in force when it started | [Calibration: current limit and save](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/calibration/#3-set-the-current-limit-and-save) |
| KI-15 | `#Error` prints `FAULT pin is HIGH` while the driver stage reports a fault, which is when that pin is low: the text names the wrong level. | 109: the line reads `FAULT pin is LOW: the gate driver reports a fault` | [Errors and recovery](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/errors/) |

## Something that is not here

Check the [symptom tables](https://docs.source-robotics.com/Spectral-BLDC-docs/109/08-troubleshooting/) first. If it is still not explained, [Report a problem](https://docs.source-robotics.com/Spectral-BLDC-docs/109/support/report-a-problem/)
says what to include so it can be reproduced. A fixed issue stays on this page, under "Fixed", with the release
that fixes it.
