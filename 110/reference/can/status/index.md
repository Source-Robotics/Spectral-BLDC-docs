# Status requests

Data the host asks for with a remote frame (RTR bit set, no data); the driver answers with a data frame with the same command ID. And the heartbeat, which the driver sends on its own.

### Send_Respond_Ping

<div class="cmd-facts" markdown><span class="fact">ID 10</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Ping()`</span></div>

Asks the driver to answer with an empty frame, to see that it is on the bus.

**The frame** (0 bytes) carries no data.

The driver answers with **Send_Respond_Ping**.

---

### Send_Respond_Temperature

<div class="cmd-facts" markdown><span class="fact">ID 23</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Temperature()`</span></div>

Asks for the thermistor temperature. Meaningful only with the thermistor enabled (`#Term 1`).

**The frame** (2 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-1 | temperature | signed 16-bit | °C |

</div>

The driver answers with **Send_Respond_Temperature**.

---

### Send_Respond_Voltage

<div class="cmd-facts" markdown><span class="fact">ID 24</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Voltage()`</span></div>

Asks for the supply voltage.

**The frame** (2 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-1 | voltage | unsigned 16-bit | mV |

</div>

The driver answers with **Send_Respond_Voltage**.

---

### Send_Respond_Device_Info

<div class="cmd-facts" markdown><span class="fact">ID 25</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Device_Info()`</span></div>

Asks for the driver's identity: hardware version, batch date and serial number from the EEPROM, and the firmware release (from firmware 105 on this is the build's own version; before, a value from the EEPROM).

