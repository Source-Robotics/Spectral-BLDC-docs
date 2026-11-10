# Parameters and buffers

From firmware 109 a setting that has no command of its own is a **parameter**: a number from 1 to 89 behind one
pair of commands, Send_Parameter (ID 36) to set it and Send_Get_Parameter (ID 37) to read it, answered with
Respond_Parameter (ID 38). The identifier has room for only 64 command IDs, so new settings no longer use them up.
Parameter numbers are permanent: a number is never given a new meaning. Number 73 is not used and stays free.
Parameters 84 to 87 are read only and say which build and which board answer: the git commit the firmware was
built from (84), its build time in Unix seconds (85), the board ID (86) and the calibration ID (87). `#Info` prints
them as `Build`, `Board ID` and `Calibration ID` ([Status and diagnostics](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/diagnostics/)).
Parameters 88 and 89, a diagnostic of when the current sensors are read, are the Spectral Micro's own; STEPFOC
does not have them.

The **buffers** are the larger data a drive holds: a capture of three signals, a histogram, the anti-cogging set
and the encoder table. Send_Buffer_Read (ID 41) reads them in 8-byte frames, Respond_Buffer_Data (ID 42) carries
them, and Send_Buffer_Write (ID 43) writes the anti-cogging set.

Over UART, `#Par` does the same: `#Par` lists every parameter, `#Par 1` reads one, `#Par 1,200` sets it
([Status and utility](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/uart/utility/)).

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

### Send_Parameter

<div class="cmd-facts" markdown><span class="fact">ID 36</span><span class="fact">host → driver</span><span class="fact">5 bytes</span><span class="fact">Python: `Send_Parameter()`</span></div>

