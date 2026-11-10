# Firmware release notes

What changed in each firmware release, from the release notes in the firmware repository, up to the release this site describes.

!!! note "Release 109, not published yet"
    There is no release 108 for the Spectral Micro: from 109 it shares its version numbers with STEPFOC, and goes
    from 107 straight to 109. The notes on GitHub come with the release; until then, a summary of what it brings
    over 107, each item with the page that describes it:

    - Settings in blocks with their own checksums; a reset keeps the CAN ID; flashing never touches them
      ([Saving the configuration](../05-setup/saving.md)).
    - Parameters: any setting by number over CAN (36-38) or `#Par`; identity (39) and telemetry (40); captures,
      a histogram and buffers (41-43) ([Parameters and buffers](../reference/can/parameters.md),
      [Status and diagnostics](../06-operation/diagnostics.md)).
    - The watchdog's actions: hold, brake, coast, descend ([The watchdog](../06-operation/watchdog.md)).
    - The current loop from R, L and one bandwidth, 160 Hz; a choice of speed estimates; commutation delay
      compensation; the position input filter and the velocity-integral deadband
      ([Current limit and loop tuning](../05-setup/tuning.md)).
    - The encoder table and anti-cogging measured on the drive ([Encoder table and anti-cogging](../05-setup/anti-cogging.md)).
    - Calibration puts the current limit back when it ends; `#Cal` goes on to the encoder table and anti-cogging, `#Calonly` is the calibration alone
      ([Calibration](../05-setup/calibration.md)).
    - The product lock, the current-sense zero measured at start-up, no undervoltage error while the supply ramps up.
    - Sound through the motor: tones, a queue, samples; CAN 44 and 45, `#Tone` ([Sound](../06-operation/sound.md)).

    Fixed in 109:

    - **Phase B's enable pin.** In every earlier firmware the enable input of phase B was fed by a clock signal
      instead of a steady level: the pin doubled as the microcontroller's clock output. Phase B could drop out:
      weaker or uneven torque, a calibration that failed with a wrong pole-pair count, or a motor that took a
      current command and did not move. 109 drives the pin properly. Calibrate again after updating (`#Cal`)
      where the motor can turn freely; an assembled SSG-48 keeps its calibration and gets the SSG-48 preset.
      The calibration now reports the true phase resistance and inductance (reference gimbal motor: about 7.0 to
      7.2 Ω and 1.75 to 1.9 mH, where 107 reported about 6.4 Ω and 1.25 mH). The old × 1.25 correction of the
      resistance is gone, and the current gains follow the new values
      ([Upgrading from older firmware](../07-firmware/upgrading.md)).
    - **No torque without an error.** The control loop itself keeps the gate driver awake in every driving mode.
      Before, a command that arrived at the wrong moment (a CAN current or PD frame, a UART command) could leave
      the driver asleep, with no error, until the next idle.
    - **Calibration.** The resistance and inductance steps average both current sensors. An inductance that gives
      no usable gains fails the calibration; it used to hang. Pole pairs from 1 to 49 are accepted, by the
      calibration, by parameter 78 and by `#PP` (only while idle); a rotor that
      does not follow the open-loop field ends with `Open loop: Failed`. The gate driver stays awake for the whole
      calibration; before, one could fail at once with `Resistance test: Failed`. A failed calibration switches
      the bridge off at once and enables all three phases again. An E-stop ends a calibration, and `#Cal` is not started while one is latched (`#Clear` first). Calibrating many
      times without a power cycle no longer uses up memory.
    - **After `#Cal`.** If a host takes the drive within 3 s, the encoder-table and anti-cogging runs are dropped;
      they used to wait and start at the next idle. `#Encal` and `#Cogcal` start a run only with no argument or
      with `save`, `all` (`#Encal`) or `trim` (`#Cogcal`); any other word only prints the state. `#Cogcal stop`,
      parameter 43 = 0 and parameter 52 = 0 stop a combined run in either part. While a run turns the motor, a
      capture is not armed and the histogram's source cannot be changed. The anti-cogging run's speed stays
      within the velocity limit. The encoder run's time limit fits motors with 1 to 3 pole pairs.
    - **CAN motion frames.** A current or PD frame sets its setpoint and its mode together; a control loop in
      between could overwrite the new current setpoint.
    - **Limits.** `#Ilim` and `#Vlimit` take the magnitude of a negative number. Send_Limits ignores a negative
      value or one that is not a number, and stops the current limit at 2800 mA. The gripper's current is kept
      within 0 to 2800 mA. The older CAN gain frames ignore a negative value or one that is not a number.
      Send_Voltage_Limit takes 0 to 60000 mV, as parameter 17 does, and ignores anything else.
    - **Watchdog.** Setting the time starts a fresh window: switching it on again no longer trips it at once. A
      negative time means off. A save over CAN no longer counts as silence.
    - **Storage.** A block whose check fails is read up to three times before its defaults are used. `#Info` and
      the status flags say the anti-cogging is saved only while what is in RAM equals what is stored.
    - **CAN.** A frame with a length code above 8 is treated as 8 bytes. Extended (29-bit) frames are ignored.
    - **Gripper: a poll right after a move.** A gripper poll (the empty gripper frame) sent right after a new
      move command could cancel it as new: the move then ran from the previous move's "at position", and the
      gripper reported object detection 3 (at position) while it pressed on an object. A repeat of the same
      command did the same. Now only a new command marks itself; the gripper reports 1 or 2 on contact as
      intended (bench, SSG-48: 1 on a soft and on a hard object). The same in every release before 109.
    - **Current-sense zero without the motor supply.** A driver started on USB before its supply measured the zero
      without the supply: about 60 counts (100 mA) off, and nothing said so. It now waits for the supply, uses 2048
      until it comes, says so in `#Info`, and measures the zero by itself once the supply is there.
    - **Control.** The current-loop integrals are cleared whenever the drive is idle, braking or coasting. PWM
      duties are kept between 0 and 100 %; a tone on top of a saturated output could turn a phase fully on. The
      watchdog's hold and descend no longer use the delay compensation of the last moving loop.
    - **Sound.** The note queue and the sample buffer no longer replay old content after a stop. A pitch the drive
      cannot play answers `Tone: not played`.
    - **`#Error`** prints `FAULT pin is LOW: the gate driver reports a fault`; the old text said HIGH.

    Not yet tested on a Spectral Micro: the sound.

    [Upgrading from older firmware](../07-firmware/upgrading.md) says what a driver keeps and what to run.

--8<-- "generated/firmware_release_notes.md"
