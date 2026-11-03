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

Writes the current configuration (gains, limits, calibration, CAN ID, heartbeat, watchdog, gripper flag) to the EEPROM, and copies the CAN ID into the bootloader's board ID.

The driver does not answer this command.

---

### Send_Reset

<div class="cmd-facts" markdown><span class="fact">ID 14</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_Reset()`</span></div>

Resets the driver. From firmware 104 the reset lands in the bootloader, which waits 2 s for a flashing host and then starts the firmware again; this is how a firmware update begins.

The driver does not answer this command.

---

### Send_Clear_Error

<div class="cmd-facts" markdown><span class="fact">ID 1</span><span class="fact">host → driver</span><span class="fact">0 bytes</span><span class="fact">Python: `Send_Clear_Error()`</span></div>

Clears the error flags and goes to idle. An error whose cause is still present comes straight back. A calibration error is cleared only by calibrating.

The driver does not answer this command.

---

### Send_Watchdog

<div class="cmd-facts" markdown><span class="fact">ID 15</span><span class="fact">host → driver</span><span class="fact">5 bytes</span><span class="fact">Python: `Send_Watchdog()`</span></div>

Sets the watchdog. The motion commands (Send_data_pack_1, Send_data_pack_PD, Send_gripper_data_pack) and the status requests (the Send_Respond_ remote frames) reset it; the other frames and UART commands do not. When the time runs out the driver reports a watchdog error and disables the motor, which then coasts. 0 turns it off (the default). The action byte is stored but not acted on by this firmware. The setting is kept by Send_Save_config and there is no UART command for it: to turn off a saved watchdog, send 0 over CAN and save, or use `#Default`.

**5 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Time | unsigned 32-bit | ms; 0 = off |
| 4 |  | Action | unsigned 8-bit | 0 idle, 1 hold, 2 brake (stored only) |

The driver does not answer this command.

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

<div class="cmd-facts" markdown><span class="fact">ID 35</span><span class="fact">host → driver</span><span class="fact">2 bytes</span></div>

Sets boolean settings that have no command of their own: a mask byte says which settings the frame touches, a value byte gives their new values; settings outside the mask are left alone. Bit 0 is the idle behaviour: 1 brake (phases shorted), 0 coast (the default). The setting is not saved: the driver coasts again after a power cycle. Braking applies only in idle without an error; an error always disables the motor, which then coasts. The braking current is not limited, see Control modes. Added in firmware 107 (STEPFOC 107). The Python library has no call for it yet.

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
