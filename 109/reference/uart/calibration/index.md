# Calibration and motor parameters

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#R` | Set/Get | float: resistance in Ω | The phase resistance of the motor, measured by Cal; it can also be set by hand. Also parameter 76, in mΩ. | the current value |
| `#L` | Set/Get | float: inductance in H | The phase inductance of the motor, measured by Cal; it can also be set by hand. Also parameter 77, in µH. | the current value |
| `#Kt` | Set/Get | float: Nm/A | The torque constant, found by calibration. | the current value |
| `#KV` | Set/Get | float: rpm/V | The velocity constant, found by calibration. | the current value |
| `#Flux` | Set/Get | float: Wb | The flux linkage, found by calibration. Works over UART from firmware 109; the parser of 107 and older accepted only the lowercase `#flux`, which had no handler. | the current value |
| `#Calonly` | Action |  | The calibration alone: like Cal, but nothing follows it. Save afterwards with Save. Added in firmware 109. Enters **idle** mode. | the calibration log |
| `#Cal` | Action |  | Runs the calibration routine (see Calibration): it measures R and L, finds the pole pairs, the phase order and the angle offset, and measures Kt, KV and the flux linkage. It uses its own 1600 mA current limit for its steps; from firmware 109 it puts the limit that was in force back when it ends. From firmware 109, when it succeeds, the encoder table and then the anti-cogging follow by themselves, and everything is saved (about a minute; keep the shaft free). Enters **idle** mode. | the calibration log |
| `#Calonly` | Action |  | The calibration alone: like Cal, but nothing follows it. Save afterwards with Save. Added in firmware 109. Enters **idle** mode. | the calibration log |
| `#Offset` | Set/Get | float: angle in rad | The angle offset between encoder zero and electrical zero, found by calibration. | the current value |
| `#Iqoffset` | Set/Get | int: current in mA | The current used by the angle-offset search and the commutation check of Cal, 300 mA by default. Not saved. | the current value |
| `#Magnet` | Get |  | Reads the encoder's magnet status. | `Magnet Good` or `Magnet Bad` |
| `#Dir` | Set/Get | int: 0 or 1 | The base direction of the encoder and phase mapping. Calibration always sets it to 1 (0 after `#Default`); the direction it finds is the commutation direction, which `#Info` prints. | the current value |
| `#Phase` | Get |  | Prints the phase order found by calibration. | `Phase order is: N` |
| `#Resv` | Set/Get | int: voltage in mV | The voltage the resistance test of Cal starts at; it rises until the power reaches Calpwr. Not saved. | the current value |
| `#Calpwr` | Set/Get | float: power in W | The power the resistance and inductance tests of Cal may dissipate in the motor. Not saved. | the current value |
| `#Openv` | Set/Get | int: voltage in mV | The voltage of the open-loop spin, in calibration and with Openloop. Not saved. | the current value |
| `#Opens` | Set/Get | float: electrical speed in rad/s | The speed of the open-loop spin in calibration; the same setting as the speed of `#Openloop`. | the current value |
| `#Vp` | Set/Get | int: voltage in mV | The voltage of the phase-order search in calibration. Not saved. | the current value |
| `#Encal` | Set/Get | nothing, or save, all, stop, on, off, state | The encoder table (see Encoder table and anti-cogging). Alone it measures the table and uses it: the field turns the rotor open loop one shaft turn each way at 2048 ticks/s, about 20 s, with the shaft free. `save` also saves; `all` then identifies the anti-cogging and saves both; `stop` aborts; `on` and `off` switch the correction (on only with a measured table, and not while a run turns the motor); `state` or any other word only prints. The same as parameters 52 and 53. Added in firmware 109; not yet tested on a Spectral Micro. | `Encoder table: <state>`, then the table's error in degrees |
| `#Cogcal` | Set/Get | nothing, or save, trim, stop, state | The anti-cogging identification on the drive (see Encoder table and anti-cogging): one motor turn forward and one back in velocity mode at parameter 44's speed (1500 ticks/s, about 22 s), the shaft free to turn. `save` also saves; `stop` aborts, also the encoder part of a combined run; `state` or any other word only prints. `trim` identifies like the plain command on the Spectral Micro: its firmware skips the current-sense trim. Added in firmware 109; not yet tested on a Spectral Micro. | `Anti-cogging identification: <state>`, the speed and the identified cogging in mA rms, and the harmonics when done |
| `#Calibrated` | Set/Get | int: 0 or 1 | The calibrated flag. `#Calibrated 1` clears a calibration error without calibrating; the motor may still be uncalibrated. | the flag |
| `#PP` | Set/Get | int: pole pairs | The motor's pole pairs, found by Cal; they can also be set by hand. Also parameter 78: 1-49, only while idle (50 and more would read as a STEPFOC calibration); from 109 `#PP` answers `PP: not taken (1-49, and only while idle)` otherwise. | the current value |
