# UART commands

Every command the firmware release this site describes understands over the serial port. The kind, the argument
type, the mode a command enters and what it prints are read from the firmware; the descriptions are written by
hand. [Over UART](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/uart/) explains the protocol.

## Syntax

```
#<Name> [number]
```

- A **Set/Get** command sets the value when a number follows and prints the current value either way.
- A **Get** command only prints.
- An **Action** command does something; a number after it is ignored.
- Names are case-sensitive, at most 19 characters; the argument is one word of at most 19 characters, without
  spaces, so a list is written with commas (`#WdFb 2000,0,1000,2`, `#Par 1,200`); firmware 107 and older allowed 20
  characters for name and number together. The line ends with LF (CR before it is
  fine). 256000 baud, 8N1, 3.3 V.
- A name the firmware does not know is answered `Unknown command`.

## Every command

<div class="ref-table overview" markdown>

| Command | Kind | Argument | Group |
|---|---|---|---|
| [`#Activate`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#activate) | Action |  | Status and utility |
| [`#Brake`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#brake) | Get |  | Motion |
| [`#Cal`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#cal) | Action |  | Calibration and motor parameters |
| [`#Calibrated`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#calibrated) | Set/Get | int | Calibration and motor parameters |
| [`#Calonly`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#calonly) | Action |  | Calibration and motor parameters |
| [`#Calpwr`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#calpwr) | Set/Get | float | Calibration and motor parameters |
| [`#CANID`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#canid) | Set/Get | int | Status and utility |
| [`#Cbw`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#cbw) | Set/Get | float | Gains and limits |
| [`#Clear`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#clear) | Action |  | Status and utility |
| [`#Close`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#close) | Action |  | Motion |
| [`#Cogcal`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#cogcal) | Set/Get |  | Calibration and motor parameters |
| [`#Cyc`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#cyc) | Set/Get | int | Status and utility |
| [`#Cyca`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#cyca) | Set/Get | int | Status and utility |
| [`#Default`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#default) | Action |  | Status and utility |
| [`#Dir`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#dir) | Set/Get | int | Calibration and motor parameters |
| [`#Encal`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#encal) | Set/Get |  | Calibration and motor parameters |
| [`#Error`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#error) | Get |  | Status and utility |
| [`#Flux`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#flux) | Set/Get | float | Calibration and motor parameters |
| [`#Gripact`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripact) | Set/Get | int | Gripper |
| [`#Gripcal`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripcal) | Action |  | Gripper |
| [`#Gripcur`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripcur) | Set/Get | int | Gripper |
| [`#Gripinfo`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripinfo) | Get |  | Gripper |
| [`#Gripper`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripper) | Set/Get | int | Gripper |
| [`#Grippos`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#grippos) | Set/Get | int | Gripper |
| [`#Gripstop`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripstop) | Set/Get | int | Gripper |
| [`#Gripvel`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/#gripvel) | Set/Get | int | Gripper |
| [`#Help`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#help) | Action |  | Status and utility |
| [`#Iabc`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#iabc) | Get |  | Status and utility |
| [`#Id`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#id) | Set/Get | float | Motion |
| [`#Idle`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#idle) | Action |  | Motion |
| [`#Ilim`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#ilim) | Set/Get | int | Gains and limits |
| [`#Info`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#info) | Action |  | Status and utility |
| [`#Iq`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#iq) | Set/Get | float | Motion |
| [`#Iqoffset`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#iqoffset) | Set/Get | int | Calibration and motor parameters |
| [`#KD`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kd) | Set/Get | float | Gains and limits |
| [`#Kiid`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kiid) | Set/Get | float | Gains and limits |
| [`#Kiiq`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kiiq) | Set/Get | float | Gains and limits |
| [`#Kiv`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kiv) | Set/Get | float | Gains and limits |
| [`#KP`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kp) | Set/Get | float | Gains and limits |
| [`#Kpid`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kpid) | Set/Get | float | Gains and limits |
| [`#Kpiq`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kpiq) | Set/Get | float | Gains and limits |
| [`#Kpp`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kpp) | Set/Get | float | Gains and limits |
| [`#Kpv`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#kpv) | Set/Get | float | Gains and limits |
| [`#Kt`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#kt) | Set/Get | float | Calibration and motor parameters |
| [`#KV`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#kv) | Set/Get | float | Calibration and motor parameters |
| [`#L`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#l) | Set/Get | float | Calibration and motor parameters |
| [`#LED`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#led) | Set/Get | int | Status and utility |
| [`#Magnet`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#magnet) | Get |  | Calibration and motor parameters |
| [`#Mode`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#mode) | Get |  | Status and utility |
| [`#Offset`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#offset) | Set/Get | float | Calibration and motor parameters |
| [`#Openloop`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#openloop) | Set/Get | float | Motion |
| [`#Opens`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#opens) | Set/Get | float | Calibration and motor parameters |
| [`#Openv`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#openv) | Set/Get | int | Calibration and motor parameters |
| [`#P`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#p) | Set/Get | int | Motion |
| [`#Par`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#par) | Set/Get | int | Status and utility |
| [`#Param`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#param) | Get |  | Status and utility |
| [`#PD`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#pd) | Set/Get | int | Motion |
| [`#PDI`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#pdi) | Set/Get | int | Motion |
| [`#PDV`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#pdv) | Set/Get | int | Motion |
| [`#Phase`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#phase) | Get |  | Calibration and motor parameters |
| [`#PP`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#pp) | Set/Get | int | Calibration and motor parameters |
| [`#Product`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#product) | Action |  | Status and utility |
| [`#Pullconfig`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#pullconfig) | Get |  | Status and utility |
| [`#PWM`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#pwm) | Get |  | Status and utility |
| [`#R`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#r) | Set/Get | float | Calibration and motor parameters |
| [`#Reset`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#reset) | Action |  | Status and utility |
| [`#Resv`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#resv) | Set/Get | int | Calibration and motor parameters |
| [`#Rstint`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#rstint) | Set/Get | int | Gains and limits |
| [`#Save`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#save) | Action |  | Status and utility |
| [`#SERNUM`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#sernum) | Set/Get | int | Status and utility |
| [`#Temp`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#temp) | Get |  | Status and utility |
| [`#Term`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#term) | Set/Get | int | Status and utility |
| [`#Tlim`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#tlim) | Set/Get | int | Status and utility |
| [`#Tone`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#tone) | Set/Get |  | Status and utility |
| [`#Tool`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#tool) | Set/Get | int | Status and utility |
| [`#Ud`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#ud) | Set/Get | int | Motion |
| [`#Uq`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#uq) | Set/Get | int | Motion |
| [`#V`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/#v) | Set/Get | int | Motion |
| [`#Vbus`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#vbus) | Get |  | Status and utility |
| [`#Vlim`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#vlim) | Set/Get | int | Gains and limits |
| [`#Vlimit`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/#vlimit) | Set/Get | int | Gains and limits |
| [`#Vmax`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#vmax) | Set/Get | int | Status and utility |
| [`#Vp`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/#vp) | Set/Get | int | Calibration and motor parameters |
| [`#WdFb`](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/#wdfb) | Set/Get | int list | Status and utility |

</div>

## By group

- [Motion](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/motion/): setpoints and modes
- [Gains and limits](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gains/): the loop gains, the limits, the integrator reset, the current loop bandwidth
- [Calibration and motor parameters](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/calibration/): `Cal` and `Calonly`, the motor's R, L and pole pairs, the constants calibration finds, the calibration settings, the encoder table (`Encal`) and the anti-cogging (`Cogcal`)
- [Status and utility](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/): save, reset, defaults, identity, errors, temperature, the cyclic output, any parameter (`Par`), the tool id, the watchdog fallback, the product lock
- [Gripper](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/gripper/): gripper mode
