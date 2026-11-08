---
status: new
---

# Upgrading from older firmware

Firmware 109 adds more to the Spectral Micro than any release before it: parameters, the watchdog actions, the
identity and telemetry frames, captures, the current loop from one bandwidth, a choice of speed estimates, and the
encoder table and anti-cogging. This page says what a driver keeps when it is updated to 109, what works at once,
what can be run, and how to go back. [Updating through the bootloader](update.md) is how to flash it.

There is no firmware 108 for the Spectral Micro: from 109 the Spectral Micro and STEPFOC share their version
numbers, so a Spectral Micro goes from 107 straight to 109.

## What is kept

Flashing never touches the EEPROM, where the configuration lives
([The check at power-up](../05-setup/saving.md#the-check-at-power-up)). A driver updated from 106 or 107 starts
with everything it had:

- the calibration: pole pairs, R, L, the angle offset, Kt, KV, the phase order and direction, the current gains;
- the CAN ID, the gains, the limits, the watchdog, the heartbeat, the thermistor and the gripper settings.

A driver from 101 to 105, saved before the configuration had checksums, is trusted and sealed at its first start
of 109 when it was ever saved; a blank EEPROM gets the defaults. Release 101 and older from the `main` branch have
no bootloader: such a board needs the programming adapter once
([Installing the bootloader on an older board](bootloader.md)).

The new settings start from their defaults: tool id 0, the watchdog fallback 2000 ms / 0 mA / 1000 ticks/s /
legacy, parameter 56 = 0.

## What works at once

These need no measurement and are on from the first start of 109:

- the **current-sense zero**, measured at every start-up with the driver asleep: on the bench the current read
  3.9 mA with nothing flowing, where it read −20 to +19 mA before, depending on the rotor's position;
- undervoltage is not checked for the first 500 ms after power-up, so a supply that ramps up slowly no longer
  leaves a Vbus error behind (overvoltage always is);
- the **watchdog actions**: the action byte the host already sends is acted on. Byte 0, what the Python library and
  the PAR6 runtime send, gives the legacy response, so an unchanged host sees no difference;
- `#Default` and a settings reset **keep the CAN ID**;
- the first motion frame after Idle is followed (the driver's wake-up now comes with it), and a position or speed
  frame after another mode no longer kicks with a stale velocity integral;
- the product lock, the new CAN commands and parameters, the identity frame, telemetry, the capture, `#Info`'s
  `In force:`, and [sound through the motor](../06-operation/sound.md) (not yet tested on a Spectral Micro).

## What can be run or switched on

These are off after the update, and on the Spectral Micro they stay off until you choose them, because they are
not yet tested on its bench:

- the **encoder table** and the **anti-cogging** ([Encoder table and anti-cogging](../05-setup/anti-cogging.md));
  they cannot be switched on before they are measured;
- the **PLL speed estimate** (parameter 50; the moving average stays the default) and the **commutation delay
  compensation** (parameter 64, off) ([Current limit and loop tuning](../05-setup/tuning.md#the-speed-estimate)).

## What does not change by itself

- **The current gains.** The saved Kpiq and Kiiq stay as they are: on a driver calibrated before 109 they were
  computed for 500 Hz (parameter 49 reads about 500). A calibration computes them again at 160 Hz; so does
  `#Cbw 160` (or parameter 49 = 160), then `#Save`. 160 Hz is the new default; it was chosen on the STEPFOC bench.
- **The velocity gains** stay as they are; their defaults, Kpv 0.03 and Kiv 0.0003, did not change.

## The whole upgrade

1. Flash 109 ([Updating through the bootloader](update.md)). `#Info` prints the new firmware version and ends with
   `In force:`.
2. Calibrate, with the shaft free: `#Cal`, so that the current gains come from the new formula; or keep the
   calibration and send `#Cbw 160`.
3. Check that the current limit suits your motor (`#Ilim`; calibration puts back the limit that was in force),
   then `#Save`.
4. If you want them, run the encoder table and the anti-cogging with the shaft free (`#Encal all`) and check them.

With Motor GUI's presets: apply the preset first, then calibrate. A preset writes its own current and velocity
gains, so a preset applied after the calibration puts its current gains back.

## Going back

Flashing 107 or older over 109 is safe for the configuration: the calibration and the first settings block are
unchanged, and older firmware ignores everything 109 saved from byte 256 on (tool id, fallback, anti-cogging,
encoder table). Flash 109 again and they are all still there.

!!! note "Not yet tested on the bench"
    A downgrade, and the encoder table, the anti-cogging, the PLL speed estimate, the 160 Hz current loop, the
    delay compensation and the sound on a Spectral Micro, had not been tested on the bench when this page was
    written. The
    identity, settings block 2, the watchdog actions, the current-sense zero, the Vbus start-up grace, the product
    lock, the capture and `#Default` keeping the CAN ID were.
