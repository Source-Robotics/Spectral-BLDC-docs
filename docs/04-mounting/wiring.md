# Wiring the motor

A three-phase brushless motor has three wires. They go to the terminals **U, V and W** on the board (see
[Connectors and pinout](../03-technical-data/connectors.md)), in any order: calibration finds the order of the
phases. Firmware 105 and newer compensates it in software; firmware 101 asks you to swap two wires when it is
reversed.

## Soldering

1. Cut the leads to a comfortable length: long enough to reach the pads with the board mounted, short enough not
   to get into the rotor. With firmware older than 105, leave them long enough to swap two of them later.
2. Tin the leads and solder each to one group of pads, U, V or W. The three pads of a group are one terminal.
3. Make sure no strand bridges two groups and that nothing touches the rotor or the housing.

A motor that comes with a connector keeps it: solder a short lead with the mating connector to each pad group.

!!! success "Check"
    With the driver unpowered, a multimeter shows about the same resistance between U and V, V and W, and W
    and U, and no strand bridges two groups.

!!! warning
    Never connect or disconnect the motor while the driver is powered.

## Phase order and direction

Calibration spins the motor in open loop and watches the encoder, then checks that a current command moves the
rotor the expected way.

With firmware 105 and newer, the order of the phases is detected and compensated, so the motor calibrates identically
with any wiring, and positive commands turn the motor the same way whatever the wiring: counter-clockwise seen from
the encoder side of the board, see [Control modes](../06-operation/modes.md). To turn the other way, use negative
setpoints.

Firmware older than 105 does not compensate the order: calibration stops with
`Phase order is wrong! Switch motor phases and try again!`. Swap any two of U, V and W and calibrate again.

If the motor does not respond to the commutation check, calibration says so (`Commutation/alignment check
failed!`). That means a phase is not connected, `#Iqoffset` is set too low or the magnet slipped, not that the
wires are in the wrong order; see [Calibration](../05-setup/calibration.md).
