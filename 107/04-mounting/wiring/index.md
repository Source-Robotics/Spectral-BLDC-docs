# Wiring the motor

A three-phase brushless motor has three wires. They go to the terminals **U, V and W** on the board (Figure 2 in
[Connectors and pinout](https://docs.source-robotics.com/Spectral-BLDC-docs/107/03-technical-data/connectors/)), in any order: calibration finds the order of the
phases. Firmware 105 and newer compensates it in software; firmware 101 asks you to swap two wires when it is
reversed.

## Soldering

1. Cut the leads to a comfortable length: long enough to reach the pads with the board mounted, short enough not
   to get into the rotor.
2. Tin the leads and solder each to one group of pads, U, V or W. The three pads of a group are one terminal.
3. Make sure no strand bridges two groups and that nothing touches the rotor or the housing.

A motor that comes with a connector keeps it: solder a short lead with the mating connector to each pad group.

!!! warning
    Never connect or disconnect the motor while the driver is powered.

## Phase order and direction

Calibration spins the motor in open loop and watches the encoder, then checks that a current command moves the
rotor the expected way. With firmware 105 and newer, the order of the phases is detected and compensated, so the
motor calibrates identically with any wiring, and positive commands turn the motor the same way whatever the
wiring: counter-clockwise seen from the encoder side of the board, see [Control modes](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/modes/).
To turn the other way, use negative setpoints.

If the motor does not respond to the commutation check, calibration says so (`Commutation/alignment check
failed!`). That means a phase is not connected, the current limit is 0 or the magnet slipped, not that the wires
are in the wrong order; see [Calibration](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/calibration/).
