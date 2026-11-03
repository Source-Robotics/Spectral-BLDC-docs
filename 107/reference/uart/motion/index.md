# Motion

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#Iq` | Set/Get | float: current setpoint in mA | Current (torque) control with the given Iq setpoint. Enters **current** mode. | the measured Iq in mA |
| `#Id` | Set/Get | float: current setpoint in mA | Sets the Id setpoint; normally left at 0. | the measured Id in mA |
| `#Uq` | Set/Get | int: voltage in mV | Voltage-torque mode with the given q-axis voltage (no current loop). Enters **voltage torque** mode. | the Uq setpoint in mV |
| `#Ud` | Set/Get | int: voltage in mV | The d-axis voltage used in voltage-torque mode; does not change the mode. | the Ud setpoint in mV |
| `#V` | Set/Get | int: speed setpoint in encoder ticks/s | Velocity control with the given speed. Enters **velocity** mode. | the measured speed in ticks/s |
| `#P` | Set/Get | int: position setpoint in encoder ticks | Position control to the given position. Enters **position** mode. | the measured position in ticks |
| `#PD` | Set/Get | int: position setpoint in encoder ticks | Impedance (PD) control around the given position with the gains KP and KD. Enters **PD** mode. | the measured position in ticks |
| `#PDV` | Set/Get | int: speed setpoint in encoder ticks/s | The speed setpoint of the PD loop. | the PD speed setpoint |
| `#PDI` | Set/Get | int: current feedforward in mA | The current feedforward of the PD loop. | the PD current feedforward |
| `#Idle` | Action |  | Goes to idle; the motor coasts or brakes as set by Brake. Enters **idle** mode. | `Idle` |
| `#Brake` | Set/Get | int: 0 or 1 | What the motor does in idle: 1 brakes (the phases are shorted through the driver), 0 coasts (the phases are open, the default). Takes effect once the driver is idle, so send Idle first. Not saved: the driver coasts again after a power cycle. An error always disables the motor, which then coasts. The braking current is not limited, see Control modes. Added in firmware 107. | the setting |
| `#Close` | Action |  | Leaves open loop and goes back to closed-loop idle. Enters **idle** mode. | nothing |
| `#Openloop` | Set/Get | float: electrical speed in rad/s | Turns the stator field at the given electrical speed without the encoder in the loop, with the voltage set by Openv. Without a number it still starts the motor, at the stored speed: `#Openloop` alone is not a query. The speed is the same setting as `#Opens`. Enters **open loop** mode. | the open-loop speed |
