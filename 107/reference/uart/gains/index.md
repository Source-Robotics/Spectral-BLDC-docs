# Gains and limits

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#Vlim` | Set/Get | int: voltage in mV | The voltage limit of the current loops (Ud and Uq); 0 means use the supply voltage. | the current limit in mV |
| `#Vlimit` | Set/Get | int: speed in encoder ticks/s | The speed limit; the velocity integrator is clamped to it. | the current limit |
| `#Kpp` | Set/Get | float: gain | Kp of the position loop. | the current value |
| `#KP` | Set/Get | float: gain | KP of the impedance (PD) loop. | the current value |
| `#KD` | Set/Get | float: gain | KD of the impedance (PD) loop. | the current value |
| `#Kpv` | Set/Get | float: gain | Kp of the velocity loop. | the current value |
| `#Kpiq` | Set/Get | float: gain | Kp of the Iq current loop; also sets Kpid. | the current value |
| `#Kpid` | Set/Get | float: gain | Kp of the Id current loop. | the current value |
| `#Kiv` | Set/Get | float: gain | Ki of the velocity loop. | the current value |
| `#Kiiq` | Set/Get | float: gain | Ki of the Iq current loop; also sets Kiid. | the current value |
| `#Kiid` | Set/Get | float: gain | Ki of the Id current loop. | the current value |
| `#Ilim` | Set/Get | int: current in mA | The Iq current limit. Set it to the rated phase current of your motor; the firmware clamps it to 2800 mA. | the current limit |
| `#Cbw` | Set/Get | float: bandwidth in Hz | The current loop bandwidth calibration uses to compute Kpiq and Kiiq. | the bandwidth |
| `#Rstint` | Set/Get | int: 0 or 1 | Whether the integral accumulators are reset on every new setpoint. | the setting |
