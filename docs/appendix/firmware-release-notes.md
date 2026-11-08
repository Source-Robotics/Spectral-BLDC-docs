# Firmware release notes

What changed in each firmware release, from the release notes in the firmware repository, up to the release this site describes.

!!! note "Release 108, not published yet"
    Its notes on GitHub come with the release; until then, a summary of what it brings over 107, each item with
    the page that describes it:

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
    - Calibration puts the current limit back when it ends, and can be followed by the runs of parameter 56
      ([Calibration](../05-setup/calibration.md)).
    - The product lock, the current-sense zero measured at start-up, no undervoltage error while the supply ramps up.
    - Sound through the motor: tones, a queue, samples; CAN 44 and 45, `#Tone` ([Sound](../06-operation/sound.md)).
    Not yet tested on a Spectral Micro: the encoder table, the anti-cogging, the PLL speed estimate, the
    160 Hz current loop, the delay compensation and the sound.

    [Upgrading from older firmware](../07-firmware/upgrading.md) says what a driver keeps and what to run.

--8<-- "generated/firmware_release_notes.md"
