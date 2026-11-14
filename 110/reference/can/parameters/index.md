# Parameters and buffers

From firmware 109 a setting that has no command of its own is a **parameter**: a number from 1 to 93 (89 in firmware
109) behind one pair of commands, Send_Parameter (ID 36) to set it and Send_Get_Parameter (ID 37) to read it,
answered with Respond_Parameter (ID 38). The identifier has room for only 64 command IDs, so new settings no longer
use them up.

Parameter numbers are permanent: a number is never given a new meaning. Number 73 is not used and stays free.
Parameters 84 to 87 are read only and say which build and which board answer: the git commit the firmware was built
from (84), its build time in Unix seconds (85), the board ID (86) and the calibration ID (87). `#Info` prints them
as `Build`, `Board ID` and `Calibration ID` ([Status and diagnostics](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/diagnostics/)).
Parameters 88 and 89, a diagnostic of when the current sensors are read, are the Spectral Micro's own; STEPFOC does
not have them.

Firmware 110 adds 90 to 93: the three settings that only UART could set before, `#Rstint` (90), `#Term`, the
thermistor (91) and `#Gripper`, gripper mode (92), and the gripper's stroke (93, read only). The Spectral-BLDC
library 1.22 names them (`PARAM_RSTINT`, `PARAM_THERMISTOR`, `PARAM_GRIPPER_MODE`, `PARAM_GRIPPER_STROKE`); 1.21
sets and reads them by their numbers.

The **buffers** are the larger data a drive holds: a capture of three signals, a histogram, the anti-cogging set
and the encoder table. Send_Buffer_Read (ID 41) reads them in 8-byte frames, Respond_Buffer_Data (ID 42) carries
them, and Send_Buffer_Write (ID 43) writes the anti-cogging set.

Over UART, `#Par` does the same: `#Par` lists every parameter, `#Par 1` reads one, `#Par 1,200` sets it
([Status and utility](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/uart/utility/)).

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

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0 | Parameter | unsigned 8-bit | the parameter number, 1-93 |
| 1-4 | Value | signed 32-bit | the new value, in the parameter's unit; for the gains, limits and Kt (8-16, 20) a float's bit pattern |

</div>

The driver does not answer this command.

A data frame of another length, or a remote frame, is ignored and flagged as a wrong data length. It does not reset the watchdog.

---

### Send_Get_Parameter

<div class="cmd-facts" markdown><span class="fact">ID 37</span><span class="fact">host → driver</span><span class="fact">1 bytes</span><span class="fact">Python: `Send_Get_Parameter()`</span></div>

Asks for the value in force of one parameter. The answer, Respond_Parameter, comes under ID 38, not 37: a host and a driver must never send data frames with the same identifier, because two sent at the same moment collide. Resets the watchdog. The Python library stores the value in `parameters[number]`.

**1 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0 | Parameter | unsigned 8-bit | the parameter number |

</div>

The driver answers with **Respond_Parameter**.

---

### Respond_Parameter

<div class="cmd-facts" markdown><span class="fact">ID 38</span><span class="fact">driver → host</span><span class="fact">5 bytes</span></div>

The answer to Send_Get_Parameter: the number and the value in force. For a number the firmware does not know the frame carries the number alone (1 byte; the Python library sets `unknown_parameter`). The gains, limits and Kt (parameters 8 to 16 and 20) travel as the bit pattern of an IEEE-754 float, the others as integers.

