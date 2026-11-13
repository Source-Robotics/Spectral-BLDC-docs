# Calibration and motor parameters

<div class="cmd-index" markdown>[`#Cal`](#cal) [`#Calonly`](#calonly) [`#Encal`](#encal) [`#Cogcal`](#cogcal) [`#R`](#r) [`#L`](#l) [`#PP`](#pp) [`#Kt`](#kt) [`#KV`](#kv) [`#Flux`](#flux) [`#Offset`](#offset) [`#Iqoffset`](#iqoffset) [`#Magnet`](#magnet) [`#Dir`](#dir) [`#Phase`](#phase) [`#Resv`](#resv) [`#Calpwr`](#calpwr) [`#Openv`](#openv) [`#Opens`](#opens) [`#Vp`](#vp) [`#Calibrated`](#calibrated)</div>

### `#Cal` 

<div class="cmd-facts" markdown><span class="fact">Action</span><span class="fact">Enters **idle** mode</span></div>

Runs the calibration routine (see Calibration): it measures R and L, finds the pole pairs, the phase order and the angle offset, and measures Kt, KV and the flux linkage. It uses its own 1600 mA current limit for its steps; from firmware 109 it puts the limit that was in force back when it ends. From firmware 109, when it succeeds, the encoder table and then the anti-cogging follow by themselves, and everything is saved (about a minute; keep the shaft free).

**Response:** the calibration log

---

### `#Calonly` 

<div class="cmd-facts" markdown><span class="fact">Action</span><span class="fact">Enters **idle** mode</span></div>

The calibration alone: like Cal, but nothing follows it. Save afterwards with Save. Added in firmware 109.

**Response:** the calibration log

---

### `#Encal` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> nothing, or save, all, stop, on, off, state</span></div>

The encoder table (see Encoder table and anti-cogging). Alone it measures the table and uses it: the field turns the rotor open loop one shaft turn each way at 2048 ticks/s, about 20 s, with the shaft free. `save` also saves; `all` then identifies the anti-cogging and saves both; `stop` aborts; `on` and `off` switch the correction (on only with a measured table, and not while a run turns the motor); `state` or any other word only prints. The same as parameters 52 and 53. Added in firmware 109; not yet tested on a Spectral Micro.

**Response:** `Encoder table: <state>`, then the table's error in degrees

---

### `#Cogcal` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> nothing, or save, trim, stop, state</span></div>

The anti-cogging identification on the drive (see Encoder table and anti-cogging): one motor turn forward and one back in velocity mode at parameter 44's speed (1500 ticks/s, about 22 s), the shaft free to turn. `save` also saves; `stop` aborts, also the encoder part of a combined run; `state` or any other word only prints. `trim` identifies like the plain command on the Spectral Micro: its firmware skips the current-sense trim. Added in firmware 109; not yet tested on a Spectral Micro.

**Response:** `Anti-cogging identification: <state>`, the speed and the identified cogging in mA rms, and the harmonics when done

---

### `#R` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: resistance in Ω</span></div>

The phase resistance of the motor, measured by Cal; it can also be set by hand. Also parameter 76, in mΩ.

**Response:** the current value

---

### `#L` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: inductance in H</span></div>

The phase inductance of the motor, measured by Cal; it can also be set by hand. Also parameter 77, in µH.

**Response:** the current value

---

### `#PP` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: pole pairs</span></div>

The motor's pole pairs, found by Cal; they can also be set by hand. Also parameter 78: 1-49, only while idle (50 and more would read as a STEPFOC calibration); from 109 `#PP` answers `PP: not taken (1-49, and only while idle)` otherwise.

**Response:** the current value

---

### `#Kt` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: Nm/A</span></div>

The torque constant, found by calibration.

**Response:** the current value

---

### `#KV` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: rpm/V</span></div>

The velocity constant, found by calibration.

**Response:** the current value

---

### `#Flux` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: Wb</span></div>

The flux linkage, found by calibration. Works over UART from firmware 109; the parser of 107 and older accepted only the lowercase `#flux`, which had no handler.

**Response:** the current value

---

### `#Offset` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: angle in rad</span></div>

The angle offset between encoder zero and electrical zero, found by calibration.

**Response:** the current value

---

### `#Iqoffset` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: current in mA</span></div>

The current used by the angle-offset search and the commutation check of Cal, 300 mA by default. Not saved.

**Response:** the current value

---

### `#Magnet` 

<div class="cmd-facts" markdown><span class="fact">Get</span></div>

Reads the encoder's magnet status.

**Response:** `Magnet Good` or `Magnet Bad`

---

### `#Dir` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 or 1</span></div>

The base direction of the encoder and phase mapping. Calibration always sets it to 1 (0 after `#Default`); the direction it finds is the commutation direction, which `#Info` prints.

**Response:** the current value

---

### `#Phase` 

<div class="cmd-facts" markdown><span class="fact">Get</span></div>

Prints the phase order found by calibration.

**Response:** `Phase order is: N`

---

### `#Resv` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: voltage in mV</span></div>

The voltage the resistance test of Cal starts at; it rises until the power reaches Calpwr. Not saved.

**Response:** the current value

---

### `#Calpwr` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: power in W</span></div>

The power the resistance and inductance tests of Cal may dissipate in the motor. Not saved.

**Response:** the current value

---

### `#Openv` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: voltage in mV</span></div>

The voltage of the open-loop spin, in calibration and with Openloop. Not saved.

**Response:** the current value

---

### `#Opens` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: electrical speed in rad/s</span></div>

The speed of the open-loop spin in calibration; the same setting as the speed of `#Openloop`.

**Response:** the current value

---

### `#Vp` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: voltage in mV</span></div>

The voltage of the phase-order search in calibration. Not saved.

**Response:** the current value

---

### `#Calibrated` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 or 1</span></div>

The calibrated flag. `#Calibrated 1` clears a calibration error without calibrating; the motor may still be uncalibrated.

**Response:** the flag

---
