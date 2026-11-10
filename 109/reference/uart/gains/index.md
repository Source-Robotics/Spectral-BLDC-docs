# Gains and limits

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#Vlim` | Set/Get | int: voltage in mV | The voltage limit of the current loops (Ud and Uq); 0 means use the supply voltage. | the current limit in mV |
| `#Vlimit` | Set/Get | int: speed in encoder ticks/s | The speed limit: the speed the position loop may command, and the largest velocity setpoint. (The velocity integrator is clamped to the current limit.) The magnitude of a negative number is taken. | the current limit |
| `#Kpp` | Set/Get | float: gain | Kp of the position loop. | the current value |
| `#KP` | Set/Get | float: gain | KP of the impedance (PD) loop. | the current value |
| `#KD` | Set/Get | float: gain | KD of the impedance (PD) loop. | the current value |
| `#Kpv` | Set/Get | float: gain | Kp of the velocity loop. | the current value |
| `#Kpiq` | Set/Get | float: gain | Kp of the Iq current loop; also sets Kpid. | the current value |
| `#Kpid` | Set/Get | float: gain | Kp of the Id current loop. | the current value |
| `#Kiv` | Set/Get | float: gain | Ki of the velocity loop. | the current value |
| `#Kiiq` | Set/Get | float: gain | Ki of the Iq current loop; also sets Kiid. | the current value |
| `#Kiid` | Set/Get | float: gain | Ki of the Id current loop. | the current value |
| `#Ilim` | Set/Get | int: current in mA | The Iq current limit. Set it to the rated phase current of your motor; the firmware clamps it to 2800 mA and takes the magnitude of a negative number. | the current limit |
| `#Cbw` | Set/Get | float: bandwidth in Hz, 10 to 500 | The current loop bandwidth. From firmware 109 setting it computes Kpiq and Kiiq at once from R and L, the way calibration does, and prints them (the same as parameter 49); a value outside 10-500, or with R or L at 0, changes nothing. Not saved: 160 Hz after a power cycle, but the gains it set are kept by Save. | the bandwidth, then `Kp_iq = …, Ki_iq = …` |
| `#Rstint` | Set/Get | int: 0 or 1 | Whether the integral accumulators are reset on every new setpoint. | the setting |