**The frame** (5 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0 | parameter | unsigned 8-bit | the parameter number |
| 1-4 | value | signed 32-bit | the value in force; a float's bits for 8-16 and 20 |

</div>

---

### Send_Buffer_Read

<div class="cmd-facts" markdown><span class="fact">ID 41</span><span class="fact">host → driver</span><span class="fact">5 bytes</span><span class="fact">Python: `Send_Buffer_Read()`</span></div>

Asks for entries of one of the drive's buffers: the capture, the histogram, the anti-cogging harmonics or table, or the encoder table. The driver answers with one Respond_Buffer_Data frame per entry (for the two tables, one per three values), sent from its main loop whenever a transmit mailbox is free, so a long read-out never holds up the control loop or other answers. A new request replaces one still in progress; count 0 cancels it. Entries past the end are not sent. Resets the watchdog.

**5 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0 | Kind | unsigned 8-bit | 0 capture (up to 1024 samples: parameter 32 says how many), 1 histogram (256 bins), 2 anti-cogging harmonics (8 slots), 3 anti-cogging table (256 values), 4 encoder table (128 values) |
| 1-2 | First | unsigned 16-bit | the first index |
| 3-4 | Count | unsigned 16-bit | how many entries; 0 cancels a read-out |

</div>

The driver does not answer this command.

---

### Respond_Buffer_Data

<div class="cmd-facts" markdown><span class="fact">ID 42</span><span class="fact">driver → host</span><span class="fact">8 bytes</span></div>

One entry of a buffer, the answer to Send_Buffer_Read. The first two bytes say which: the kind in the top three bits, the index in the other thirteen (kind × 8192 + index). The six bytes after them depend on the kind, as the table below the frame says.

**The frame** (8 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-1 | header | unsigned 16-bit | kind × 8192 + index |
| 2-3 | word_a | signed 16-bit | capture: channel A; histogram: the count (unsigned); harmonics: the harmonic number (0 = slot unused); tables: entry index |
| 4-5 | word_b | signed 16-bit | capture: channel B; histogram: the sum's upper 16 bits; harmonics: a, the cosine term in mA; tables: entry index + 1 |
| 6-7 | word_c | signed 16-bit | capture: channel C; histogram: the sum's lower 16 bits; harmonics: b, the sine term in mA; tables: entry index + 2 (0 past the end) |

</div>

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

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-1 | Header | unsigned 16-bit | kind × 8192 + index; kind 2 or 3 |
| 2-3 | Word A | signed 16-bit | kind 2: the harmonic (1-32, 0 = unused); kind 3: value at index |
| 4-5 | Word B | signed 16-bit | kind 2: a in mA; kind 3: value at index + 1 |
| 6-7 | Word C | signed 16-bit | kind 2: b in mA; kind 3: value at index + 2 |

</div>

The driver does not answer this command.

---

## Every parameter

The number and the name are read from the firmware; the rest is checked against its source. *Access*: a read-only
parameter ignores a write; a run parameter starts or stops a run when written and gives its state when read.

### Watchdog and tool

Parameters 1 to 5 live in settings block 2 of the EEPROM, 6 and 7 in the first settings block beside the other settings; Send_Save_config keeps all seven. A value outside a range is clamped, replaced or ignored, as the Value column says.

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 1 | What the drive is built into. For an MSG the tens digit is the rail (1 = 100, 2 = 150, 3 = 200 mm) and the units digit the stepper (1 = 21.5, 2 = 40, 3 = 60 mm). Also `#Tool`; reported in the identity frame.<br><span class="meta">`PARAM_TOOL_ID` · Access: set, read · Kept by Save: yes, settings block 2</span> | 0 none, 1 SSG-48, 11-33 MSG, 200-254 your own tools; a value outside 0-255 is ignored. Default 0 |
| 2 | How long watchdog hold or descend runs before the after-action takes over.<br><span class="meta">`PARAM_WD_FALLBACK_TIME` · Access: set, read · Kept by Save: yes, settings block 2</span> | ms, 0-60000 (clamped). Default 2000 |
| 3 | The current watchdog descend applies. 0 lets gravity lower a joint; a gripper gets its grip current.<br><span class="meta">`PARAM_WD_FALLBACK_CURRENT` · Access: set, read · Kept by Save: yes, settings block 2</span> | mA, signed, -32768 to 32767 (outside: 0). Default 0 |
| 4 | The speed watchdog descend never exceeds, in either direction.<br><span class="meta">`PARAM_WD_FALLBACK_SPEED` · Access: set, read · Kept by Save: yes, settings block 2</span> | ticks/s, 0-65535 (outside: 1000). Default 1000 |
| 5 | What follows hold or descend when the fallback time has run out.<br><span class="meta">`PARAM_WD_AFTER_ACTION` · Access: set, read · Kept by Save: yes, settings block 2</span> | 0 legacy, 2 brake, 3 coast (any other value: 0). Default 0 |
| 6 | The watchdog time, the same value Send_Watchdog sets.<br><span class="meta">`PARAM_WD_TIME` · Access: set, read · Kept by Save: yes, settings block 1</span> | ms, 0 = off (a negative value: 0). Default 0 |
| 7 | What a trip of the watchdog alone does, the same value as byte 4 of Send_Watchdog.<br><span class="meta">`PARAM_WD_ACTION` · Access: set, read · Kept by Save: yes, settings block 1</span> | 0 legacy, 1 hold, 2 brake, 3 coast, 4 descend (outside 0-255: 0; 5-255 act as legacy). Default 0 |

</div>

### Gains, limits and settings

The values in force, readable and writable by parameter (their own commands, given in each row, still work). A float travels as its IEEE-754 bit pattern, big-endian, the way the gain commands send it; over UART `#Par 9,0.02` sets Kpv. A write goes to RAM like the commands' own; Send_Save_config keeps it. Parameter 23, the product stamp, stays read only.

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 8 | Kp of the position loop (Send_Position_Gains, `#Kpp`).<br><span class="meta">`PARAM_KPP` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 9 | Kp of the velocity loop (Send_Velocity_Gains, `#Kpv`).<br><span class="meta">`PARAM_KPV` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 10 | Ki of the velocity loop (Send_Velocity_Gains, `#Kiv`).<br><span class="meta">`PARAM_KIV` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 11 | Kp of the current loops; writing it sets the Iq and the Id loop, as `#Kpiq` does (Send_Current_Gains sets the Iq loop only). A calibration and parameter 49 set it too.<br><span class="meta">`PARAM_KPIQ` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 12 | Ki of the current loops; writing it sets the Iq and the Id loop, as `#Kiiq` does (Send_Current_Gains sets the Iq loop only). A calibration and parameter 49 set it too.<br><span class="meta">`PARAM_KIIQ` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 13 | KP, the stiffness of the impedance (PD) loop (Send_PD_Gains).<br><span class="meta">`PARAM_KP` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 14 | KD, the damping of the impedance (PD) loop (Send_PD_Gains).<br><span class="meta">`PARAM_KD` · Access: set, read · Kept by Save: yes</span> | float; 0 or more, below 10^9 (negative or not a number: refused) |
| 15 | The velocity limit (Send_Limits, `#Vlimit`).<br><span class="meta">`PARAM_VELOCITY_LIMIT` · Access: set, read · Kept by Save: yes</span> | float, ticks/s; 0 or more, below 10^9 (otherwise refused) |
| 16 | The current limit (Send_Limits, `#Ilim`).<br><span class="meta">`PARAM_CURRENT_LIMIT` · Access: set, read · Kept by Save: yes</span> | float, mA; 0-2800 (negative or above 2800: refused) |
| 17 | The voltage limit of the current loops (Send_Voltage_Limit, `#Vlim`).<br><span class="meta">`PARAM_VOLTAGE_LIMIT` · Access: set, read · Kept by Save: yes</span> | mV, 0-60000 (outside: refused); 0 = the supply voltage |
| 18 | The idle behaviour (Send_Settings bit 0, `#Brake`).<br><span class="meta">`PARAM_BRAKE_COAST` · Access: set, read · Kept by Save: yes, settings block 2, from firmware 110 (109 coasted at every power-up). Never saved, and after `#Default`: coast</span> | 1 brake, 0 coast (any value but 0: brake) |
| 19 | The heartbeat interval (Send_Heartbeat_Setup).<br><span class="meta">`PARAM_HEARTBEAT_MS` · Access: set, read · Kept by Save: yes</span> | ms, 0-60000 (outside: refused); 0 = off |
| 20 | The torque constant (Send_Kt, `#Kt`, calibration).<br><span class="meta">`PARAM_KT` · Access: set, read · Kept by Save: yes</span> | float, Nm/A; 0 or more, below 10^9 (otherwise refused) |
| 23 | The product lock: the product that calibrated this board. Stamped at the first start-up of a calibrated board and at every save. A firmware that finds the other product's stamp drives nothing (see Errors).<br><span class="meta">`PARAM_BOARD_PRODUCT` · Access: read only · Kept by Save: yes, settings block 2 (stamped by the firmware)</span> | 2 Spectral Micro, 1 STEPFOC, 0 none |
| 90 | Whether the velocity and current integrators are reset on every new setpoint command (`#Rstint`). Added in firmware 110.<br><span class="meta">`PARAM_RSTINT` · Access: set, read · Kept by Save: yes</span> | 0 or 1 (anything else: refused). Default 0 |
| 91 | The thermistor measurement and the temperature error (`#Term`). Added in firmware 110.<br><span class="meta">`PARAM_THERMISTOR` · Access: set, read · Kept by Save: yes</span> | 0 off, 1 on (anything else: refused). Default 0 |
| 92 | Gripper mode (`#Gripper`), in force at once: the driver then reads its commands as a gripper, or as a motor. It is written only while the driver is idle, so a move is never cut over half-way. Added in firmware 110.<br><span class="meta">`PARAM_GRIPPER_MODE` · Access: set, read · Kept by Save: yes</span> | 0 or 1 (anything else, or a write while the driver is not idle: refused). Default 0 |

</div>

### The motor

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 76 | The phase resistance, the same value as `#R` (in Ω there). Calibration measures it; set by hand, the current gains follow when parameter 49 is written.<br><span class="meta">`PARAM_R_MOHM` · Access: set, read · Kept by Save: yes, with the calibration</span> | mΩ, 1-100000 (outside: refused) |
| 77 | The phase inductance, the same value as `#L` (in H there). Calibration measures it; set by hand, the current gains follow when parameter 49 is written.<br><span class="meta">`PARAM_L_UH` · Access: set, read · Kept by Save: yes, with the calibration</span> | µH, 1-1000000 (outside: refused) |
| 78 | The motor's pole pairs, the same value as `#PP`. Calibration finds them.<br><span class="meta">`PARAM_POLE_PAIRS` · Access: set, read · Kept by Save: yes, with the calibration</span> | 1-49, only while the driver is idle (otherwise refused); 50 and more would read as a STEPFOC calibration |

</div>

### Current sensing and the current loop

The current-sense zero is the ADC reading with no current flowing, in counts from 2048 (1 count is about 1.6 mA). The driver measures it at every start-up with the bridge off; the trim is added to it.

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 21 | The current-sense zero of channel 1 in use. Measured at start-up (the trim, 59, added); writable for tests, until the next start-up.<br><span class="meta">`PARAM_SENSE1_OFFSET` · Access: set, read · Kept by Save: no: measured again at every start-up</span> | counts from 2048, -400 to 400 (outside: refused) |
| 22 | The current-sense zero of channel 2 in use, as 21.<br><span class="meta">`PARAM_SENSE2_OFFSET` · Access: set, read · Kept by Save: no: measured again at every start-up</span> | counts from 2048, -400 to 400 (outside: refused) |
| 40 | The zero of channel 1 measured with the bridge off, the trim added.<br><span class="meta">`PARAM_SENSE1_OFFSET_OFF` · Access: read only · Kept by Save: no: measured at every start-up</span> | counts from 2048 |
| 41 | The zero of channel 2 measured with the bridge off, the trim added.<br><span class="meta">`PARAM_SENSE2_OFFSET_OFF` · Access: read only · Kept by Save: no: measured at every start-up</span> | counts from 2048 |
| 42 | The second zero measurement, made in idle after start-up with the bridge switching at 50 % duty. On the bench it made the current ripple worse, so it is measured and kept but not used unless 46 asks for it.<br><span class="meta">`PARAM_SENSE_ZERO_SWITCHING` · Access: read only · Kept by Save: no</span> | 0 not run, 1 measuring, 2 in use, 3 rejected (implausible), 4 interrupted (a command or an error came first), 5 measured, not in use |
| 46 | Which zero is in use. 1 takes effect only while 42 reads 5 (measured, not in use).<br><span class="meta">`PARAM_SENSE_ZERO_USE_SWITCHING` · Access: set, read · Kept by Save: no</span> | 1 the zero measured with the bridge switching, 0 the bridge-off zero. Default 0 |
| 47 | The zero of channel 1 measured with the bridge switching.<br><span class="meta">`PARAM_SENSE1_OFFSET_SW` · Access: read only · Kept by Save: no</span> | counts from 2048 |
| 48 | The zero of channel 2 measured with the bridge switching.<br><span class="meta">`PARAM_SENSE2_OFFSET_SW` · Access: read only · Kept by Save: no</span> | counts from 2048 |
| 49 | Writing it sets Kp_iq and Ki_iq at once from R, L and this bandwidth, as `#Cbw` does. Reading gives the bandwidth the gains in force amount to with the R and L in force (0 without them).<br><span class="meta">`PARAM_CURRENT_BANDWIDTH` · Access: set, read · Kept by Save: no; the gains it sets are kept by Save</span> | Hz, 10-500 (outside, or with R or L not set: refused). 160 at every start-up |
| 58 | The d-axis current setpoint, as `#Id`. It makes no torque, only more current in the coils.<br><span class="meta">`PARAM_ID_SETPOINT` · Access: set, read · Kept by Save: no</span> | mA, -3000 to 3000 (outside: refused). Default 0 |
| 59 | The trim added to the zero of channel 1 measured at every start-up; writing it moves the zero in use at once. The Spectral Micro firmware 109 skips the trim step of the anti-cogging identification, so only a write sets it.<br><span class="meta">`PARAM_ZERO_TRIM1` · Access: set, read · Kept by Save: yes, encoder block</span> | counts, -60 to 60 (outside: refused). Default 0 |
| 60 | The trim of channel 2, as 59.<br><span class="meta">`PARAM_ZERO_TRIM2` · Access: set, read · Kept by Save: yes, encoder block</span> | counts, -60 to 60 (outside: refused). Default 0 |
| 61 | The electrical offset between the encoder and the motor, found by calibration (`#Offset` in rad).<br><span class="meta">`PARAM_THETA_OFFSET` · Access: read only · Kept by Save: yes, with the calibration</span> | 0.1° electrical |
| 62 | The 1st harmonic of the anti-cogging set found by an identification with the trim (43 = 4 or 5).<br><span class="meta">`PARAM_TRIM_H1_BEFORE` · Access: read only · Kept by Save: no</span> | 0.1 mA |
| 63 | After a trim, the 1st harmonic again; the Spectral Micro skips the trim, so it equals 62.<br><span class="meta">`PARAM_TRIM_H1_AFTER` · Access: read only · Kept by Save: no</span> | 0.1 mA |
| 64 | Commutation delay compensation: the output voltage is turned forward by the angle the rotor covers in this time. Applied in the closed-loop modes above 100 ticks/s. 234 µs is the Spectral Micro's own delay, measured on the bench.<br><span class="meta">`PARAM_COMM_DELAY_US` · Access: set, read · Kept by Save: no: 234 at every start-up</span> | µs, 0-500 (outside: refused), 0 = off. Default 234 |
| 65 | Where the transforms of every control loop take sin and cos from. On the STEPFOC bench the table was not faster.<br><span class="meta">`PARAM_FAST_TRIG` · Access: set, read · Kept by Save: no</span> | 1 from the integer sine table, 0 from the float routine. Default 0 |
| 88 | An experimental diagnostic of when the current sensors are read, off by default. They are read by a software start, wherever the code happens to be in the 25 kHz centre-aligned PWM cycle, so the moment of a reading depends on the code before it. With a count set, the driver waits until the PWM counter is within 24 counts of it (at most about 60 µs), then reads. Leave it at -1 unless you are investigating the current sensing.<br><span class="meta">`PARAM_SENSE_SAMPLE_AT` · Access: set, read · Kept by Save: no: -1 at every start-up</span> | -1: read wherever the code is (the default); 0 to the PWM period (the timer's reload value): wait for that count first (outside: refused) |
| 89 | Where in the PWM cycle the last current reading happened; it shows where parameter 88 puts the readings.<br><span class="meta">`PARAM_SENSE_SAMPLE_SEEN` · Access: read only · Kept by Save: —</span> | the PWM counter at the last reading, +65536 while it counts down |

</div>

### Speed estimate and the velocity loop

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 50 | The speed the loops, the watchdog descend, telemetry and the capture use. Calibration and the gripper's stop detection always use the moving average.<br><span class="meta">`PARAM_SPEED_ESTIMATOR` · Access: set, read · Kept by Save: no: 2 at every start-up</span> | 0 moving average, 1 PLL, 2 direct PLL (outside: refused). Default 2 |
| 51 | The natural frequency of both PLLs.<br><span class="meta">`PARAM_SPEED_PLL_BANDWIDTH` · Access: set, read · Kept by Save: no: 100 at every start-up</span> | Hz, 10-250 (outside: refused). Default 100 |
| 74 | The position input filter, position and PD modes: a critically damped filter between the host's position setpoints and the loops, which also makes the speed from them. Only for hosts that send positions without the speed; about the host's setpoint rate ÷ 12.<br><span class="meta">`PARAM_INPUT_FILTER_HZ` · Access: set, read · Kept by Save: no</span> | Hz, 0-200 (outside: refused), 0 = off. Default 0 |
| 75 | Position mode: the velocity integral sees the position error less this band, so a holding motor stops pushing against a small error. It trades holding current for accuracy.<br><span class="meta">`PARAM_VEL_INT_DEADBAND` · Access: set, read · Kept by Save: no</span> | ticks, 0-2000 (outside: refused), 0 = off. Default 0 |

</div>

### Anti-cogging

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 37 | Which form of the stored anti-cogging is added to the current setpoint in velocity and position modes. 1 or 2 is refused while the stored set holds nothing for that form: read it back.<br><span class="meta">`PARAM_COGGING_MODE` · Access: set, read · Kept by Save: yes, anti-cogging block</span> | 0 off, 1 harmonics, 2 table. Default 0 |
| 38 | How much of the stored anti-cogging is applied.<br><span class="meta">`PARAM_COGGING_SCALE` · Access: set, read · Kept by Save: yes, anti-cogging block</span> | percent, 0-200 (clamped). Default 100 |
| 43 | The anti-cogging identification on the drive: one motor turn forward and one back in velocity mode at the speed of 44. The shaft must be free to turn. A command from a host or an error aborts it. On the Spectral Micro 4 and 5 identify like 1 and 2 (the trim step is skipped); not yet tested on its bench.<br><span class="meta">`PARAM_COGCAL` · Access: set starts or stops a run; read gives its state · Kept by Save: the result, when started with 2, 3 or 5</span> | Write 0 abort, 1 identify, 2 identify and save, 3 encoder table, then anti-cogging, then save all, 4 identify with the current-sense zero trim, 5 the same and save. Read 0 idle, 1 turning forward, 2 turning backward, 3 done (harmonics on), 4 aborted, 5 failed (an error, or not calibrated), 6 failed (the shaft did not turn), 7 a combined run is measuring the encoder table, 8 the combined run's encoder table failed (52 says why), 9 not used, 10 switched off (the encoder table was measured again on its own), 11 done without the trim |
| 44 | The speed the identification turns at.<br><span class="meta">`PARAM_COGCAL_SPEED` · Access: set, read · Kept by Save: no</span> | ticks/s, 100-20000 (clamped). Default 1500 |
| 45 | The cogging current the last identification found, rms.<br><span class="meta">`PARAM_COGCAL_RIPPLE` · Access: read only · Kept by Save: no</span> | 0.1 mA rms |

</div>

### Encoder table

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 52 | Measures the encoder table: the field turns the rotor open loop one shaft turn forward and one back at 2048 ticks/s (about 20 s). The shaft must be free.<br><span class="meta">`PARAM_ENCAL` · Access: set starts or stops a run; read gives its state · Kept by Save: the table, when started with 2 or 3</span> | Write 0 abort, 1 measure and use, 2 measure, use and save, 3 then the anti-cogging and save all. Read 0 idle, 1 turning forward, 2 turning backward, 3 done (in use), 4 aborted, 5 failed (an error, or not calibrated), 6 failed (the rotor did not follow the field), 7 rejected (over 4° peak to peak, or an offset move over 60° electrical) |
| 53 | Corrects the encoder reading with the table.<br><span class="meta">`PARAM_ENCAL_USE` · Access: set, read · Kept by Save: yes, encoder block</span> | 1 on, 0 off; 1 only when a table was measured; refused while one is being measured |
| 54 | The table's error, peak to peak (0 without a table).<br><span class="meta">`PARAM_ENCAL_PP` · Access: read only · Kept by Save: with the table</span> | 0.01° of the shaft |
| 55 | The once-per-turn part of the error, its amplitude (mostly a magnet off the axis).<br><span class="meta">`PARAM_ENCAL_ONCE` · Access: read only · Kept by Save: with the table</span> | 0.01° of the shaft |
| 56 | No effect on the Spectral Micro: `#Cal` always runs the encoder table and the anti-cogging, and `#Calonly` never does. It stays so that the parameter numbers match STEPFOC.<br><span class="meta">`PARAM_AFTER_CAL` · Access: set, read · Kept by Save: yes, encoder block</span> | 0, 1 or 2 (outside: refused). Default 0 |
| 57 | How far the last encoder-table run moved the electrical offset.<br><span class="meta">`PARAM_ENCAL_OFFSET` · Access: read only · Kept by Save: no</span> | 0.1° electrical |

</div>

### Capture and histogram

The signal numbers: 0 none, 1 measured Iq (mA), 2 measured Id (mA), 3 Iq setpoint with the anti-cogging (mA), 4 speed (ticks/s, saturates at ±32767), 5 speed ÷ 16, 6 position (ticks, the low 16 bits), 7 position error (ticks), 8 electrical angle (0-16383 per electrical turn, from the encoder alone), 9 encoder (0-16383 per motor turn), 10 Vbus (10 mV), 11 and 12 the two current-sense readings (counts after the zero), 13 the control interrupt's time (µs), 14 the anti-cogging feedforward (mA), 15 the Iq setpoint without the anti-cogging (mA), 16 the Uq setpoint (mV), 17 and 18 the d and q voltage the output transform received (mV). None of these settings is saved.

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 24 | The signal of channel A, which is also the trigger channel.<br><span class="meta">`PARAM_CAPTURE_SOURCE_A` · Access: set, read · Kept by Save: no</span> | signal 0-18 (outside: 0). Default 4, speed |
| 25 | The signal of channel B.<br><span class="meta">`PARAM_CAPTURE_SOURCE_B` · Access: set, read · Kept by Save: no</span> | signal 0-18 (outside: 0). Default 1, Iq |
| 26 | The signal of channel C.<br><span class="meta">`PARAM_CAPTURE_SOURCE_C` · Access: set, read · Kept by Save: no</span> | signal 0-18 (outside: 0). Default 8, electrical angle |
| 27 | One sample every N control loops of 200 µs.<br><span class="meta">`PARAM_CAPTURE_DIVIDER` · Access: set, read · Kept by Save: no</span> | control loops per sample, 1-65535 (clamped). Default 1 |
| 28 | 1 to 4 clear the buffer and arm a capture; 0 stops one and keeps what was recorded. The error trigger fires when the error flag rises, a watchdog trip included; an error already present does not fire it.<br><span class="meta">`PARAM_CAPTURE_TRIGGER` · Access: set, read · Kept by Save: no</span> | 0 stop, 1 now, 2 on an error, 3 channel A rising through the level, 4 falling through it (outside: 0) |
| 29 | The level of triggers 3 and 4.<br><span class="meta">`PARAM_CAPTURE_LEVEL` · Access: set, read · Kept by Save: no</span> | channel A's unit, -32768 to 32767 (saturated). Default 0 |
| 30 | How many samples from before the trigger the capture keeps.<br><span class="meta">`PARAM_CAPTURE_PRETRIGGER` · Access: set, read · Kept by Save: no</span> | samples, 0-1023 (clamped). Default 0 |
| 31 | Where the capture stands.<br><span class="meta">`PARAM_CAPTURE_STATE` · Access: read only · Kept by Save: no</span> | 0 idle, 1 armed, 2 recording, 3 done |
| 32 | The samples readable with buffer kind 0.<br><span class="meta">`PARAM_CAPTURE_COUNT` · Access: read only · Kept by Save: no</span> | samples, 0-1024 |
| 33 | Which sample of the read-out is the trigger sample.<br><span class="meta">`PARAM_CAPTURE_TRIGGER_INDEX` · Access: read only · Kept by Save: no</span> | sample index; -1 before a trigger |
| 34 | 1 or 2 clear the histogram and start it; 0 stops it and keeps the data readable.<br><span class="meta">`PARAM_HIST_X` · Access: set, read · Kept by Save: no</span> | 0 off, 1 electrical angle, 2 encoder (256 bins each; outside: 0) |
| 35 | The signal summed per bin. Set it before 34.<br><span class="meta">`PARAM_HIST_Y` · Access: set, read · Kept by Save: no</span> | signal 0-18 (outside: 0). Default 3, Iq setpoint |
| 36 | Samples summed since the start. The histogram stops by itself when one bin holds 65535.<br><span class="meta">`PARAM_HIST_SAMPLES` · Access: read only · Kept by Save: no</span> | samples |
| 39 | The samples per channel a capture holds.<br><span class="meta">`PARAM_CAPTURE_LENGTH` · Access: read only · Kept by Save: —</span> | 1024 |

</div>

### Sound

None of the sound settings is saved; see [Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/sound/).

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 80 | What the sound is doing; a host that refills the queue or the sample buffer reads it.<br><span class="meta">`PARAM_SOUND_STATE` · Access: read only · Kept by Save: —</span> | bits 0-7 events queued, 8-18 samples buffered, 24 a tone sounds, 25 the queue plays, 26 samples play, 27 the samples ran dry |
| 81 | The sound's voltage at most, all tones and samples together.<br><span class="meta">`PARAM_SOUND_LIMIT_MV` · Access: set, read · Kept by Save: no: 2000 at every start-up</span> | mV, 0-6000 (outside: refused). Default 2000; 0 refuses sound and stops what plays |
| 82 | Which axis carries the sound. The q axis makes torque, a small ripple at the tone's pitch, and was much louder on the bench; the d axis makes no torque and is quieter.<br><span class="meta">`PARAM_SOUND_AXIS` · Access: set, read · Kept by Save: no: 1 at every start-up</span> | 1 the q axis (default), 0 the d axis (outside: refused) |

</div>

### Status

<div class="ref-table params" markdown>

| No. | What it is | Value |
|---|---|---|
| 79 | What is in force and what is running, one bit each.<br><span class="meta">`PARAM_FEATURES` · Access: read only · Kept by Save: —</span> | bits, see What is in force |
| 83 | The stack margin: RAM between the heap and the stack that the stack has not used since start-up (setup() fills it with a pattern at its end, and this counts the bytes the pattern is still in). The stack needs about 1.5 to 2 KB of the about 7 KB there are; a value far below that means the drive is short of RAM.<br><span class="meta">`PARAM_STACK_UNUSED` · Access: read only · Kept by Save: —</span> | bytes; -1 if it was not measured |
| 84 | The git commit the firmware was built from. `#Info` prints it as `Build:`, with a `+` for bit 28.<br><span class="meta">`PARAM_BUILD_COMMIT` · Access: read only · Kept by Save: —</span> | the commit's first 7 hex digits as a number (bits 0-27); bit 28 set: built with uncommitted changes; 0 when git was not available at the build |
| 85 | When the firmware was built.<br><span class="meta">`PARAM_BUILD_TIME` · Access: read only · Kept by Save: —</span> | Unix seconds, UTC; 0 when the build did not set it |
| 86 | This board: the chip's factory-unique 96-bit number folded into 32 bits. It never changes, also not with a new firmware or `#Default`. `#Info` prints it as `Board ID:`, 8 hex digits. It is not the bootloader's board ID (0 to 13).<br><span class="meta">`PARAM_BOARD_ID` · Access: read only · Kept by Save: —</span> | 32 bits, read as unsigned |
| 87 | A new number at every successful calibration, so a host can tell one calibration from the next. Send_Save_config keeps it, and `#Default` sets it back to 0. `#Info` prints it as `Calibration ID:`, 8 hex digits.<br><span class="meta">`PARAM_CALIBRATION_ID` · Access: read only · Kept by Save: yes, settings block 2</span> | 32 bits, read as unsigned; 0 before the first calibration |
| 93 | The gripper's stroke between positions 0 and 255, from its last calibration ([Gripper mode](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/gripper-mode/#calibrating-the-gripper)). Added in firmware 110.<br><span class="meta">`PARAM_GRIPPER_STROKE` · Access: read only · Kept by Save: no: the gripper calibrates after every power-up</span> | ticks; 0 while the gripper is not calibrated since power-up |

</div>

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
| 24 | sound is playing ([Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/sound/)) |

Bits 18, 19 and 25 to 31 are 0.

## Reading the capture

A capture records three signals inside the control loop, one sample every *divider* loops, 1024 samples per
channel. It starts when parameter 28 is written: at once (1), when the error flag rises (2, a watchdog trip
included), or when channel A rises (3) or falls (4) through the level of parameter 29. Parameter 30 keeps that many
samples from before the trigger. [Status and diagnostics](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/diagnostics/) shows a whole capture.

1. Set the signals (24, 25, 26), the divider (27), the pre-trigger (30) and, for 3 and 4, the level (29).
2. Write the trigger (28). Parameter 31 reads 1 (armed), 2 (recording), then 3 (done).
3. Read parameter 32 (samples readable) and 33 (the trigger sample's index, −1 if none).
4. Send_Buffer_Read with kind 0, first 0, count = parameter 32: one Respond_Buffer_Data frame per sample, oldest
   first.

The histogram works the same way with parameters 34 to 36 and kind 1: it adds a signal into 256 bins by the
electrical angle or by the encoder, every control loop, until it is stopped or one bin holds 65535 samples.
