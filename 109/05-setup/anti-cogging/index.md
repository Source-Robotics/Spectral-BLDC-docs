# Encoder table and anti-cogging

Firmware 109 can measure two corrections on the drive itself, with nothing but the motor on the bench: the
**encoder table**, which corrects the small error of the encoder's angle reading, and the **anti-cogging**, a
current that cancels the motor's own torque ripple. The same routines run on the sister driver STEPFOC. From
firmware 109 they follow every `#Cal` by themselves; `#Calonly` is the calibration alone.

!!! note "Tested on a gimbal motor"
    On the Spectral Micro bench (gimbal motor, 2026-11-10) a full `#Cal` measured the encoder table (0.50° peak to
    peak) and identified the anti-cogging (6.8 mA rms), and saved both. Check the result as below before you keep it. When a
    run fails after a `#Cal` the calibration itself is still good: save it with `#Save`.

!!! danger "The motor turns"
    Each run turns the motor one revolution forward and one back, slowly. Keep the shaft free: nothing on it and
    nothing it could drive. A mechanism that cannot turn a whole revolution, a gripper's jaws for example, has to
    come off first.

## The encoder table

The magnetic encoder reads the shaft angle with a small error that changes slowly around the turn: the magnet is
never exactly on the axis, and the chip itself is not perfectly linear. On the STEPFOC bench motor it was 0.65°
peak to peak. The commutation multiplies it by the pole pairs: on an 11-pole-pair motor 0.65° becomes 7 electrical
degrees, which costs torque and makes the current uneven around the turn.

To measure it, the driver turns the field open loop, one shaft revolution forward and one back at 2048 ticks/s
(about 20 s), with a current of 80 % of the current limit holding the rotor to the field. At each 1/128 of a turn
it records how far the encoder's angle is from the field's. Forward and backward are averaged, so friction, which
pulls the rotor behind the field in each direction, cancels; only the harmonics 1 to 16 per turn are kept, which
leaves out the motor's own pull at higher orders. The result is a table of 128 corrections. From then on the
encoder reading is corrected with it, and the electrical offset is moved by the table's mean error, so the
commutation stays right. A check of the routine on a simulated 11-pole-pair motor at the Spectral Micro's loop
rate took the commutation error from 30 to 0.4 electrical degrees.

A table over 4° peak to peak, or one that would move the offset by more than 60 electrical degrees, is rejected
as implausible: the magnet is loose or far off its place.

## Anti-cogging

A motor's magnets pull towards the stator's teeth, and errors in the current measurement add a ripple once and
twice per electrical turn. At low speed both show as a ripple in the speed and the position. Anti-cogging adds a
current to the current setpoint that cancels it: a function of the electrical angle, added in velocity and
position modes.

To find it, the driver runs in velocity mode at 1500 ticks/s (parameter 44), records the current the velocity
loop asks for in 256 bins over the electrical angle for one motor revolution forward and one back, and averages
the two directions, each without its mean, so friction drops out. From that it keeps two forms of the same
correction:

- **harmonics** (parameter 37 = 1): the 8 largest of the harmonics 1 to 32 of the electrical angle, each
  a·cos(h·θ) + b·sin(h·θ) in mA;
- **table** (parameter 37 = 2): 256 values in mA over one electrical turn, interpolated between them.

The identification switches the harmonics on. Parameter 38 scales the correction from 0 to 200 % for
experiments; 100 % is as identified. The identification records the current the loops ask for, so it depends a
little on the gains: after a large change of the current or velocity gains, identify it again.

The STEPFOC firmware can also correct the current-sense zeros from the anti-cogging's once-per-turn part (the
**zero trim**, 43 = 4 or 5). The Spectral Micro firmware 109 skips that step until the map of its current channels
is measured: 4 and 5 identify like 1 and 2, and the trims (parameters 59 and 60) change only when written.

## Running them

The driver must be calibrated and without an error. Both runs keep the CAN watchdog fed while they go, end by
holding the position the shaft reached, and stop at once when a host sends a command (a motion command, Idle) or
an error comes up; nothing is saved then.

