# Saving the configuration

Nothing you set survives a power cycle until you save it.

=== "Motor GUI"
    **Save**. The GUI marks *Unsaved changes* until you do.

=== "Terminal"
    ```
    #Save
    ```

Saving writes the configuration to the EEPROM: the motor parameters and the calibration, every gain and limit,
the CAN node ID, the heartbeat and watchdog settings, the thermistor and LED settings, the temperature and voltage
limits and the gripper flag. From firmware 109 also the tool id and the watchdog fallback, the anti-cogging set
with its mode and scale, and the encoder table with its on/off switch, parameter 56 and the current-sense zero
trims. Over CAN, Send_Save_config does the same. Saving also copies the node ID into the bootloader's board ID
([The bootloader](https://docs.source-robotics.com/Spectral-BLDC-docs/109/07-firmware/the-bootloader/#the-board-id)). Save after calibration, after tuning, and
after changing the node ID.

!!! warning "Set the current limit before you save a calibration"
    Firmware 107 and older left the current limit at 1600 mA after a calibration, and a save stored it. From
    firmware 109 calibration puts the limit that was in force back; check that it suits your motor (`#Ilim`)
    before you save.

## What is not saved

These settings are lost at a power cycle, whatever you save. The driver starts with the values in the
[Defaults](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/defaults/) reference:

- the idle behaviour (`#Brake`, Send_Settings): the driver coasts after every power-up;
- the calibration settings `#Cbw` (160 Hz; the gains it computed are kept), `#Resv`, `#Calpwr`, `#Openv`,
  `#Opens`, `#Vp` and `#Iqoffset`: set them again before each calibration that needs other values;
- the parameters of firmware 109 that tune the loops: the speed estimate (the direct PLL at 100 Hz), the
  commutation delay compensation (234 µs), the sin/cos table (off), the position input filter and the velocity-integral deadband
  (off), the anti-cogging identification speed, the d-axis current, and the capture and histogram settings. The
  [parameter table](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#every-parameter) says for every parameter whether it is kept;
- the cyclic output (`#Cyc`, `#Cyca`);
- the serial number. Saving writes it, but the firmware does not read it back at power-up: after a power cycle
  the driver reports 1, and the next save writes that 1 over the stored number.

## The defaults

=== "Motor GUI"
    *Default* in the settings.

=== "Terminal"
    ```
    #Default
    ```

Restoring the defaults writes the factory values to the EEPROM and loads them. It erases the calibration (the
driver reports *Not calibrated*), clears the gripper flag, the heartbeat rate and the watchdog, sets the hardware
version to 1 and the batch date to 24092024, and stores 1111 as the serial number; from firmware 109 it also
clears the tool id, the watchdog fallback, the anti-cogging set, the encoder table and its zero trims, and sets
parameter 56 back to 0. The CAN node ID is kept from firmware 109 (it is 0 only when no valid ID is stored);
firmware 107 and older set it to 0. Note what the driver reports before you use it. The values are listed in the
[Defaults](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/defaults/) reference.

Use it before the first calibration of a motor, after a firmware update when the driver behaves oddly, and when
the state shows nonsense values (a `-1` where a number should be).

## The check at power-up

The configuration lives in an EEPROM chip on the board (a 24C16, 2 KB), apart from the firmware: flashing a new
firmware never touches it, and only the firmware's check at power-up decides to reset a part of it. Since
firmware 106 the saved configuration is in blocks, each with its own checksum; firmware 109 adds three:

| Block | Bytes | Checksum at | Holds |
|---|---|---|---|
| calibration | 60-188, reserved 204-228 | 200 | the motor's resistance, inductance, pole pairs, phase order, direction, angle offset, Kt, KV and the current loop gains |
| settings 1 | 44-180 | 196 | the other gains, the limits, the node ID, the watchdog, the heartbeat and the flags |
| settings 2 (109) | 260-312 | 256 | tool id, watchdog fallback, the product stamp, the calibration ID; reserved slots |
| anti-cogging (109) | 324-879 | 320 | the harmonics, the table, mode and scale |
| encoder table (109) | 884-1147 | 880 | the table, its on/off switch, parameter 56, the current-sense zero trims |

At power-up the driver checks each. A block that fails, after a power loss during a save for instance, is replaced
by its factory values without a message, and the others are kept: a failed settings block gives the default gains
and limits (from firmware 109 the node ID stays, if it was valid), a failed calibration block leaves the driver
*Not calibrated*. The new blocks need the chip's upper banks; on a smaller chip they keep their defaults in RAM
and are not saved, which `#Info` says (`Settings block 2: not available`, `block 3 not available`). Going back to an
older firmware is safe: the first two blocks are unchanged, and older firmware ignores everything from byte 256
on. [Upgrading from older firmware](https://docs.source-robotics.com/Spectral-BLDC-docs/109/07-firmware/upgrading/) says what changes when you update.

A board that comes from a release before 106 has no checksums yet: the driver keeps its values once and seals
them; from firmware 109 every board that was ever saved is trusted this way. A value that was already wrong (a
`-1` in `#Info`, for instance) then stays, and `#Default` with a new calibration is the fix. A blank EEPROM gets
the defaults.

## What the driver reports

`#Info` prints the identity and the motor: hardware version, batch date, firmware version, CAN ID, whether the
motor is calibrated, temperature, supply voltage, the phase order and direction, the pole pairs, resistance,
inductance, Kt and KV, and from firmware 109 the build, the board ID and the calibration ID, the tool id, the
watchdog, the EEPROM blocks and, at its end, what is in force. `#SERNUM` prints the serial number, `#Param` the gains and limits, `#Error` the active errors. They are
the first thing to look at when something is off, and the thing to copy into a bug report.
[Status and diagnostics](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/diagnostics/) explains the new lines.
