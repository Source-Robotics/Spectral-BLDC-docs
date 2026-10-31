# UART commands

Every command the firmware release this site describes understands over the serial port. The kind, the argument
type, the mode a command enters and what it prints are read from the firmware; the descriptions are written by
hand. [Over UART](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/uart/) explains the protocol.

## Syntax

```
#<Name> [number]
```

- A **Set/Get** command sets the value when a number follows and prints the current value either way.
- A **Get** command only prints.
- An **Action** command does something; a number after it is ignored.
- Names are case-sensitive, at most 19 characters; the number at most 19; the line ends with LF (CR before it is
  fine). 256000 baud, 8N1, 3.3 V.
- A name the parser does not know is answered `Unknown command`.

## Every command

| Command | Kind | Argument | Group |
|---|---|---|---|
| [`#Activate`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Action |  | Status and utility |
| [`#Brake`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#Cal`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Action |  | Calibration and motor parameters |
| [`#Calibrated`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |
| [`#Calpwr`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#CANID`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Cbw`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Clear`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Action |  | Status and utility |
| [`#Close`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Action |  | Motion |
| [`#Cyc`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Cyca`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Default`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Action |  | Status and utility |
| [`#Dir`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |
| [`#Error`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#Flux`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#Gripact`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Set/Get | int | Gripper |
| [`#Gripcal`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Action |  | Gripper |
| [`#Gripcur`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Set/Get | int | Gripper |
| [`#Gripinfo`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Get |  | Gripper |
| [`#Gripper`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Set/Get | int | Gripper |
| [`#Grippos`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Set/Get | int | Gripper |
| [`#Gripstop`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Set/Get | int | Gripper |
| [`#Gripvel`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/) | Set/Get | int | Gripper |
| [`#Help`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Action |  | Status and utility |
| [`#Iabc`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#Id`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | float | Motion |
| [`#Idle`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Action |  | Motion |
| [`#Ilim`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | int | Gains and limits |
| [`#Info`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#Iq`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | float | Motion |
| [`#Iqoffset`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |
| [`#KD`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kiid`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kiiq`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kiv`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#KP`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kpid`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kpiq`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kpp`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kpv`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | float | Gains and limits |
| [`#Kt`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#KV`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#L`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#LED`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Magnet`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Get |  | Calibration and motor parameters |
| [`#Mode`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#Offset`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#Openloop`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | float | Motion |
| [`#Opens`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#Openv`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |
| [`#P`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#Param`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#PD`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#PDI`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#PDV`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#Phase`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Get |  | Calibration and motor parameters |
| [`#PP`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |
| [`#Pullconfig`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#PWM`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#R`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | float | Calibration and motor parameters |
| [`#Reset`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Action |  | Status and utility |
| [`#Resv`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |
| [`#Rstint`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | int | Gains and limits |
| [`#Save`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Action |  | Status and utility |
| [`#SERNUM`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Temp`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#Term`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Tlim`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Ud`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#Uq`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#V`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/) | Set/Get | int | Motion |
| [`#Vbus`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Get |  | Status and utility |
| [`#Vlim`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | int | Gains and limits |
| [`#Vlimit`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/) | Set/Get | int | Gains and limits |
| [`#Vmax`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/) | Set/Get | int | Status and utility |
| [`#Vp`](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/) | Set/Get | int | Calibration and motor parameters |

The parser also accepts `#Calangle`, `#EN`, `#SIN`, `#SPWM`, `#Vmin`, `#flux`, `#zz`, which have no handler: the driver answers nothing to them.

## By group

- [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/motion/): setpoints and modes
- [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gains/): the loop gains, the limits, the integrator reset, the current loop bandwidth
- [Calibration and motor parameters](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/calibration/): `Cal`, the motor's R, L and pole pairs, the constants calibration finds, the calibration settings
- [Status and utility](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/utility/): save, reset, defaults, identity, errors, temperature, the cyclic output
- [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/gripper/): gripper mode
