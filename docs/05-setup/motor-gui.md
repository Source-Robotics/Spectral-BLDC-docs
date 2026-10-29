---
status: draft
---

# Motor GUI

[Motor GUI](https://motorgui.com/) is the usual way to set up, test and tune a driver: a tool in the browser that
connects to one driver over the serial adapter or to a bus of drivers over the CANvas adapter, shows the state,
moves the motor, runs the calibration, tunes the loops with live plots, records telemetry and updates the
firmware. Nothing is installed. Everything it does, the driver also does from a terminal or from Python — the
GUI reads and writes the same settings — so every procedure in this manual shows the GUI first and the terminal
command beside it.

!!! note "Screenshots follow"
    Motor GUI is being finished; this page describes what it does and will get its pictures when the tool is done.

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
2. Open [motorgui.com](https://motorgui.com/), choose the connection kind, and **Open port**. The browser asks
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

<!-- screenshots to follow -->

## What next

[Calibration](calibration.md) is the first thing to do with a connected driver;
[Working in Motor GUI](../06-operation/motor-gui.md) covers everyday use: moving the motor, the plots, recordings,
several motors on a bus.
