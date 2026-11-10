# System

Identity, saving, resetting, errors, the watchdog, the heartbeat and the settings.

### Send_CAN_ID

<div class="cmd-facts" markdown><span class="fact">ID 11</span><span class="fact">host → driver</span><span class="fact">1 bytes</span><span class="fact">Python: `Send_CAN_ID()`</span></div>

Gives the driver a new node ID, 0 to 13 (the firmware accepts up to 15, but the bootloader reserves 14 and 15: a driver on one of those cannot be updated over CAN). The driver answers to the new ID at once. The ID is kept over a power cycle only after Send_Save_config, and saving is also what copies it into the bootloader's board ID.

**1 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | ID | unsigned 8-bit | 0 to 13 (14 and 15 are accepted but reserved by the bootloader) |

The driver does not answer this command.

---

### Send_ESTOP

<div class="cmd-facts" markdown><span class="fact">ID 0</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_ESTOP()`</span></div>

Stops the motor and raises the E-stop error, which stays until Send_Clear_Error.

The driver does not answer this command.

---

### Send_Idle

<div class="cmd-facts" markdown><span class="fact">ID 12</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_Idle()`</span></div>

Puts the driver in idle mode: the motor coasts, or brakes when Send_Settings or `#Brake 1` asked for it.

The driver does not answer this command.

---

### Send_Save_config

<div class="cmd-facts" markdown><span class="fact">ID 13</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_Save_config()`</span></div>

Writes the current configuration (gains, limits, calibration, CAN ID, heartbeat, watchdog, gripper flag) to the EEPROM, and copies the CAN ID into the bootloader's board ID. From firmware 109 it also writes the tool id and the watchdog fallback (settings block 2), the anti-cogging set with its mode and scale, and the encoder table with its on/off flag, parameter 56 and the current-sense zero trims, each block with its own checksum; of the two large blocks only the 16-byte pages that changed are written. Not kept: the idle behaviour of Send_Settings, the current loop bandwidth, and every parameter the parameter table marks as not kept. A drive stopped by the product lock writes nothing.

The driver does not answer this command.

---

### Send_Reset

<div class="cmd-facts" markdown><span class="fact">ID 14</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_Reset()`</span></div>

Resets the driver. From firmware 104 the reset lands in the bootloader, which waits 2 s for a flashing host and then starts the firmware again; this is how a firmware update begins.

The driver does not answer this command.

---

### Send_Clear_Error

<div class="cmd-facts" markdown><span class="fact">ID 1</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_Clear_Error()`</span></div>

Clears the error flags and goes to idle; it also ends a watchdog hold or descend. An error whose cause is still present comes straight back. A calibration error is cleared only by calibrating.

The driver does not answer this command.

---

### Send_Watchdog

<div class="cmd-facts" markdown><span class="fact">ID 15</span><span class="fact">host → driver</span><span class="fact">5 bytes</span><span class="fact">Python: `Send_Watchdog()`</span></div>

Sets the watchdog. The motion commands (Send_data_pack_1, Send_data_pack_PD, Send_gripper_data_pack) and the requests the driver answers (the Send_Respond_ remote frames, Send_Get_Parameter, Send_Buffer_Read) reset it; the other frames (Send_Parameter among them) and UART commands do not. When the time runs out the driver reports a watchdog error and does what the action byte says. 0 turns it off (the default). From firmware 109 the driver acts on the action byte, but only when the watchdog is the only active error: any other error gets the legacy response, the motor disabled and coasting. Hold and descend run for the fallback time (parameter 2, 2 s by default), then the after-action (parameter 5); they start only if the driver was in position, velocity, current, PD or gripper mode, otherwise the driver gives the legacy response and the motor coasts. Setting the time starts a fresh window, and a negative time means off. [The watchdog](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/watchdog/) explains each action. The setting is kept by Send_Save_config. The same values are parameters 6 and 7, which `#Par` reaches over UART: to turn off a saved watchdog, send 0 over CAN or `#Par 6,0`, and save.

**5 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Time | unsigned 32-bit | ms; 0 = off |
| 4 |  | Action | unsigned 8-bit | 0 legacy (the motor disabled, coasting), 1 hold the position, 2 brake (not current-limited), 3 coast, 4 descend at the fallback current and speed; other values act as 0 |

The driver does not answer this command.

Firmware 107 and older store the action byte without acting on it. The Python library sends all five actions from 1.21 ('Idle', 'Hold', 'Brake', 'Coast', 'Descend'); 1.20 and older send only 0, 1 or 2.

---

### Send_Heartbeat_Setup

<div class="cmd-facts" markdown><span class="fact">ID 30</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Heartbeat_Setup()`</span></div>

Sets the heartbeat interval in ms; 0 turns the heartbeat off (the default). Kept by Send_Save_config.

**4 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Interval | unsigned 32-bit | ms; 0 = off |

---

### Send_Settings

<div class="cmd-facts" markdown><span class="fact">ID 35</span><span class="fact">host → driver</span><span class="fact">2 bytes</span><span class="fact">Python: `Send_Settings()`</span></div>

Sets boolean settings that have no command of their own: a mask byte says which settings the frame touches, a value byte gives their new values; settings outside the mask are left alone. Bit 0 is the idle behaviour: 1 brake (phases shorted), 0 coast (the default). The setting is not saved: the driver coasts again after a power cycle. Braking applies only in idle without an error; an error always disables the motor, which then coasts. The braking current is not limited, see Control modes. Added in firmware 107 (STEPFOC 107). The Python library has `Send_Settings(mask, value)` and, for this bit, `Send_Brake_Coast(brake)` from 1.21; 1.20 and older have no call for it.

**2 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | Mask | unsigned 8-bit | bit 0 = write the idle behaviour |
| 1 |  | Value | unsigned 8-bit | bit 0: 1 brake, 0 coast |

The driver does not answer this command.

---

### Send_Cyclic_command

<div class="cmd-facts" markdown><span class="fact">ID 29</span><span class="fact">host → driver</span><span class="fact">not implemented</span></div>

Reserved. The firmware has no handler for this ID and the Python library's call does nothing.

---
