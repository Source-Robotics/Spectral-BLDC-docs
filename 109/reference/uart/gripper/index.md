# Gripper

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#Gripper` | Set/Get | int: 0 or 1 | Whether this driver is a gripper. Save it; `#Default` clears it. | the flag |
| `#Gripcal` | Action |  | Starts the gripper calibration (the jaws find their end stops). Enters **gripper calibration** mode. | `Gripper calibration!` |
| `#Gripinfo` | Get |  | Prints the gripper state: whether the driver is a gripper, calibrated, activated, the position, speed and current setpoints, the E-stop, action and object-detection status, and the end stops. | the report |
| `#Gripstop` | Set/Get | int: 0 or 1 | The gripper E-stop bit. | the bit |
| `#Gripact` | Set/Get | int: 0 or 1 | The activate bit. | the bit |
| `#Gripcur` | Set/Get | int: current in mA | The current limit of gripper moves. From firmware 109 a gripper move uses its magnitude and stops at 2800 mA; see the gripper manual for the safe range. | the setpoint |
| `#Gripvel` | Set/Get | int: 0 to 255 | The speed setpoint of gripper moves. | the setpoint |
| `#Grippos` | Set/Get | int: 0 (open) to 255 (closed) | The position setpoint; also activates the gripper, sets the action bit and goes to gripper mode. Enters **gripper** mode. | the current position |
