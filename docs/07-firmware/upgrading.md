---
status: new
---

# Upgrading from older firmware

Firmware 109 adds more to the Spectral Micro than any release before it: parameters, the watchdog actions, the
identity and telemetry frames, captures, the current loop from one bandwidth, a choice of speed estimates, and the
encoder table and anti-cogging.

This page says what a driver keeps when it is updated to 109, what works at once, what can be run, and how to go back.
[Updating through the bootloader](update.md) is how to flash it.

There is no firmware 108 for the Spectral Micro: from 109 the Spectral Micro and STEPFOC share their version
numbers, so a Spectral Micro goes from 107 straight to 109.

## What is kept

Flashing never touches the EEPROM, where the configuration lives
([The check at power-up](../05-setup/saving.md#the-check-at-power-up)). A driver updated from 106 or 107 starts
with everything it had:

- the calibration: pole pairs, R, L, the angle offset, Kt, KV, the phase order and direction, the current gains;
- the CAN ID, the gains, the limits, the watchdog, the heartbeat, the thermistor and the gripper settings.

!!! warning "Calibrate again after the update, where the motor can turn freely"
    In every firmware before 109 the enable input of phase B was fed by a clock signal instead of a steady level,
    so phase B could drop out, also while the calibration measured the motor. A calibration made with 107 or older
    stored the resistance about 10 % and the inductance about 45 % too low (reference gimbal motor: about 6.4 Ω and
    1.25 mH, where 109 measures about 7.0 to 7.2 Ω and 1.75 to 1.9 mH).

    The driver keeps running on such a calibration: on the bench an SSG-48 updated to 109 without a new
    calibration reached every target and gripped as before. Only the current gains are computed from the low
    values. So:

    - **A motor that can turn freely:** run `#Cal` once after the update. The current gains then follow the true
      values, and the encoder table and the anti-cogging are measured too.
    - **An assembled SSG-48 gripper,** whose motor moves the jaws: do not run `#Cal`. Apply Motor GUI's SSG-48
      preset over UART instead: it writes 300 Hz current gains for the gripper's motor and saves. Set *Gripper CAN
      ID* to the gripper's node first: it starts at 6, the PAR6 gripper's; a PAROL6 gripper is node 0. A motor
      calibration needs the body opened and the linear guide with the jaws off; then use `#Calonly`, because
      `#Cal` also runs the encoder table and the anti-cogging.

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
- phase B's enable pin is driven properly, and the control loop keeps the gate driver awake in every driving
  mode: either could leave a motor that took a command and did not move, or that pushed unevenly;
- the limits refuse a negative value, and Send_Limits and the gripper's current stop at 2800 mA;
- setting the watchdog time starts a fresh window, so switching it on again no longer trips it at once;
- `#Default` and a settings reset **keep the CAN ID**;
- the first motion frame after Idle is followed (the driver's wake-up now comes with it), and a position or speed
  frame after another mode no longer kicks with a stale velocity integral;
- the product lock, the new CAN commands and parameters, the identity frame, telemetry, the capture, `#Info`'s
  `In force:`, and [sound through the motor](../06-operation/sound.md) (not yet tested on a Spectral Micro).

## What can be run or switched on

The encoder table and the anti-cogging are off after the update until they are measured (`#Cal` measures both);
the speed estimate and the delay compensation are new defaults, on from the first start:

- the **encoder table** and the **anti-cogging** ([Encoder table and anti-cogging](../05-setup/anti-cogging.md));
  they cannot be switched on before they are measured;
- the **direct PLL speed estimate** at 100 Hz (parameters 50 and 51) and the **commutation delay compensation** of
  234 µs (parameter 64), both on by default from 109
  ([Current limit and loop tuning](../05-setup/tuning.md#the-speed-estimate)). They change how the velocity loop
  behaves with the gains you had: a speed step overshoots less. Check your velocity gains after the update.

## What does not change by itself

- **The current gains.** The saved Kpiq and Kiiq stay as they are: on a driver calibrated before 109 they were
  computed for 500 Hz (parameter 49 reads about 500), from a resistance and an inductance that were too low. A
  calibration with 109 measures both again and computes the gains at 160 Hz. `#Cbw 160` on the old calibration
  does not replace it: it uses the old values and gives gains for a lower bandwidth than it names. 160 Hz is the
  new default; it was chosen on the STEPFOC bench.
- **The velocity gains** stay as they are; their defaults, Kpv 0.03 and Kiv 0.0003, did not change.

## The whole upgrade

1. Flash 109 ([Updating through the bootloader](update.md)). `#Info` prints the new firmware version and ends with
   `In force:`.
2. Check that the current limit suits your motor (`#Ilim`): calibration puts back the limit that was in force, and
   the encoder table in the next step runs at 80 % of it.
3. Calibrate, with the shaft free: `#Cal`, so that the resistance, the inductance and the current gains are
   measured again. It goes on to the encoder table and the anti-cogging, and saves everything. `#Calonly` is the
   calibration alone.
4. After `#Calonly`: `#Save`; and if you want them, run the encoder table and the anti-cogging with the shaft free
   (`#Encal all`) and check them.

With Motor GUI's presets: apply the preset first, then calibrate. A product preset writes its own current and
velocity gains, so one applied after the calibration puts its current gains back. The *Generic motor* presets set
soft limits and velocity gains and leave the current gains to `#Cbw` and the calibration.

## Going back

Flashing 107 or older over 109 is safe for the configuration: the calibration and the first settings block are
unchanged, and older firmware ignores everything 109 saved from byte 256 on (tool id, fallback, anti-cogging,
encoder table). Flash 109 again and they are all still there.

!!! note "Not yet tested on the bench"
    A downgrade and the sound on a Spectral Micro had not been tested on the bench when this page was written;
    the rest of this page was.
