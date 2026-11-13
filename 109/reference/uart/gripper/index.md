# Gripper

<div class="cmd-index" markdown>[`#Gripper`](#gripper) [`#Gripcal`](#gripcal) [`#Grippos`](#grippos) [`#Gripvel`](#gripvel) [`#Gripcur`](#gripcur) [`#Gripact`](#gripact) [`#Gripstop`](#gripstop) [`#Gripinfo`](#gripinfo)</div>

### `#Gripper` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 or 1</span></div>

Whether this driver is a gripper. Save it; `#Default` clears it.

**Response:** the flag

---

### `#Gripcal` 

<div class="cmd-facts" markdown><span class="fact">Action</span><span class="fact">Enters **gripper calibration** mode</span></div>

Starts the gripper calibration (the jaws find their end stops).

**Response:** `Gripper calibration!`

---

### `#Grippos` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 (open) to 255 (closed)</span><span class="fact">Enters **gripper** mode</span></div>

The position setpoint; also activates the gripper, sets the action bit and goes to gripper mode.

**Response:** the current position

---

### `#Gripvel` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 to 255</span></div>

The speed setpoint of gripper moves.

**Response:** the setpoint

---

### `#Gripcur` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: current in mA</span></div>

The current limit of gripper moves. From firmware 109 a gripper move uses its magnitude and stops at 2800 mA; see the gripper manual for the safe range.

**Response:** the setpoint

---

### `#Gripact` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 or 1</span></div>

The activate bit.

**Response:** the bit

---

### `#Gripstop` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: 0 or 1</span></div>

The gripper E-stop bit.

**Response:** the bit

---

### `#Gripinfo` 

<div class="cmd-facts" markdown><span class="fact">Get</span></div>

Prints the gripper state: whether the driver is a gripper, calibrated, activated, the position, speed and current setpoints, the E-stop, action and object-detection status, and the end stops.

**Response:** the report

---
