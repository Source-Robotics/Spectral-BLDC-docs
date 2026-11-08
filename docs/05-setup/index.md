# First setup

From a mounted and wired driver to a calibrated, tuned motor. Motor GUI in the browser is the usual tool for it;
every step also gives the terminal command, for a terminal or for the console in Motor GUI.

1. [Motor GUI](motor-gui.md): the browser, the serial adapter, opening the port, what is on the screen.
2. [The serial terminal](terminal.md): the alternative — PuTTY, the PlatformIO monitor or the Arduino monitor,
   and the `#` commands.
3. [Calibration](calibration.md): the factory defaults, then the run that measures the motor and finds its pole
   pairs, phase order and constants.
4. [Encoder table and anti-cogging](anti-cogging.md): two corrections the driver can measure on itself after a
   calibration, how to run them and how to check them.
5. [Current limit and loop tuning](tuning.md): the current limit for the motor, the loop gains if the defaults do
   not suit it, the speed estimate and the delay compensation.
6. [Saving the configuration](saving.md): nothing survives a power cycle until it is saved; where it is kept.

A driver that has been through these pages is ready for [Operation](../06-operation/index.md). The
[Quick start](../quick-start.md) is the same path on one page.
