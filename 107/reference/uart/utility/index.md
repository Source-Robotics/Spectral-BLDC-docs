# Status and utility

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#Vmax` | Set/Get | int: voltage in mV | The supply voltage above which a Vbus error is raised. | `Vmax in mV: N` |
| `#Save` | Action |  | Writes the configuration to the EEPROM. Do it after calibration and after tuning. | `Save` |
| `#Reset` | Action |  | Resets the driver. From firmware 105 the reset lands in the bootloader, which waits 2 s for a flashing host and then starts the firmware again. | nothing |
| `#Tlim` | Set/Get | int: temperature in °C | The temperature at which the temperature error is raised; 75 by default. | `Temp limit N` |
| `#Default` | Action |  | Writes the factory defaults to the EEPROM, including the serial number, hardware version and batch date, and clears the gripper flag, heartbeat and watchdog. Back those up first. | `Loaded default config!` |
| `#Temp` | Get |  | Prints the thermistor temperature. | °C, or `Temp Off` while the thermistor is disabled |
| `#Term` | Set/Get | int: 0 or 1 | Enables the thermistor measurement and the temperature error (off by default). | the setting |
| `#Mode` | Get |  | Prints the control mode. | `Idle mode`, `Position control`, `Speed control`, `Current control`, `PD control`, `Open loop`, `Gripper mode`, `Gripper calib mode` |
| `#Vbus` | Get |  | Prints the supply voltage. | mV |
| `#Error` | Get |  | Prints which errors are active. | `No errors!` or `In error state!` followed by one line per active error |
| `#Clear` | Action |  | Clears the errors and goes to idle. An error whose cause is still present comes straight back; a calibration error is cleared only by calibrating (or `#Calibrated 1`). Enters **idle** mode. | `Clear errors` |
| `#Iabc` | Get |  | Prints the phase currents. | `Ia`, `Ib` in mA |
| `#PWM` | Get |  | Prints the PWM duty values. | the duties |
| `#Help` | Action |  | Prints a short command reference. Added in firmware 106. | the reference |
| `#Info` | Get |  | Prints the driver's identity and state: hardware and firmware version, serial number, motor parameters, calibration, errors. | the report |
| `#Param` | Get |  | Prints every gain of every loop. | the gains |
| `#Cyc` | Set/Get | int: interval in ms (0 = off) | Sends position, speed and Iq on its own every interval: `$ <position> <speed> <Iq>`; for BetterSerialPlotter. | `Cyclic disabled` when turned off |
| `#Cyca` | Set/Get | int: interval in ms (0 = off) | Like Cyc, in the Arduino plotter format `Position:x,Speed:y,Iq:z`. | `Cyclic disabled` when turned off |
| `#CANID` | Set/Get | int: 0 to 13 | The CAN node ID. Use 0 to 13: the firmware accepts 14 and 15, but the bootloader reserves them and a driver on one of those cannot be updated over CAN. Setting the ID also sets the bootloader's board ID. Kept over a power cycle after Save. | the ID, or `Invalid CAN ID` |
| `#SERNUM` | Set/Get | int: number | The serial number stored in the EEPROM. | `Serial number is: N` |
| `#Activate` | Action |  | Sets the activated flag. | `Controller activated` |
| `#Pullconfig` | Get |  | Prints the whole configuration on one line, for Motor GUI. | the configuration |
| `#LED` | Set/Get | int: 0 or 1 | Turns the status LED on or off. | the LED state |
