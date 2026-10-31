# Calibration and motor parameters

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#R` | Set/Get | float: resistance in Ω | The phase resistance of the motor, measured by Cal; it can also be set by hand. | the current value |
| `#L` | Set/Get | float: inductance in H | The phase inductance of the motor, measured by Cal; it can also be set by hand. | the current value |
| `#Kt` | Set/Get | float: Nm/A | The torque constant, found by calibration. | the current value |
| `#KV` | Set/Get | float: rpm/V | The velocity constant, found by calibration. | the current value |
| `#Flux` | Set/Get | float: Wb | The flux linkage, found by calibration. Not reachable over UART: the parser accepts `#flux` (lowercase) but the handler expects `Flux`, so neither spelling works. | the current value |
| `#Cal` | Action |  | Runs the calibration routine (see Calibration): it measures R and L, finds the pole pairs, the phase order and the angle offset, and measures Kt, KV and the flux linkage. | the calibration log |
| `#Offset` | Set/Get | float: angle in rad | The angle offset between encoder zero and electrical zero, found by calibration. | the current value |
| `#Iqoffset` | Set/Get | int: current in mA | The current used by the angle-offset search. | the current value |
| `#Magnet` | Get |  | Reads the encoder's magnet status. | `Magnet Good` or `Magnet Bad` |
| `#Dir` | Set/Get | int: 0 or 1 | The counting direction of the encoder (1 is the default). | the current value |
| `#Phase` | Get |  | Prints the phase order found by calibration. | `Phase order is: N` |
| `#Resv` | Set/Get | int: voltage in mV | The voltage the resistance test of Cal starts at; it rises until the power reaches Calpwr. | the current value |
| `#Calpwr` | Set/Get | float: power in W | The power the resistance and inductance tests of Cal may dissipate in the motor. | the current value |
| `#Openv` | Set/Get | int: voltage in mV | The voltage of the open-loop spin, in calibration and with Openloop. | the current value |
| `#Opens` | Set/Get | float: electrical speed in rad/s | The speed of the open-loop spin in calibration. | the current value |
| `#Vp` | Set/Get | int: voltage in mV | The voltage of the phase-order search in calibration. | the current value |
| `#Calibrated` | Set/Get | int: 0 or 1 | The calibrated flag. `#Calibrated 1` clears a calibration error without calibrating; the motor may still be uncalibrated. | the flag |
| `#PP` | Set/Get | int: pole pairs | The motor's pole pairs, found by Cal; they can also be set by hand. | the current value |
