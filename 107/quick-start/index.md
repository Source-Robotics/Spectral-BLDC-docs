# Quick start

From the box to a calibrated motor that follows commands, on one page. The quickest way through is
[Motor GUI](https://motorgui.com/) in the browser; every step also shows the terminal commands, and ends with a
link to the chapter that explains it. Follow the link when a step is not clear or something fails.

!!! danger "Read first"
    Reversed supply polarity, a daisy-chain cable the wrong way round, or 5 V on the UART port destroys the driver.
    The motor turns during calibration. The [Safety](https://docs.source-robotics.com/Spectral-BLDC-docs/107/02-safety/) chapter is two minutes long.

## 1. What you need

| | Where to get it |
|---|---|
| **Spectral Micro driver** | [single driver](https://source-robotics.com/products/spectral-micro-bldc-controller) or the [starter kit](https://source-robotics.com/products/spectral-micro-bldc-starter-kit), which has everything below except the motor, the bracket and the supply |
| **A brushless motor** with a phase resistance of 2 to 24 Ω and 2.8 A or less: a gimbal motor, from the 2804 class to the 8108 class | the [tested motors](https://docs.source-robotics.com/Spectral-BLDC-docs/107/03-technical-data/tested-motors/) are safe choices |
| **The encoder magnet**, diametrically magnetised; the stock one is 6 × 2.5 mm, another thickness is fine if it gives the 1 mm gap | [magnet](https://source-robotics.com/products/6x2-5mm-diametrical-neodymium-magnet) |
| **A bracket** that holds the board behind the motor, and M3 screws | the [example bracket](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files) to adapt and print; a NEMA 17-format motor needs only a spacer |
| **USB-to-serial adapter**, 3.3 V, and its cable | [serial adapter](https://source-robotics.com/products/usb-to-serial-adapter), [UART cable](https://source-robotics.com/products/uart-cable) |
| **Power cable** | [power cable](https://source-robotics.com/products/spectral-micro-power-cable) |
| **A 12 to 29 V supply**, 24 V recommended | a bench supply with a current limit is the safest start |
| For CAN later: **CANvas USB-to-CAN adapter** and a **CAN cable** | [CAN adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter), [CAN cable](https://source-robotics.com/products/spectral-micro-can-cable) |
| Optional: **100 kΩ NTC thermistor** for motor temperature protection | [thermistor](https://source-robotics.com/products/100k-ntc-thermistor) |
| **Software**: Motor GUI in Chrome or Edge, or a serial terminal | [motorgui.com](https://motorgui.com/); PuTTY, the PlatformIO monitor or the Arduino serial monitor |

Read in more detail: [What you need](https://docs.source-robotics.com/Spectral-BLDC-docs/107/01-overview/what-you-need/).

## 2. Fit the magnet

Press the magnet onto the end of the motor shaft, centred, and glue it. It must end up about **1 mm** above the
encoder chip in the middle of the board, and it must not be able to turn on the shaft. A magnet that slips is the
usual cause of a calibration that "succeeds" and a motor that then runs badly.

Read in more detail: [The encoder magnet](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/magnet/).

## 3. Mount the board

Bolt the bracket to the bottom of the motor and the board to the bracket, with the encoder chip (the bottom of the
board) towards the magnet. A NEMA 17-format motor takes the board on a spacer with its own rear screws. Check the
gap: 1 mm, not touching.

Read in more detail: [Mounting on the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/mounting/).

## 4. Wire the motor

Solder the motor's three wires to **U, V and W**. The order does not matter: calibration detects it.

Read in more detail: [Wiring the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/wiring/).

## 5. Connect power and the PC

1. The supply to a power connector: **DC+ to positive, DC− to negative**. Check twice.
2. The serial adapter to the UART connector with the UART cable (TX to RX, RX to TX; 3.3 V only).
3. Power on. The LED turns on steadily: the driver is not calibrated yet, which it reports as an error state.
   (The serial adapter alone powers the driver's logic: it answers over UART without the supply, but reports a
   Vbus error and will not calibrate or move.)

=== "Motor GUI"
    Open [motorgui.com](https://motorgui.com/) in Chrome or Edge, choose the serial connection and **Connect** on
    the adapter's port. The driver's identity and state appear: hardware and firmware version, serial number,
    *Not calibrated*, *No errors*. If nothing connects: the port, the cable's TX/RX, the browser (Web Serial needs
    a Chromium browser).

    Read in more detail: [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/motor-gui/).

=== "Terminal"
    Open a terminal on the adapter's port, 256000 baud, line ending CR+LF, and type `#Info`. The driver prints its
    hardware and firmware version and the state of everything.

    Read in more detail: [The serial terminal](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/terminal/).

Read in more detail: [Power and the CAN daisy chain](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/power-and-can/) ·
[Connectors and pinout](https://docs.source-robotics.com/Spectral-BLDC-docs/107/03-technical-data/connectors/).

**Check:** the driver's identity and live state appear before you change settings. A missing connection
is covered in [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/motor-gui/#opening-the-port) or [Troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/107/08-troubleshooting/).

## 6. Calibrate

First the factory defaults, so that calibration does not start from another motor's values or from junk in the
EEPROM: *Default* in the Motor GUI settings, or `#Default` in the terminal. (It also resets the serial number the
driver reports.) Then fix the motor to the bench, nothing on the shaft, 24 V on the supply. There is nothing to
enter: calibration
measures the motor's resistance and inductance and finds its pole pairs and phase order by itself.

=== "Motor GUI"
    Start the calibration. The GUI switches to *Calibration mode* and shows the driver's log step by step.

=== "Terminal"
    ```
    #Cal
    ```

The LED flashes, the motor clicks, then turns in both directions, and the driver reports each step: the magnet,
the supply, the resistance and inductance, the pole pairs, the phase order, the motor constants, and finally

```
Calibration success!
Save config with #Save
Going to idle!
```

A failed step names itself. `Magnet test: Failed` is the magnet; `Resistance test: Failed` or `Open loop: Failed`
means a phase is not connected or the motor is outside the 2 to 24 Ω range; `Commutation/alignment check failed!`
means the motor did not respond: check the three wires, the supply, and that the magnet does not slip.

Read in more detail: [Calibration](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/calibration/), with the whole log and every message.

**Check:** the calibration log ends with `Calibration success!`. If it does not, use the failed step in
[Calibration troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/calibration/#troubleshooting); do not treat a stopped motor as success.

## 7. Set the current limit and save

The current limit is the current the motor may draw, in mA; it is also the grip of the motor against a load. The
firmware's default of 1000 mA suits the gimbal motors in the tested list; a small 2804 is better at 500 mA, a motor
rated for more can go up to 2800 mA.

=== "Motor GUI"
    Set the current limit in the limits, then **Save** (the GUI warns about unsaved changes until you do).

=== "Terminal"
    ```
    #Ilim 1000
    #Save
    ```

Without saving, the calibration is gone at the next power cycle. The LED now shows three short flashes and a
pause: normal operation.

Read in more detail: [Current limit and loop tuning](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/tuning/) ·
[Saving the configuration](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/saving/).

**Check:** after **Save**, Motor GUI no longer marks unsaved changes. [Saving](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/saving/) explains
which settings are kept.

## 8. Move it

=== "Motor GUI"
    Use the jog controls: *Jog velocity* turns the motor at a speed, *Jog position* moves it to a position, *Jog
    current* applies a torque; *Send setpoint* sends a value in the current control mode. The plots show position,
    speed and current while it moves.

=== "Terminal"
    ```
    #V 16384        one revolution per second
    #V 0
    #P 0            back to where it started
    #P 16384        one revolution forward
    #Idle
    ```

Position is in encoder ticks, 16384 per revolution; speed in ticks per second; current in mA. If the motor hums
or whines, lower the current limit or tune the loops.

Read in more detail: [Control modes](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/modes/) · [Current limit and loop tuning](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/tuning/).

**Check:** the position/speed feedback follows the request, and **Idle** stops driving the motor. A motor
that does not follow needs [Troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/107/08-troubleshooting/) before a load is attached.

## 9. Where to go next

| You want to | Read |
|---|---|
| get to know Motor GUI: the screen, the plots, recordings, several motors | [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/motor-gui/), [Working in Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/motor-gui/) |
| control the driver from a program over CAN | [Over CAN](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/can/), then [With Python](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/python/) |
| put several drivers on one bus | give each a node ID and terminate the ends: [Power and the CAN daisy chain](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/power-and-can/) |
| protect the motor from overheating | [Thermistor](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/thermistor/) |
| update the firmware | [Firmware](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/) |
| look up a message or a command | [API reference](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/) |
| build something: a wheeled robot, a leg, a compliant arm | [Guides](https://docs.source-robotics.com/Spectral-BLDC-docs/107/guides/) |
| understand why it does not work | [Errors and recovery](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/errors/), [Troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/107/08-troubleshooting/) |