| What | UART | CAN: Send_Parameter |
|---|---|---|
| the encoder table, used at once | `#Encal` | 52 = 1 |
| the encoder table, used and saved | `#Encal save` | 52 = 2 |
| the encoder table, then the anti-cogging, then save all | `#Encal all` | 52 = 3, or 43 = 3 |
| the anti-cogging, switched on | `#Cogcal` | 43 = 1 |
| the anti-cogging, switched on and saved | `#Cogcal save` | 43 = 2 |
| stop a run | `#Encal stop`, `#Cogcal stop` | 52 = 0, 43 = 0 |

A save from a run is the whole configuration, as `#Save` writes it. After a change of the motor, the magnet or
its position, run the encoder table and the anti-cogging again, in that order, or calibrate again.

After `Calibration success!` of a `#Cal` the driver runs both by itself and saves everything when they succeed.

Two guards keep a correction from running on the wrong data: parameter 37 refuses 1 or 2 while no set is stored
for that form, and an encoder table measured on its own (52 = 1 or 2) switches an anti-cogging set from before
off, because that set was found on the uncorrected encoder; the anti-cogging state then reads 10 until it is
identified again.

## Checking them

`#Info` ends with what is in force:

```
In force:
  encoder table: on, error 0.61 deg p-p
  anti-cogging: on (harmonics), saved
  current-sense zero trim: 0 / 0 counts
  delay compensation: 234 us
  speed estimate: direct PLL, 100 Hz
  input filter: off; integral deadband: off
```

(here with an example encoder error). While a run goes, a line `running: encoder table` or
`running: anti-cogging identification` follows. `#Encal state` and `#Cogcal state` print one run's state without
starting it; parameter 43 gives the same state over CAN.

Over CAN the same is in the parameters (the [parameter table](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#every-parameter)):

| Parameter | What it tells |
|---|---|
| 52 | the encoder table's state: 3 done, 4 aborted, 5 error or not calibrated, 6 the rotor did not follow, 7 rejected |
| 54, 55 | the table's error peak to peak and its once-per-turn part, 0.01° of the shaft (on the STEPFOC bench 0.61-0.65°, two runs within 0.021°) |
| 57 | how far the last table moved the electrical offset, 0.1° electrical |
| 43 | the anti-cogging state: 3 done, 6 the shaft did not turn |
| 45 | the cogging current found, 0.1 mA rms |
| 79 | the bits of what is in force, see [What is in force](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#what-is-in-force-parameter-79) |

Send_Buffer_Read reads the corrections themselves: kind 4 the encoder table (128 values in 1/16 count), kind 2
the harmonics, kind 3 the anti-cogging table ([Respond_Buffer_Data](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#respond_buffer_data)).
A capture of the speed while the motor turns slowly, with the anti-cogging off and on
([Status and diagnostics](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/diagnostics/#a-capture)), shows whether it helps on your motor.

When a run fails:

| State | Cause | What to do |
|---|---|---|
| 52 = 6, 43 = 6 | the rotor did not follow: the shaft is blocked, or the current is too low to turn it | free the shaft; for the encoder table raise the current limit (it uses 80 % of it) |
| 52 = 5, 43 = 5 | the driver was in error or is not calibrated | `#Error`, clear it, calibrate |
| 52 = 4, 43 = 4 | a command came first | run it again and send nothing meanwhile |
| 52 = 7 | the table is implausible | check the magnet: glued, centred, at the right distance ([The encoder magnet](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/magnet/)), then calibrate |
| 43 = 8 | the encoder table of a combined run failed | parameter 52 says why |

## Switching them off

| | UART | CAN: Send_Parameter |
|---|---|---|
| the encoder table off / on | `#Encal off`, `#Encal on` | 53 = 0, 53 = 1 |
| the anti-cogging off, harmonics, table | — | 37 = 0, 1, 2 |
| how much of the anti-cogging | — | 38 = 0 to 200 (%) |

`#Save` keeps the switches with the corrections. `#Default` clears both corrections and the trims.