Sets one parameter by its number (the [parameter table](#every-parameter)). Firmware 109 gives new settings a parameter number instead of a command ID of their own, since the identifier has room for only 64 command IDs. A value outside a parameter's range is clamped, replaced or refused as the table says; a number the firmware does not know, or a read-only one, is ignored. The driver does not answer: read the value back with Send_Get_Parameter. A value set this way lives in RAM until Send_Save_config, like every other setting; the table says which parameters Save keeps.

**5 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | Parameter | unsigned 8-bit | the parameter number, 1-87 |
| 1-4 |  | Value | signed 32-bit | the new value, in the parameter's unit; for the gains, limits and Kt (8-16, 20) a float's bit pattern |

The driver does not answer this command.

A data frame of another length, or a remote frame, is ignored and flagged as a wrong data length. It does not reset the watchdog.

---

### Send_Get_Parameter

<div class="cmd-facts" markdown><span class="fact">ID 37</span><span class="fact">host → driver</span><span class="fact">1 bytes</span><span class="fact">Python: `Send_Get_Parameter()`</span></div>

Asks for the value in force of one parameter. The answer, Respond_Parameter, comes under ID 38, not 37: a host and a driver must never send data frames with the same identifier, because two sent at the same moment collide. Resets the watchdog. The Python library stores the value in `parameters[number]`.

**1 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | Parameter | unsigned 8-bit | the parameter number |

The driver answers with **Respond_Parameter**.

---

### Respond_Parameter

<div class="cmd-facts" markdown><span class="fact">ID 38</span><span class="fact">driver → host</span><span class="fact">5 bytes</span></div>

The answer to Send_Get_Parameter: the number and the value in force. For a number the firmware does not know the frame carries the number alone (1 byte; the Python library sets `unknown_parameter`). The gains, limits and Kt (parameters 8 to 16 and 20) travel as the bit pattern of an IEEE-754 float, the others as integers.

**The frame** (5 bytes)

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | parameter | unsigned 8-bit | the parameter number |
| 1-4 |  | value | signed 32-bit | the value in force; a float's bits for 8-16 and 20 |

---

### Send_Buffer_Read

<div class="cmd-facts" markdown><span class="fact">ID 41</span><span class="fact">host → driver</span><span class="fact">5 bytes</span><span class="fact">Python: `Send_Buffer_Read()`</span></div>

Asks for entries of one of the drive's buffers: the capture, the histogram, the anti-cogging harmonics or table, or the encoder table. The driver answers with one Respond_Buffer_Data frame per entry (for the two tables, one per three values), sent from its main loop whenever a transmit mailbox is free, so a long read-out never holds up the control loop or other answers. A new request replaces one still in progress; count 0 cancels it. Entries past the end are not sent. Resets the watchdog.

**5 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | Kind | unsigned 8-bit | 0 capture (up to 1024 samples: parameter 32 says how many), 1 histogram (256 bins), 2 anti-cogging harmonics (8 slots), 3 anti-cogging table (256 values), 4 encoder table (128 values) |
| 1-2 |  | First | unsigned 16-bit | the first index |
| 3-4 |  | Count | unsigned 16-bit | how many entries; 0 cancels a read-out |

The driver does not answer this command.

---

### Respond_Buffer_Data

<div class="cmd-facts" markdown><span class="fact">ID 42</span><span class="fact">driver → host</span><span class="fact">8 bytes</span></div>

One entry of a buffer, the answer to Send_Buffer_Read. The first two bytes say which: the kind in the top three bits, the index in the other thirteen (kind × 8192 + index). The six bytes after them depend on the kind, as the table below the frame says.

**The frame** (8 bytes)

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-1 |  | header | unsigned 16-bit | kind × 8192 + index |
| 2-3 |  | word_a | signed 16-bit | capture: channel A; histogram: the count (unsigned); harmonics: the harmonic number (0 = slot unused); tables: entry index |
| 4-5 |  | word_b | signed 16-bit | capture: channel B; histogram: the sum's upper 16 bits; harmonics: a, the cosine term in mA; tables: entry index + 1 |
| 6-7 |  | word_c | signed 16-bit | capture: channel C; histogram: the sum's lower 16 bits; harmonics: b, the sine term in mA; tables: entry index + 2 (0 past the end) |

| Kind | Index | Bytes 2-7 |
|---|---|---|
| 0 capture | the sample, oldest first, 0 to parameter 32 − 1 | channels A, B and C, each in its signal's unit (the parameter table lists the signals) |
| 1 histogram | the bin, 0-255 over one electrical turn or one motor turn | the count (unsigned 16-bit), then the sum (signed 32-bit); the bin's mean is sum ÷ count |
| 2 anti-cogging harmonics | the slot, 0-7 | the harmonic of the electrical angle (1-32, 0 = unused), a and b in mA: the slot adds a·cos(h·θ) + b·sin(h·θ) |
| 3 anti-cogging table | the first of three values, 0-255 | three values in mA, 64 angle counts apart (256 per electrical turn) |
| 4 encoder table | the first of three values, 0-127 | three corrections in 1/16 encoder count, 128 per motor turn |

---

### Send_Buffer_Write

<div class="cmd-facts" markdown><span class="fact">ID 43</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Cogging_Harmonic(), Send_Cogging_Table()`</span></div>

Writes the anti-cogging set: kind 2 one harmonic slot per frame, kind 3 three table values per frame, in the Respond_Buffer_Data layout. Other kinds are ignored (the encoder table cannot be written), and so is a harmonic above 32. The set lives in RAM until Send_Save_config; switch it on with parameter 37. The driver does not answer.

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-1 |  | Header | unsigned 16-bit | kind × 8192 + index; kind 2 or 3 |
| 2-3 |  | Word A | signed 16-bit | kind 2: the harmonic (1-32, 0 = unused); kind 3: value at index |
| 4-5 |  | Word B | signed 16-bit | kind 2: a in mA; kind 3: value at index + 1 |
| 6-7 |  | Word C | signed 16-bit | kind 2: b in mA; kind 3: value at index + 2 |

The driver does not answer this command.

---

## Every parameter

The number and the name are read from the firmware; the rest is checked against its source. *Access*: a read-only
parameter ignores a write; a run parameter starts or stops a run when written and gives its state when read.

### Watchdog and tool

Parameters 1 to 5 live in settings block 2 of the EEPROM, 6 and 7 in the first settings block beside the other settings; Send_Save_config keeps all seven. A value outside a range is clamped, replaced or ignored, as the Value column says.

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 1 | `PARAM_TOOL_ID` | set, read | 0 none, 1 SSG-48, 11-33 MSG, 200-254 your own tools; a value outside 0-255 is ignored. Default 0 | yes, settings block 2 | What the drive is built into. For an MSG the tens digit is the rail (1 = 100, 2 = 150, 3 = 200 mm) and the units digit the stepper (1 = 21.5, 2 = 40, 3 = 60 mm). Also `#Tool`; reported in the identity frame. |
| 2 | `PARAM_WD_FALLBACK_TIME` | set, read | ms, 0-60000 (clamped). Default 2000 | yes, settings block 2 | How long watchdog hold or descend runs before the after-action takes over. |
| 3 | `PARAM_WD_FALLBACK_CURRENT` | set, read | mA, signed, -32768 to 32767 (outside: 0). Default 0 | yes, settings block 2 | The current watchdog descend applies. 0 lets gravity lower a joint; a gripper gets its grip current. |
| 4 | `PARAM_WD_FALLBACK_SPEED` | set, read | ticks/s, 0-65535 (outside: 1000). Default 1000 | yes, settings block 2 | The speed watchdog descend never exceeds, in either direction. |
| 5 | `PARAM_WD_AFTER_ACTION` | set, read | 0 legacy, 2 brake, 3 coast (any other value: 0). Default 0 | yes, settings block 2 | What follows hold or descend when the fallback time has run out. |
| 6 | `PARAM_WD_TIME` | set, read | ms, 0 = off (a negative value: 0). Default 0 | yes, settings block 1 | The watchdog time, the same value Send_Watchdog sets. |
| 7 | `PARAM_WD_ACTION` | set, read | 0 legacy, 1 hold, 2 brake, 3 coast, 4 descend (outside 0-255: 0; 5-255 act as legacy). Default 0 | yes, settings block 1 | What a trip of the watchdog alone does, the same value as byte 4 of Send_Watchdog. |

### Gains, limits and settings

The values in force, readable and writable by parameter (their own commands, given in each row, still work). A float travels as its IEEE-754 bit pattern, big-endian, the way the gain commands send it; over UART `#Par 9,0.02` sets Kpv. A write goes to RAM like the commands' own; Send_Save_config keeps it. Parameter 23, the product stamp, stays read only.

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 8 | `PARAM_KPP` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | Kp of the position loop (Send_Position_Gains, `#Kpp`). |
| 9 | `PARAM_KPV` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | Kp of the velocity loop (Send_Velocity_Gains, `#Kpv`). |
| 10 | `PARAM_KIV` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | Ki of the velocity loop (Send_Velocity_Gains, `#Kiv`). |
| 11 | `PARAM_KPIQ` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | Kp of the current loops; writing it sets the Iq and the Id loop, as `#Kpiq` does (Send_Current_Gains sets the Iq loop only). A calibration and parameter 49 set it too. |
| 12 | `PARAM_KIIQ` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | Ki of the current loops; writing it sets the Iq and the Id loop, as `#Kiiq` does (Send_Current_Gains sets the Iq loop only). A calibration and parameter 49 set it too. |
| 13 | `PARAM_KP` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | KP, the stiffness of the impedance (PD) loop (Send_PD_Gains). |
| 14 | `PARAM_KD` | set, read | float; 0 or more, below 10^9 (negative or not a number: refused) | yes | KD, the damping of the impedance (PD) loop (Send_PD_Gains). |
| 15 | `PARAM_VELOCITY_LIMIT` | set, read | float, ticks/s; 0 or more, below 10^9 (otherwise refused) | yes | The velocity limit (Send_Limits, `#Vlimit`). |
| 16 | `PARAM_CURRENT_LIMIT` | set, read | float, mA; 0-2800 (negative or above 2800: refused) | yes | The current limit (Send_Limits, `#Ilim`). |
| 17 | `PARAM_VOLTAGE_LIMIT` | set, read | mV, 0-60000 (outside: refused); 0 = the supply voltage | yes | The voltage limit of the current loops (Send_Voltage_Limit, `#Vlim`). |
| 18 | `PARAM_BRAKE_COAST` | set, read | 1 brake, 0 coast (any value but 0: brake) | no: the driver coasts at every power-up | The idle behaviour (Send_Settings bit 0, `#Brake`). |
| 19 | `PARAM_HEARTBEAT_MS` | set, read | ms, 0-60000 (outside: refused); 0 = off | yes | The heartbeat interval (Send_Heartbeat_Setup). |
| 20 | `PARAM_KT` | set, read | float, Nm/A; 0 or more, below 10^9 (otherwise refused) | yes | The torque constant (Send_Kt, `#Kt`, calibration). |
| 23 | `PARAM_BOARD_PRODUCT` | read only | 2 Spectral Micro, 1 STEPFOC, 0 none | yes, settings block 2 (stamped by the firmware) | The product lock: the product that calibrated this board. Stamped at the first start-up of a calibrated board and at every save. A firmware that finds the other product's stamp drives nothing (see Errors). |

### The motor

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 76 | `PARAM_R_MOHM` | set, read | mΩ, 1-100000 (outside: refused) | yes, with the calibration | The phase resistance, the same value as `#R` (in Ω there). Calibration measures it; set by hand, the current gains follow when parameter 49 is written. |
| 77 | `PARAM_L_UH` | set, read | µH, 1-1000000 (outside: refused) | yes, with the calibration | The phase inductance, the same value as `#L` (in H there). Calibration measures it; set by hand, the current gains follow when parameter 49 is written. |
| 78 | `PARAM_POLE_PAIRS` | set, read | 1-49, only while the driver is idle (otherwise refused); 50 and more would read as a STEPFOC calibration | yes, with the calibration | The motor's pole pairs, the same value as `#PP`. Calibration finds them. |

### Current sensing and the current loop

The current-sense zero is the ADC reading with no current flowing, in counts from 2048 (1 count is about 1.6 mA). The driver measures it at every start-up with the bridge off; the trim is added to it.

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 21 | `PARAM_SENSE1_OFFSET` | set, read | counts from 2048, -400 to 400 (outside: refused) | no: measured again at every start-up | The current-sense zero of channel 1 in use. Measured at start-up (the trim, 59, added); writable for tests, until the next start-up. |
| 22 | `PARAM_SENSE2_OFFSET` | set, read | counts from 2048, -400 to 400 (outside: refused) | no: measured again at every start-up | The current-sense zero of channel 2 in use, as 21. |
| 40 | `PARAM_SENSE1_OFFSET_OFF` | read only | counts from 2048 | no: measured at every start-up | The zero of channel 1 measured with the bridge off, the trim added. |
| 41 | `PARAM_SENSE2_OFFSET_OFF` | read only | counts from 2048 | no: measured at every start-up | The zero of channel 2 measured with the bridge off, the trim added. |
| 42 | `PARAM_SENSE_ZERO_SWITCHING` | read only | 0 not run, 1 measuring, 2 in use, 3 rejected (implausible), 4 interrupted (a command or an error came first), 5 measured, not in use | no | The second zero measurement, made in idle after start-up with the bridge switching at 50 % duty. On the bench it made the current ripple worse, so it is measured and kept but not used unless 46 asks for it. |
| 46 | `PARAM_SENSE_ZERO_USE_SWITCHING` | set, read | 1 the zero measured with the bridge switching, 0 the bridge-off zero. Default 0 | no | Which zero is in use. 1 takes effect only while 42 reads 5 (measured, not in use). |
| 47 | `PARAM_SENSE1_OFFSET_SW` | read only | counts from 2048 | no | The zero of channel 1 measured with the bridge switching. |
| 48 | `PARAM_SENSE2_OFFSET_SW` | read only | counts from 2048 | no | The zero of channel 2 measured with the bridge switching. |
| 49 | `PARAM_CURRENT_BANDWIDTH` | set, read | Hz, 10-500 (outside, or with R or L not set: refused). 160 at every start-up | no; the gains it sets are kept by Save | Writing it sets Kp_iq and Ki_iq at once from R, L and this bandwidth, as `#Cbw` does. Reading gives the bandwidth the gains in force amount to with the R and L in force (0 without them). |
| 58 | `PARAM_ID_SETPOINT` | set, read | mA, -3000 to 3000 (outside: refused). Default 0 | no | The d-axis current setpoint, as `#Id`. It makes no torque, only more current in the coils. |
| 59 | `PARAM_ZERO_TRIM1` | set, read | counts, -60 to 60 (outside: refused). Default 0 | yes, encoder block | The trim added to the zero of channel 1 measured at every start-up; writing it moves the zero in use at once. The Spectral Micro firmware 109 skips the trim step of the anti-cogging identification, so only a write sets it. |
| 60 | `PARAM_ZERO_TRIM2` | set, read | counts, -60 to 60 (outside: refused). Default 0 | yes, encoder block | The trim of channel 2, as 59. |
| 61 | `PARAM_THETA_OFFSET` | read only | 0.1° electrical | yes, with the calibration | The electrical offset between the encoder and the motor, found by calibration (`#Offset` in rad). |
| 62 | `PARAM_TRIM_H1_BEFORE` | read only | 0.1 mA | no | The 1st harmonic of the anti-cogging set found by an identification with the trim (43 = 4 or 5). |
| 63 | `PARAM_TRIM_H1_AFTER` | read only | 0.1 mA | no | After a trim, the 1st harmonic again; the Spectral Micro skips the trim, so it equals 62. |
| 64 | `PARAM_COMM_DELAY_US` | set, read | µs, 0-500 (outside: refused), 0 = off. Default 234 | no: 234 at every start-up | Commutation delay compensation: the output voltage is turned forward by the angle the rotor covers in this time. Applied in the closed-loop modes above 100 ticks/s. 234 µs is the Spectral Micro's own delay, measured on the bench. |
| 65 | `PARAM_FAST_TRIG` | set, read | 1 from the integer sine table, 0 from the float routine. Default 0 | no | Where the transforms of every control loop take sin and cos from. On the STEPFOC bench the table was not faster. |
| 88 | `PARAM_SENSE_SAMPLE_AT` | set, read | -1: read wherever the code is (the default); 0 to the PWM period (the timer's reload value): wait for that count first (outside: refused) | no: -1 at every start-up | An experimental diagnostic of when the current sensors are read, off by default. They are read by a software start, wherever the code happens to be in the 25 kHz centre-aligned PWM cycle, so the moment of a reading depends on the code before it. With a count set, the driver waits until the PWM counter is within 24 counts of it (at most about 60 µs), then reads. Leave it at -1 unless you are investigating the current sensing. |
| 89 | `PARAM_SENSE_SAMPLE_SEEN` | read only | the PWM counter at the last reading, +65536 while it counts down | — | Where in the PWM cycle the last current reading happened; it shows where parameter 88 puts the readings. |

### Speed estimate and the velocity loop

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 50 | `PARAM_SPEED_ESTIMATOR` | set, read | 0 moving average, 1 PLL, 2 direct PLL (outside: refused). Default 2 | no: 2 at every start-up | The speed the loops, the watchdog descend, telemetry and the capture use. Calibration and the gripper's stop detection always use the moving average. |
| 51 | `PARAM_SPEED_PLL_BANDWIDTH` | set, read | Hz, 10-250 (outside: refused). Default 100 | no: 100 at every start-up | The natural frequency of both PLLs. |
| 74 | `PARAM_INPUT_FILTER_HZ` | set, read | Hz, 0-200 (outside: refused), 0 = off. Default 0 | no | The position input filter, position and PD modes: a critically damped filter between the host's position setpoints and the loops, which also makes the speed from them. Only for hosts that send positions without the speed; about the host's setpoint rate ÷ 12. |
| 75 | `PARAM_VEL_INT_DEADBAND` | set, read | ticks, 0-2000 (outside: refused), 0 = off. Default 0 | no | Position mode: the velocity integral sees the position error less this band, so a holding motor stops pushing against a small error. It trades holding current for accuracy. |

### Anti-cogging

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 37 | `PARAM_COGGING_MODE` | set, read | 0 off, 1 harmonics, 2 table. Default 0 | yes, anti-cogging block | Which form of the stored anti-cogging is added to the current setpoint in velocity and position modes. 1 or 2 is refused while the stored set holds nothing for that form: read it back. |
| 38 | `PARAM_COGGING_SCALE` | set, read | percent, 0-200 (clamped). Default 100 | yes, anti-cogging block | How much of the stored anti-cogging is applied. |
| 43 | `PARAM_COGCAL` | set starts or stops a run; read gives its state | Write 0 abort, 1 identify, 2 identify and save, 3 encoder table, then anti-cogging, then save all, 4 identify with the current-sense zero trim, 5 the same and save. Read 0 idle, 1 turning forward, 2 turning backward, 3 done (harmonics on), 4 aborted, 5 failed (an error, or not calibrated), 6 failed (the shaft did not turn), 7 a combined run is measuring the encoder table, 8 the combined run's encoder table failed (52 says why), 9 not used, 10 switched off (the encoder table was measured again on its own), 11 done without the trim | the result, when started with 2, 3 or 5 | The anti-cogging identification on the drive: one motor turn forward and one back in velocity mode at the speed of 44. The shaft must be free to turn. A command from a host or an error aborts it. On the Spectral Micro 4 and 5 identify like 1 and 2 (the trim step is skipped); not yet tested on its bench. |
| 44 | `PARAM_COGCAL_SPEED` | set, read | ticks/s, 100-20000 (clamped). Default 1500 | no | The speed the identification turns at. |
| 45 | `PARAM_COGCAL_RIPPLE` | read only | 0.1 mA rms | no | The cogging current the last identification found, rms. |

### Encoder table

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 52 | `PARAM_ENCAL` | set starts or stops a run; read gives its state | Write 0 abort, 1 measure and use, 2 measure, use and save, 3 then the anti-cogging and save all. Read 0 idle, 1 turning forward, 2 turning backward, 3 done (in use), 4 aborted, 5 failed (an error, or not calibrated), 6 failed (the rotor did not follow the field), 7 rejected (over 4° peak to peak, or an offset move over 60° electrical) | the table, when started with 2 or 3 | Measures the encoder table: the field turns the rotor open loop one shaft turn forward and one back at 2048 ticks/s (about 20 s). The shaft must be free. |
| 53 | `PARAM_ENCAL_USE` | set, read | 1 on, 0 off; 1 only when a table was measured; refused while one is being measured | yes, encoder block | Corrects the encoder reading with the table. |
| 54 | `PARAM_ENCAL_PP` | read only | 0.01° of the shaft | with the table | The table's error, peak to peak (0 without a table). |
| 55 | `PARAM_ENCAL_ONCE` | read only | 0.01° of the shaft | with the table | The once-per-turn part of the error, its amplitude (mostly a magnet off the axis). |
| 56 | `PARAM_AFTER_CAL` | set, read | 0, 1 or 2 (outside: refused). Default 0 | yes, encoder block | No effect on the Spectral Micro: `#Cal` always runs the encoder table and the anti-cogging, and `#Calonly` never does. It stays so that the parameter numbers match STEPFOC. |
| 57 | `PARAM_ENCAL_OFFSET` | read only | 0.1° electrical | no | How far the last encoder-table run moved the electrical offset. |

### Capture and histogram

The signal numbers: 0 none, 1 measured Iq (mA), 2 measured Id (mA), 3 Iq setpoint with the anti-cogging (mA), 4 speed (ticks/s, saturates at ±32767), 5 speed ÷ 16, 6 position (ticks, the low 16 bits), 7 position error (ticks), 8 electrical angle (0-16383 per electrical turn, from the encoder alone), 9 encoder (0-16383 per motor turn), 10 Vbus (10 mV), 11 and 12 the two current-sense readings (counts after the zero), 13 the control interrupt's time (µs), 14 the anti-cogging feedforward (mA), 15 the Iq setpoint without the anti-cogging (mA), 16 the Uq setpoint (mV), 17 and 18 the d and q voltage the output transform received (mV). None of these settings is saved.

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 24 | `PARAM_CAPTURE_SOURCE_A` | set, read | signal 0-18 (outside: 0). Default 4, speed | no | The signal of channel A, which is also the trigger channel. |
| 25 | `PARAM_CAPTURE_SOURCE_B` | set, read | signal 0-18 (outside: 0). Default 1, Iq | no | The signal of channel B. |
| 26 | `PARAM_CAPTURE_SOURCE_C` | set, read | signal 0-18 (outside: 0). Default 8, electrical angle | no | The signal of channel C. |
| 27 | `PARAM_CAPTURE_DIVIDER` | set, read | control loops per sample, 1-65535 (clamped). Default 1 | no | One sample every N control loops of 200 µs. |
| 28 | `PARAM_CAPTURE_TRIGGER` | set, read | 0 stop, 1 now, 2 on an error, 3 channel A rising through the level, 4 falling through it (outside: 0) | no | 1 to 4 clear the buffer and arm a capture; 0 stops one and keeps what was recorded. The error trigger fires when the error flag rises, a watchdog trip included; an error already present does not fire it. |
| 29 | `PARAM_CAPTURE_LEVEL` | set, read | channel A's unit, -32768 to 32767 (saturated). Default 0 | no | The level of triggers 3 and 4. |
| 30 | `PARAM_CAPTURE_PRETRIGGER` | set, read | samples, 0-1023 (clamped). Default 0 | no | How many samples from before the trigger the capture keeps. |
| 31 | `PARAM_CAPTURE_STATE` | read only | 0 idle, 1 armed, 2 recording, 3 done | no | Where the capture stands. |
| 32 | `PARAM_CAPTURE_COUNT` | read only | samples, 0-1024 | no | The samples readable with buffer kind 0. |
| 33 | `PARAM_CAPTURE_TRIGGER_INDEX` | read only | sample index; -1 before a trigger | no | Which sample of the read-out is the trigger sample. |
| 34 | `PARAM_HIST_X` | set, read | 0 off, 1 electrical angle, 2 encoder (256 bins each; outside: 0) | no | 1 or 2 clear the histogram and start it; 0 stops it and keeps the data readable. |
| 35 | `PARAM_HIST_Y` | set, read | signal 0-18 (outside: 0). Default 3, Iq setpoint | no | The signal summed per bin. Set it before 34. |
| 36 | `PARAM_HIST_SAMPLES` | read only | samples | no | Samples summed since the start. The histogram stops by itself when one bin holds 65535. |
| 39 | `PARAM_CAPTURE_LENGTH` | read only | 1024 | — | The samples per channel a capture holds. |

### Sound

None of the sound settings is saved; see [Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/sound/).

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 80 | `PARAM_SOUND_STATE` | read only | bits 0-7 events queued, 8-18 samples buffered, 24 a tone sounds, 25 the queue plays, 26 samples play, 27 the samples ran dry | — | What the sound is doing; a host that refills the queue or the sample buffer reads it. |
| 81 | `PARAM_SOUND_LIMIT_MV` | set, read | mV, 0-6000 (outside: refused). Default 2000; 0 refuses sound and stops what plays | no: 2000 at every start-up | The sound's voltage at most, all tones and samples together. |
| 82 | `PARAM_SOUND_AXIS` | set, read | 1 the q axis (default), 0 the d axis (outside: refused) | no: 1 at every start-up | Which axis carries the sound. The q axis makes torque, a small ripple at the tone's pitch, and was much louder on the bench; the d axis makes no torque and is quieter. |

### Status

| No. | Name | Access | Value | Kept by Save | What it is |
|---|---|---|---|---|---|
| 79 | `PARAM_FEATURES` | read only | bits, see What is in force | — | What is in force and what is running, one bit each. |
| 83 | `PARAM_STACK_UNUSED` | read only | bytes; -1 if it was not measured | — | The stack margin: RAM between the heap and the stack that the stack has not used since start-up (setup() fills it with a pattern at its end, and this counts the bytes the pattern is still in). The stack needs about 1.5 to 2 KB of the about 7 KB there are; a value far below that means the drive is short of RAM. |
| 84 | `PARAM_BUILD_COMMIT` | read only | the commit's first 7 hex digits as a number (bits 0-27); bit 28 set: built with uncommitted changes; 0 when git was not available at the build | — | The git commit the firmware was built from. `#Info` prints it as `Build:`, with a `+` for bit 28. |
| 85 | `PARAM_BUILD_TIME` | read only | Unix seconds, UTC; 0 when the build did not set it | — | When the firmware was built. |
| 86 | `PARAM_BOARD_ID` | read only | 32 bits, read as unsigned | — | This board: the chip's factory-unique 96-bit number folded into 32 bits. It never changes, also not with a new firmware or `#Default`. `#Info` prints it as `Board ID:`, 8 hex digits. It is not the bootloader's board ID (0 to 13). |
| 87 | `PARAM_CALIBRATION_ID` | read only | 32 bits, read as unsigned; 0 before the first calibration | yes, settings block 2 | A new number at every successful calibration, so a host can tell one calibration from the next. Send_Save_config keeps it, and `#Default` sets it back to 0. `#Info` prints it as `Calibration ID:`, 8 hex digits. |

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
| 24 | sound is playing ([Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/sound/)) |

Bits 18, 19 and 25 to 31 are 0.

## Reading the capture

A capture records three signals inside the control loop, one sample every *divider* loops, 1024 samples per
channel. It starts when parameter 28 is written: at once (1), when the error flag rises (2, a watchdog trip
included), or when channel A rises (3) or falls (4) through the level of parameter 29. Parameter 30 keeps that many
samples from before the trigger. [Status and diagnostics](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/diagnostics/) shows a whole capture.

1. Set the signals (24, 25, 26), the divider (27), the pre-trigger (30) and, for 3 and 4, the level (29).
2. Write the trigger (28). Parameter 31 reads 1 (armed), 2 (recording), then 3 (done).
3. Read parameter 32 (samples readable) and 33 (the trigger sample's index, −1 if none).
4. Send_Buffer_Read with kind 0, first 0, count = parameter 32: one Respond_Buffer_Data frame per sample, oldest
   first.

The histogram works the same way with parameters 34 to 36 and kind 1: it adds a signal into 256 bins by the
electrical angle or by the encoder, every control loop, until it is stopped or one bin holds 65535 samples.
