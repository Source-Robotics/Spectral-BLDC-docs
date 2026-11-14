# Gains and limits

The commands that set the loop gains and the limits. None of them is answered; save with Send_Save_config.

### Send_PD_Gains

<div class="cmd-facts" markdown><span class="fact">ID 16</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_PD_Gains()`</span></div>

Sets KP and KD, the gains of the impedance (PD) loop. Keep them with Send_Save_config.

**8 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | KP | float 32 |  |
| 4-7 | KD | float 32 |  |

</div>

The driver does not answer this command.

---

### Send_Current_Gains

<div class="cmd-facts" markdown><span class="fact">ID 17</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Current_Gains()`</span></div>

Sets Kp and Ki of the PI current loop of Iq. The Id loop keeps its gains; over UART, `#Kpiq` and `#Kiiq` set both loops, and so do parameters 11 and 12.

**8 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Kp_iq | float 32 |  |
| 4-7 | Ki_iq | float 32 |  |

</div>

The driver does not answer this command.

---

### Send_Velocity_Gains

<div class="cmd-facts" markdown><span class="fact">ID 18</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Velocity_Gains()`</span></div>

Sets Kp and Ki of the PI velocity loop.

**8 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Kpv | float 32 |  |
| 4-7 | Kiv | float 32 |  |

</div>

The driver does not answer this command.

---

### Send_Position_Gains

<div class="cmd-facts" markdown><span class="fact">ID 19</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Position_Gains()`</span></div>

Sets Kp of the P position loop.

**4 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Kpp | float 32 |  |

</div>

The driver does not answer this command.

---

### Send_Limits

<div class="cmd-facts" markdown><span class="fact">ID 20</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Limits()`</span></div>

Sets the speed limit and the current limit the loops may reach. From firmware 109 a negative value, or one that is not a number, is ignored, and the current limit stops at the driver's 2800 mA, as with `#Ilim`. Firmware 107 and older stored the current limit as it arrived. Never send more than the motor's rating.

**8 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Speed limit | float 32 | encoder ticks/s |
| 4-7 | Current limit | float 32 | mA |

</div>

The driver does not answer this command.

---

### Send_Kt

<div class="cmd-facts" markdown><span class="fact">ID 22</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Kt()`</span></div>

Sets the motor's torque constant Kt, which the driver uses to estimate torque from current.

**4 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Kt | float 32 | Nm/A |

</div>

The driver does not answer this command.

---

### Send_Voltage_Limit

<div class="cmd-facts" markdown><span class="fact">ID 34</span><span class="fact">host → driver</span><span class="fact">4 bytes</span><span class="fact">Python: `Send_Voltage_Limit()`</span></div>

Sets the voltage limit of the current loops (the same value as `#Vlim`), in mV. 0 means use the supply voltage. In the 104 release image (the source at tag V104 does not have it yet) and in every release from 105. From firmware 109 it takes 0 to 60000 mV, as parameter 17 does; a value outside is ignored.

**4 bytes**

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Voltage limit | signed 32-bit | mV; 0 = Vbus |

</div>

The driver does not answer this command.

---
