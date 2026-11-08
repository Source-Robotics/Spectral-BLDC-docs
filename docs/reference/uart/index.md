# UART commands

Every command the firmware release this site describes understands over the serial port. The kind, the argument
type, the mode a command enters and what it prints are read from the firmware; the descriptions are written by
hand. [Over UART](../../06-operation/uart.md) explains the protocol.

## Syntax

```
#<Name> [number]
```

- A **Set/Get** command sets the value when a number follows and prints the current value either way.
- A **Get** command only prints.
- An **Action** command does something; a number after it is ignored.
- Names are case-sensitive, at most 19 characters; the argument is one word of at most 19 characters, without
  spaces, so a list is written with commas (`#WdFb 2000,0,1000,2`, `#Par 56,0`); firmware 107 and older allowed 20
  characters for name and number together. The line ends with LF (CR before it is
  fine). 256000 baud, 8N1, 3.3 V.
- A name the firmware does not know is answered `Unknown command`.

## Every command

<!-- uart-overview -->

## By group

- [Motion](motion.md): setpoints and modes
- [Gains and limits](gains.md): the loop gains, the limits, the integrator reset, the current loop bandwidth
- [Calibration and motor parameters](calibration.md): `Cal` and `Calonly`, the motor's R, L and pole pairs, the constants calibration finds, the calibration settings, the encoder table (`Encal`) and the anti-cogging (`Cogcal`)
- [Status and utility](utility.md): save, reset, defaults, identity, errors, temperature, the cyclic output, any parameter (`Par`), the tool id, the watchdog fallback, the product lock
- [Gripper](gripper.md): gripper mode