**The frame** (7 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0 | HARDWARE_VERSION | unsigned 8-bit | PCB revision |
| 1 | BATCH_DATE | unsigned 8-bit | production batch, the lowest 8 bits of the stored value (24092024 after #Default is sent as 120) |
| 2 | SOFTWARE_VERSION | unsigned 8-bit | firmware release, e.g. 107 |
| 3-6 | SERIAL_NUMBER | unsigned 32-bit | serial number |

</div>

The driver answers with **Send_Respond_Device_Info**.

---

### Send_Respond_State_of_Errors

<div class="cmd-facts" markdown><span class="fact">ID 26</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_State_of_Errors()`</span></div>

Asks for every error flag and the calibrated, activated, watchdog and product-lock states.

**The frame** (2 bytes)

<div class="ref-table fields" markdown>

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 | 7 | error | bit | any error is active |
| 0 | 6 | temperature_error | bit | motor over the temperature limit |
| 0 | 5 | encoder_error | bit | magnet not detected or misaligned |
| 0 | 4 | vbus_error | bit | supply voltage outside the limits |
| 0 | 3 | driver_error | bit | the MOSFET driver reports undervoltage, thermal shutdown or overcurrent |
| 0 | 2 | velocity_error | bit | speed over the limit |
| 0 | 1 | current_error | bit | reserved; never set by this firmware |
| 0 | 0 | estop_error | bit | Send_ESTOP was received (from firmware 110 also #Estop over UART) |
| 1 | 7 | calibrated | bit | the motor is calibrated |
| 1 | 6 | activated | bit | the controller is activated |
| 1 | 5 | watchdog_error | bit | the watchdog ran out |
| 1 | 4 | wrong_product | bit | from firmware 109: this firmware is on the other product's board (the product lock) and drives nothing |

</div>

The driver answers with **Send_Respond_State_of_Errors**.

---

### Send_Respond_Iq_data

<div class="cmd-facts" markdown><span class="fact">ID 27</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Iq_data()`</span></div>

Asks for the measured Iq current.

**The frame** (2 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-1 | current | signed 16-bit | mA |

</div>

The driver answers with **Send_Respond_Iq_data**.

---

### Send_Respond_Encoder_data

<div class="cmd-facts" markdown><span class="fact">ID 28</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Encoder_data()`</span></div>

Asks for the position and the filtered speed, as 32-bit values. Python attributes `position` and `speed`.

**The frame** (8 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | position | signed 32-bit | encoder ticks |
| 4-7 | speed | signed 32-bit | encoder ticks/s |

</div>

The driver answers with **Send_Respond_Encoder_data**.

---

### Send_Respond_Kt

<div class="cmd-facts" markdown><span class="fact">ID 33</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Kt()`</span></div>

Asks for the torque constant Kt the driver uses. Added in firmware 104.

**The frame** (4 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-3 | Kt | float 32 | Nm/A |

</div>

The driver answers with **Send_Respond_Kt**.

---

### Send_Respond_Identity

<div class="cmd-facts" markdown><span class="fact">ID 39</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Identity()`</span></div>

Asks what the drive is: the product, the tool it is built into, the firmware release, the hardware version, the pole pairs, whether it is calibrated, and eight flags. A host can check it before it commands or flashes a drive. Added in firmware 109. Python attributes `product_id`, `product_name`, `tool_id`, `firmware_version`, `identity_hardware_version`, `pole_pairs`, `identity_calibrated`, `identity_flags`.

**The frame** (8 bytes)

<div class="ref-table fields" markdown>

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | product | unsigned 8-bit | 1 STEPFOC, 2 Spectral Micro: the firmware that answers |
| 1 |  | tool_id | unsigned 8-bit | parameter 1: 0 none, 1 SSG-48, 11-33 MSG, 200-254 your own |
| 2-3 |  | firmware_version | unsigned 16-bit | the release, e.g. 109 |
| 4 |  | hardware_version | unsigned 8-bit | PCB revision from the EEPROM |
| 5 |  | pole_pairs | unsigned 8-bit | the motor's pole pairs; 0 if outside 0-255 |
| 6 |  | calibrated | unsigned 8-bit | 1 calibrated, 0 not |
| 7 | 0 | gripper | bit | the driver is set up as a gripper (#Gripper 1) |
| 7 | 1 | brake_on_idle | bit | idle brakes (1) or coasts (0) |
| 7 | 2 | commutation_reversed | bit | calibration found the coils wired the other way round |
| 7 | 3 | settings_block2 | bit | the EEPROM has the bank settings block 2 lives in, so parameters 1-5 can be saved |
| 7 | 4 | wrong_product | bit | this firmware is on the other product's board (the product lock) and drives nothing |
| 7 | 5 | sense_zero_measured | bit | the current-sense zero was measured at start-up and is plausible |
| 7 | 6 | cogging_saved | bit | the anti-cogging in use is the one saved in the EEPROM |
| 7 | 7 | switching_zero_in_use | bit | the current-sense zero measured with the bridge switching is in use (parameter 46) |

</div>

The driver answers with **Send_Respond_Identity**.

The flags in byte 7 are numbered the usual way, bit 0 the least significant (unlike the error bytes, which the firmware packs from bit 7 down).

---

### Send_Respond_Telemetry

<div class="cmd-facts" markdown><span class="fact">ID 40</span><span class="fact">host → driver as a remote frame, driver → host as a data frame</span><span class="fact">remote frame, 0 bytes</span><span class="fact">Python: `Send_Respond_Telemetry()`</span></div>

Asks for the temperature, the supply voltage, both error bytes and the current in one frame, all from the same moment: one request instead of four. Added in firmware 109. The Python library fills the same attributes as the four separate answers.

**The frame** (8 bytes)

<div class="ref-table fields" markdown>

| Byte | Field | Type | Meaning |
|---|---|---|---|
| 0-1 | temperature | signed 16-bit | °C (meaningful with the thermistor enabled) |
| 2-3 | voltage | signed 16-bit | supply voltage in mV |
| 4 | errors_1 | unsigned 8-bit | the error flags, as byte 0 of Send_Respond_State_of_Errors |
| 5 | errors_2 | unsigned 8-bit | calibrated, activated, watchdog, wrong product, as byte 1 of Send_Respond_State_of_Errors |
| 6-7 | current | signed 16-bit | Iq in mA |

</div>

The driver answers with **Send_Respond_Telemetry**.

---

### Respond_Heartbeat

<div class="cmd-facts" markdown><span class="fact">ID 9</span><span class="fact">driver → host</span><span class="fact">0 bytes</span></div>

The frame the driver sends on its own at the heartbeat interval (Send_Heartbeat_Setup); empty. Off by default. Any other frame the driver sends resets the heartbeat timer, so a driver that answers motion commands at a high rate never sends a heartbeat.

**The frame** (0 bytes) carries no data.

---
