# Status and utility

| Command | Kind | Argument | What it does | Response |
|---|---|---|---|---|
| `#Vmax` | Set/Get | int: voltage in mV | The supply voltage above which a Vbus error is raised: 29000 mV after `#Default`. | `Vmax in mV: N` |
| `#Save` | Action |  | Writes the configuration to the EEPROM. Do it after calibration and after tuning. | `Save` |
| `#Reset` | Action |  | Resets the driver. From firmware 104 the reset lands in the bootloader, which waits 2 s for a flashing host and then starts the firmware again. | nothing |
| `#Tlim` | Set/Get | int: temperature in °C | The temperature at which the temperature error is raised; 75 by default. | `Temp limit N` |
| `#Default` | Action |  | Writes the factory defaults to the EEPROM and loads them: the calibration is erased (Not calibrated), the CAN node ID goes back to 0, the gripper flag, heartbeat and watchdog are cleared, the hardware version and batch date are set to 1 and 24092024, and 1111 is stored as the serial number. Note the values first. | `Loaded default config!` |
| `#Temp` | Get |  | Prints the thermistor temperature. | °C, or `Temp Off` while the thermistor is disabled |
| `#Term` | Set/Get | int: 0 or 1 | Enables the thermistor measurement and the temperature error (off by default). | the setting |
| `#Mode` | Get |  | Prints the control mode. In voltage-torque mode (`#Uq`) it prints nothing. | `Idle mode`, `Position control`, `Speed control`, `Current control`, `PD control`, `Open loop`, `Gripper mode`, `Gripper calib mode` |
| `#Vbus` | Get |  | Prints the supply voltage. | mV |
| `#Error` | Get |  | Prints which errors are active. | `No errors!` or `In error state!`, then one line per active error (see Errors and LED states), and `FAULT pin is HIGH` while the driver stage's fault pin is active |
| `#Clear` | Action |  | Clears the errors and goes to idle. An error whose cause is still present comes straight back; a calibration error is cleared only by calibrating (or `#Calibrated 1`). Enters **idle** mode. | `Clear errors` |
| `#Iabc` | Get |  | Prints the phase currents. | `Ia`, `Ib`, `Ic` in mA |
| `#PWM` | Get |  | Prints the PWM duty values. | the duties |
| `#Help` | Action |  | Prints a short command reference. Added in firmware 106. | the reference |
| `#Info` | Get |  | Prints the driver's identity and the motor: hardware version, batch date, firmware version, ISR time, CAN ID, calibrated or not, temperature, Vbus, Dir, phase order, commutation direction, the speeds of the calibration spin, pole pairs, R, L, Kt and KV. The serial number is `#SERNUM`, the gains `#Param`, the errors `#Error`. | the report |
| `#Param` | Get |  | Prints every gain of every loop. | the gains |
| `#Cyc` | Set/Get | int: interval in ms (0 = off) | Sends position, speed and Iq on its own every interval: `$ <position> <speed> <Iq>`; for BetterSerialPlotter. | `Cyclic disabled` for `#Cyc` without a number; `#Cyc 0` stops the output without an answer |
| `#Cyca` | Set/Get | int: interval in ms (0 = off) | Like Cyc, in the Arduino plotter format `Position:x,Speed:y,Iq:z`. | `Cyclic disabled` for `#Cyca` without a number; `#Cyca 0` stops the output without an answer |
| `#CANID` | Set/Get | int: 0 to 13 | The CAN node ID. Use 0 to 13: the firmware accepts 14 and 15, but the bootloader reserves them and a driver on one of those cannot be updated over CAN. Kept over a power cycle after Save, which also copies it into the bootloader's board ID. | the ID, or `Invalid CAN ID` |
| `#SERNUM` | Set/Get | int: number | The serial number. Save writes it to the EEPROM, but the firmware does not read it back at power-up: after a power cycle the driver reports 1. | `Serial number is: N` |
| `#Activate` | Action |  | Sets the controller's activated flag (bit 6 of byte 1 of Send_Respond_State_of_Errors). It is not the gripper's activate bit, which `#Gripact` and Send_gripper_data_pack set. | `Controller activated` |
| `#Pullconfig` | Get |  | Prints the whole configuration on one line, for Motor GUI. | the configuration |
| `#LED` | Set/Get | int: 0 or 1 | Turns the status LED on or off. | the LED state |
