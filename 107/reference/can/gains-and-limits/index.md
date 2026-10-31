# Gains and limits

The commands that set the loop gains and the limits. None of them is answered; save with Send_Save_config.

### Send_PD_Gains

<div class="cmd-facts" markdown><span class="fact">ID 16</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_PD_Gains()`</span></div>

Sets KP and KD, the gains of the impedance (PD) loop. Keep them with Send_Save_config.

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | KP | float 32 |  |
| 4-7 |  | KD | float 32 |  |

The driver does not answer this command.

---

### Send_Current_Gains

<div class="cmd-facts" markdown><span class="fact">ID 17</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Current_Gains()`</span></div>

Sets Kp and Ki of the PI current loops (Iq and Id).

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Kp_iq | float 32 |  |
| 4-7 |  | Ki_iq | float 32 |  |

The driver does not answer this command.

---

### Send_Velocity_Gains

<div class="cmd-facts" markdown><span class="fact">ID 18</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Velocity_Gains()`</span></div>

Sets Kp and Ki of the PI velocity loop.

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Kpv | float 32 |  |
| 4-7 |  | Kiv | float 32 |  |

The driver does not answer this command.

---

### Send_Position_Gains

<div class="cmd-facts" markdown><span class="fact">ID 19</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Position_Gains()`</span></div>

Sets Kp of the P position loop.

**4 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Kpp | float 32 |  |

The driver does not answer this command.

---

### Send_Limits

<div class="cmd-facts" markdown><span class="fact">ID 20</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Limits()`</span></div>

Sets the speed limit and the current limit the loops may reach. The current limit is clamped by the firmware to the driver's maximum of 2800 mA.

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Speed limit | float 32 | encoder ticks/s |
| 4-7 |  | Current limit | float 32 | mA |

The driver does not answer this command.

---

### Send_Kt

<div class="cmd-facts" markdown><span class="fact">ID 22</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Kt()`</span></div>

Sets the motor's torque constant Kt, which the driver uses to estimate torque from current.

**4 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Kt | float 32 | Nm/A |

The driver does not answer this command.

---

### Send_Voltage_Limit

<div class="cmd-facts" markdown><span class="fact">ID 34</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Voltage_Limit()`</span></div>

Sets the voltage limit of the current loops (the same value as `#Vlim`), in mV. 0 means use the supply voltage. Added in firmware 105.

**4 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-3 |  | Voltage limit | signed 32-bit | mV; 0 = Vbus |

The driver does not answer this command.

---
