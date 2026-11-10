# Parameters and buffers

From firmware 109 a setting that has no command of its own is a **parameter**: a number from 1 to 89 behind one
pair of commands, Send_Parameter (ID 36) to set it and Send_Get_Parameter (ID 37) to read it, answered with
Respond_Parameter (ID 38). The identifier has room for only 64 command IDs, so new settings no longer use them up.
Parameter numbers are permanent: a number is never given a new meaning. Number 73 is not used and stays free.
Parameters 84 to 87 are read only and say which build and which board answer: the git commit the firmware was
built from (84), its build time in Unix seconds (85), the board ID (86) and the calibration ID (87). `#Info` prints
them as `Build`, `Board ID` and `Calibration ID` ([Status and diagnostics](../../06-operation/diagnostics.md)).
Parameters 88 and 89, a diagnostic of when the current sensors are read, are the Spectral Micro's own; STEPFOC
does not have them.

The **buffers** are the larger data a drive holds: a capture of three signals, a histogram, the anti-cogging set
and the encoder table. Send_Buffer_Read (ID 41) reads them in 8-byte frames, Respond_Buffer_Data (ID 42) carries
them, and Send_Buffer_Write (ID 43) writes the anti-cogging set.

Over UART, `#Par` does the same: `#Par` lists every parameter, `#Par 1` reads one, `#Par 1,200` sets it
([Status and utility](../uart/utility.md)).

## Setting and reading a parameter

A set is not answered: read the value back to know what the driver took. A value outside a parameter's range is
clamped, replaced or refused, as the table says, and a read-only number ignores the write.

```python
import Spectral_BLDC as Spectral

comms = Spectral.CanCommunication(bustype='slcan', channel='COM41', bitrate=1000000)
motor = Spectral.SpectralCAN(node_id=0, communication=comms)

motor.Send_Parameter(1, 200)               # tool id 200, a custom tool
motor.Send_Get_Parameter(1)                # read it back
message, ids = comms.receive_can_messages(timeout=0.1)
if message is not None:
    motor.UnpackData(message, ids)
print(motor.parameters.get(1))
motor.Send_Save_config()                   # keep it over a power cycle
```

`Send_Parameter`, `Send_Get_Parameter` and the buffer calls need the Spectral-BLDC library 1.21 or newer.
`Send_Parameter` takes the value itself: a gain or a limit (8 to 16 and 20) is sent as a float, so
`motor.Send_Parameter(16, 1500)` sets a current limit of 1500 mA; every other parameter takes a whole number.

## The commands

<!-- can-commands: parameters -->

## Every parameter

The number and the name are read from the firmware; the rest is checked against its source. *Access*: a read-only
parameter ignores a write; a run parameter starts or stops a run when written and gives its state when read.

<!-- can-parameters -->

## What is in force: parameter 79

Parameter 79 says in one read what the drive runs with. `#Info` prints the same at its end, under `In force:`.
Bit 0 is the least significant.

| Bit | Set when |
|---|---|
| 0 | the motor is calibrated |
| 1 | an encoder table is measured (in RAM) |
| 2 | the encoder table is in use (parameter 53) |
| 3 | an anti-cogging set is in RAM (harmonics or table) |
| 4 | anti-cogging is on (parameter 37 not 0) |
| 5 | anti-cogging is on as the table (otherwise as the harmonics) |
| 6 | the anti-cogging set in RAM is the one saved in the EEPROM |
| 7 | a current-sense zero trim is applied (parameter 59 or 60 not 0) |
| 8 | the current-sense zero measured with the bridge switching is in use (parameter 46) |
| 9 | commutation delay compensation is on (parameter 64 not 0) |
| 10 | the speed estimate is a PLL (parameter 50 is 1 or 2) |
| 11, 12 | 0 on the Spectral Micro (the STEPFOC's fast reading and fast PWM) |
| 13 | sin and cos come from the integer table (parameter 65) |
| 14 | the position input filter is on (parameter 74 not 0) |
| 15 | the velocity-integral deadband is on (parameter 75 not 0) |
| 16-17 | parameter 56 (no effect on the Spectral Micro) |
| 20 | a calibration is running |
| 21 | the encoder table is being measured |
| 22 | the anti-cogging is being identified |
| 23 | the runs after a calibration are about to start |
| 24 | sound is playing ([Sound](../../06-operation/sound.md)) |

Bits 18, 19 and 25 to 31 are 0.

## Reading the capture

A capture records three signals inside the control loop, one sample every *divider* loops, 1024 samples per
channel. It starts when parameter 28 is written: at once (1), when the error flag rises (2, a watchdog trip
included), or when channel A rises (3) or falls (4) through the level of parameter 29. Parameter 30 keeps that many
samples from before the trigger. [Status and diagnostics](../../06-operation/diagnostics.md) shows a whole capture.

1. Set the signals (24, 25, 26), the divider (27), the pre-trigger (30) and, for 3 and 4, the level (29).
2. Write the trigger (28). Parameter 31 reads 1 (armed), 2 (recording), then 3 (done).
3. Read parameter 32 (samples readable) and 33 (the trigger sample's index, −1 if none).
4. Send_Buffer_Read with kind 0, first 0, count = parameter 32: one Respond_Buffer_Data frame per sample, oldest
   first.

The histogram works the same way with parameters 34 to 36 and kind 1: it adds a signal into 256 bins by the
electrical angle or by the encoder, every control loop, until it is stopped or one bin holds 65535 samples.
