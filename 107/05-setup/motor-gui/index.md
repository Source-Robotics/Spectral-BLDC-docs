# Motor GUI

[Motor GUI](https://motorgui.com/) is the usual way to set up, test and tune a driver: a tool in the browser that
connects to one driver over the serial adapter or to a bus of drivers over the CANvas adapter, shows the state,
moves the motor, runs the calibration, tunes the loops with live plots, records telemetry and updates the
firmware. Nothing is installed. Everything it does, the driver also does from a terminal or from Python — the
GUI reads and writes the same settings — so every procedure in this manual shows the GUI first and the terminal
command beside it.

## The browser

Motor GUI reaches the hardware through the browser's serial port access (Web Serial), which Chromium-based
browsers have: Chrome, Edge, Brave, Opera. Firefox and Safari cannot open serial ports.

## Two ways to connect

| | Adapter | Use it for |
|---|---|---|
| **One driver over serial** | the 3.3 V USB-to-serial adapter on the driver's UART connector, 256000 baud | the first setup and calibration (calibration runs over UART only), tuning on the bench |
| **A bus over CAN** | the CANvas adapter; it appears as a serial port and speaks slcan | every driver on the bus by its node ID: testing a machine, updating firmware on all joints |

## Opening the port

1. Plug in the adapter and the motor supply. The adapter alone powers the driver's logic, enough to open the
   port and read the settings, but the driver reports a Vbus error and will not calibrate or move until the
   supply is on.
2. Open [motorgui.com](https://motorgui.com/), choose the connection kind, and **Connect**. The browser asks
   which port; pick the adapter's.
3. The driver's identity appears: hardware version, firmware version, serial number, batch date, whether it is
   calibrated and activated, and the active errors — what `#Info` prints in a terminal.

If the port is not offered, the browser is not Chromium-based, or another program holds the port (a terminal left
open, PlatformIO's monitor). If the port opens and nothing appears: the driver is unpowered, or TX and RX are
crossed on an adapter that is not the Source Robotics one.

## What is on the screen

- **State**: the identity above, the control mode the driver is in, the errors, and **Clear errors**.
- **Jog**: *Jog position*, *Jog velocity* and *Jog current* move the motor in the matching control mode; *Send
  setpoint* sends a value in the current mode. *Live stream while dragging* follows a slider as you move it.
- **Plots** of position, speed and current, panning and zooming, with the value under the pointer.
- **Settings**: the motor parameters (pole pairs, resistance, inductance), the limits (current, velocity,
  voltage), the loop gains with *Apply gains* and *Apply preset*, the CAN node ID, the watchdog, the thermistor.
  The GUI marks *Unsaved changes* until you **Save** to the driver's EEPROM; *Default* restores the factory values.
- **Calibration**: starts `#Cal` and shows the driver's log step by step; afterwards the resistance, inductance and pole pairs it measured, the phase order and direction, Kt, KV
  and the flux linkage.
- **Telemetry**: the stream from the driver, and recordings of it for a test or a bug report.
- **Firmware update**: the releases from GitHub, flashed through the bootloader; *Scan bootloaders* on a bus.
- **Gripper**: the gripper controls, for a driver in gripper mode.
- **Console**: type any `#` command by hand; the answer appears below it.
- **Wiring diagrams** and **Keyboard shortcuts** under help.

## Screen guide

<figure class="gui-shot" markdown="1">
<div class="gui-shot__image" markdown="1">

![Motor GUI connection bar with UART transport, baud rate and Connect](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/motor-gui/connection.jpg){ width="1000" }

<span class="gui-shot__mark" style="left:3%;top:20%" aria-hidden="true">1</span>
<span class="gui-shot__mark" style="left:15%;top:20%" aria-hidden="true">2</span>
<span class="gui-shot__mark" style="left:23%;top:20%" aria-hidden="true">3</span>

</div>
<figcaption markdown="1">**1. Transport:** choose UART for the serial adapter. **2. Baud:** 256000 for a stock driver. **3. Connect:** choose the adapter in the browser's port picker.</figcaption>
</figure>

<figure class="gui-shot" markdown="1">
<div class="gui-shot__image" markdown="1">

![Motor GUI simulated motor: device state, controls and live telemetry](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/motor-gui/motor-demo.jpg){ width="1000" }

<span class="gui-shot__mark" style="left:1%;top:9%" aria-hidden="true">1</span>
<span class="gui-shot__mark" style="left:1%;top:18%" aria-hidden="true">2</span>
<span class="gui-shot__mark" style="left:1%;top:40%" aria-hidden="true">3</span>
<span class="gui-shot__mark" style="left:88%;top:17%" aria-hidden="true">4</span>

</div>
<figcaption markdown="1">**1. Connection and node:** confirm the intended driver. **2. State:** calibration, activation and faults. **3. Command mode:** setpoints and jog controls. **4. Live telemetry:** measured position, speed and current. This screenshot uses **Mock CAN (demo)**, not physical hardware.</figcaption>
</figure>

**Check:** after connecting real hardware, the state and identity belong to your driver. If they do not appear, check the transport, selected port, supply and TX/RX wiring before trying to move.

## Try it without hardware

Open [Motor GUI](https://motorgui.com/), choose **Mock CAN (demo)**, and press **Connect**. The motor and gripper panels run in the browser without a port picker. Motor calibration (`#Cal`) still requires a real UART connection; the CAN demo does not perform it.

## What next

[Calibration](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/calibration/) is the first thing to do with a connected driver;
[Working in Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/motor-gui/) covers everyday use: moving the motor, the plots, recordings,
several motors on a bus.
