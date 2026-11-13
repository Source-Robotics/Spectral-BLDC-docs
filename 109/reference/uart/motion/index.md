# Motion

<div class="cmd-index" markdown>[`#Iq`](#iq) [`#Id`](#id) [`#V`](#v) [`#P`](#p) [`#PD`](#pd) [`#PDV`](#pdv) [`#PDI`](#pdi) [`#Uq`](#uq) [`#Ud`](#ud) [`#Openloop`](#openloop) [`#Idle`](#idle) [`#Brake`](#brake) [`#Close`](#close)</div>

### `#Iq` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: current setpoint in mA</span><span class="fact">Enters **current** mode</span></div>

Current (torque) control with the given Iq setpoint.

**Response:** the measured Iq in mA

---

### `#Id` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: current setpoint in mA</span></div>

Sets the Id setpoint; normally left at 0. Also parameter 58.

**Response:** the measured Id in mA

---

### `#V` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: speed setpoint in encoder ticks/s</span><span class="fact">Enters **velocity** mode</span></div>

Velocity control with the given speed.

**Response:** the measured speed in ticks/s

---

### `#P` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: position setpoint in encoder ticks</span><span class="fact">Enters **position** mode</span></div>

Position control to the given position.

**Response:** the measured position in ticks

---

### `#PD` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: position setpoint in encoder ticks</span><span class="fact">Enters **PD** mode</span></div>

Impedance (PD) control around the given position with the gains KP and KD.

**Response:** the measured position in ticks

---

### `#PDV` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: speed setpoint in encoder ticks/s</span></div>

The speed setpoint of the PD loop.

**Response:** the PD speed setpoint

---

### `#PDI` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: current feedforward in mA</span></div>

The current feedforward of the PD loop.

**Response:** the PD current feedforward

---

### `#Uq` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: voltage in mV</span><span class="fact">Enters **voltage torque** mode</span></div>

Voltage-torque mode with the given q-axis voltage (no current loop).

**Response:** the Uq setpoint in mV

---

### `#Ud` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> int: voltage in mV</span></div>

The d-axis voltage used in voltage-torque mode; does not change the mode.

**Response:** the Ud setpoint in mV

---

### `#Openloop` 

<div class="cmd-facts" markdown><span class="fact">Set/Get</span><span class="fact"><span class="k">Argument</span> float: electrical speed in rad/s</span><span class="fact">Enters **open loop** mode</span></div>

Turns the stator field at the given electrical speed without the encoder in the loop, with the voltage set by Openv. Without a number it still starts the motor, at the stored speed: `#Openloop` alone is not a query. The speed is the same setting as `#Opens`.

**Response:** the open-loop speed

---

### `#Idle` 

<div class="cmd-facts" markdown><span class="fact">Action</span><span class="fact">Enters **idle** mode</span></div>

Goes to idle; the motor coasts or brakes as set by Brake.

**Response:** `Idle`

---

### `#Brake` 

<div class="cmd-facts" markdown><span class="fact">Get</span><span class="fact"><span class="k">Argument</span> 0 or 1</span></div>

What the motor does in idle: 1 brakes (the phases are shorted through the driver), 0 coasts (the phases are open, the default). Takes effect once the driver is idle, so send Idle first. Not saved: the driver coasts again after a power cycle. An error always disables the motor, which then coasts. The braking current is not limited, see Control modes. Added in firmware 107.

**Response:** the setting

---

### `#Close` 

<div class="cmd-facts" markdown><span class="fact">Action</span><span class="fact">Enters **idle** mode</span></div>

Leaves open loop and goes back to closed-loop idle.

**Response:** nothing

---
