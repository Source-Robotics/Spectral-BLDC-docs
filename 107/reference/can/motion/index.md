# Motion

The commands that move the motor and the frames that come back.

### Send_data_pack_1

<div class="cmd-facts" markdown><span class="fact">ID 2</span><span class="fact">host → driver</span><span class="fact">2 or 5 or 8 bytes</span><span class="fact">Python: `Send_data_pack_1()`</span></div>

The motion command. Its length decides the control mode the driver enters: 8 bytes command a position with a speed and a current feedforward, 5 bytes a speed with a current feedforward, 2 bytes a current. Send 0 for a feedforward you do not use. A frame of any other length is ignored (the driver flags it as a wrong data length) but still answered.

**8 bytes** — position setpoint with speed and current feedforward (position mode)

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-2 |  | Position setpoint | signed 24-bit | encoder ticks |
| 3-5 |  | Speed feedforward | signed 24-bit | encoder ticks/s |
| 6-7 |  | Current feedforward | signed 16-bit | mA |

**5 bytes** — speed setpoint with current feedforward (velocity mode)

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-2 |  | Speed setpoint | signed 24-bit | encoder ticks/s |
| 3-4 |  | Current feedforward | signed 16-bit | mA |

**2 bytes** — current setpoint (current mode)

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-1 |  | Current setpoint | signed 16-bit | mA |

The driver answers with **Respond_data_pack_1**.

Every form resets the watchdog. With `Rstint` set, the integral accumulators are cleared on each new setpoint.

---

### Send_data_pack_PD

<div class="cmd-facts" markdown><span class="fact">ID 4</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_data_pack_PD()`</span></div>

Puts the driver in impedance (PD) mode and sets the position, speed and current feedforward of the PD loop, whose gains are KP and KD (Send_PD_Gains).

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-2 |  | Position setpoint | signed 24-bit | encoder ticks |
| 3-5 |  | Speed setpoint | signed 24-bit | encoder ticks/s |
| 6-7 |  | Current feedforward | signed 16-bit | mA |

The driver answers with **Respond_data_pack_1**.

Firmware 106 and older wrote the speed into the feedforward instead of the PD loop's speed setpoint, so the speed term had no effect; 107 fixed it.

---

### Respond_data_pack_1

<div class="cmd-facts" markdown><span class="fact">ID 3</span><span class="fact">driver → host</span><span class="fact">8 bytes</span></div>

The driver's answer to Send_data_pack_1 and Send_data_pack_PD: where the motor is, how fast it turns and the current it draws. The Python library stores them as `position`, `speed` and `current`.

**The frame** (8 bytes)

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0-2 |  | position | signed 24-bit | encoder ticks |
| 3-5 |  | speed | signed 24-bit | encoder ticks/s |
| 6-7 |  | current | signed 16-bit | Iq in mA |

---

### Send_data_pack_2

<div class="cmd-facts" markdown><span class="fact">ID 6</span><span class="fact">host → driver</span><span class="fact">not implemented</span></div>

Reserved. The firmware has no handler for this ID and the Python library's call does nothing.

---

### Send_data_pack_3

<div class="cmd-facts" markdown><span class="fact">ID 8</span><span class="fact">host → driver</span><span class="fact">not implemented</span></div>

Reserved. The firmware has no handler for this ID and the Python library's call does nothing.

---

### Respond_data_pack_2

<div class="cmd-facts" markdown><span class="fact">ID 5</span><span class="fact">driver → host</span><span class="fact">0 bytes</span></div>

Reserved; the driver never sends it.

---

### Respond_data_pack_3

<div class="cmd-facts" markdown><span class="fact">ID 7</span><span class="fact">driver → host</span><span class="fact">0 bytes</span></div>

Reserved; the driver never sends it.

---

### Send_Iq

<div class="cmd-facts" markdown><span class="fact">ID 21</span><span class="fact">host → driver</span><span class="fact">not implemented</span></div>

Reserved; the firmware has no handler for this ID. Use the 2-byte form of Send_data_pack_1 for a current setpoint.

---
