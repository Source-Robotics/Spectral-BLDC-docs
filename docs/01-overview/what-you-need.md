# What you need

This page lists what a Spectral Micro setup is made of, what comes with the driver, and what you buy or make
yourself.

## The driver

The Spectral Micro is sold as a single driver or as a starter kit in the Source Robotics shop:

- [Spectral Micro BLDC controller](https://source-robotics.com/products/spectral-micro-bldc-controller)
- [Spectral Micro starter kit](https://source-robotics.com/products/spectral-micro-bldc-starter-kit), which adds
  the adapters, the magnet, the cables and a thermistor listed below

Every driver is end-of-line tested and ships with the current firmware release and the bootloader already
installed, so a driver works out of the box with a serial terminal, the Python library or Motor GUI. The firmware
can be updated later without a programming adapter; see [Firmware](../07-firmware/index.md).

## A brushless motor

The Spectral Micro drives three-phase brushless motors with a phase resistance of about 2 to 24 Ω and a current
of 2.8 A or less: gimbal motors from the small 2804 class up to the 8108 class, and other brushless motors of
similar resistance, such as the NEMA 17-format 42BLS40. The [tested motors](../03-technical-data/tested-motors.md)
are known to work. The motor needs a place for the encoder magnet on the axis of its shaft, on the side where the
board is mounted.

!!! danger "Low-resistance motors"
    The calibration routine's default voltages are made for motors of 2 Ω and more. A motor with a much lower
    resistance, such as a drone motor, draws a destructive current at those voltages. Do not calibrate one without
    lowering the calibration voltages (`#Resv`, `#Openv`, `#Vp`) and the current limit first.

## The encoder magnet

A diametrically magnetised 6 × 2.5 mm neodymium magnet on the end of the motor shaft, about 1 mm above the
encoder chip in the middle of the board: [6 × 2.5 mm diametrical magnet](https://source-robotics.com/products/6x2-5mm-diametrical-neodymium-magnet).
An axially magnetised magnet, or one that wobbles, makes calibration fail or report bad positions. The 6 × 2.5 mm
size is the stock one, not a requirement: another thickness is a way to set the 1 mm gap when a shaft or a bracket
leaves the wrong distance. [The encoder magnet](../04-mounting/magnet.md) says how to fit it.

## A mounting bracket

The board does not bolt to a gimbal motor directly: a bracket holds it behind the motor, with the encoder chip on
the shaft's axis and 1 mm from the magnet. The firmware repository has an
[example bracket](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files) to
adapt to your motor; see [Mounting on the motor](../04-mounting/mounting.md). A motor with the NEMA 17 hole
pattern, such as the 42BLS40, takes the board on a spacer with its own screws.

## Adapters and cables

| Part | Needed for | Shop |
|---|---|---|
| USB-to-serial adapter (3.3 V) | the serial terminal: calibration, tuning, any `#` command | [Serial adapter](https://source-robotics.com/products/usb-to-serial-adapter) |
| CANvas USB-to-CAN adapter | CAN control from a PC, the Python library, Motor GUI over CAN | [CAN adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter) |
| CAN cable and power cable | daisy-chaining several drivers | [CAN cable](https://source-robotics.com/products/spectral-micro-can-cable), [power cable](https://source-robotics.com/products/spectral-micro-power-cable) |
| 100 kΩ NTC thermistor | motor temperature protection (optional but recommended) | [Thermistor](https://source-robotics.com/products/100k-ntc-thermistor) |
| JTAG programming adapter | only for installing the bootloader on an older board, or for firmware development | [Programming adapter](https://source-robotics.com/products/jtag-programming-adapter-1-27-pitch) |

!!! danger "Cable orientation"
    The daisy-chain cables for CAN and power are keyed by their orientation, not by their connector. A cable
    plugged in the wrong way round destroys the driver. Use the cables from the shop or follow
    [Power and the CAN daisy chain](../04-mounting/power-and-can.md) exactly when you make your own.

## A power supply

12 to 29 V DC, 24 V recommended; see [Ratings and limits](../03-technical-data/ratings.md). Calibrate at 24 V:
the resistance, inductance and motor constants come out wrong at a lower voltage. A bench supply with a current
limit is the safest way to start.

## Software

- [Motor GUI](https://motorgui.com/), in the browser, over the serial adapter or the CAN adapter: the usual tool
  for setup, calibration, tuning, plots and firmware updates; see [Motor GUI](../05-setup/motor-gui.md).
- Or a serial terminal: PuTTY, the PlatformIO monitor in VS Code, or the Arduino serial monitor; see
  [The serial terminal](../05-setup/terminal.md).
- The Python library `Spectral-BLDC` for CAN control from your own programs; see [With Python](../06-operation/python.md).
