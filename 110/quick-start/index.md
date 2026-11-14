# Quick start

From the box to a calibrated motor that follows commands, in four parts. The quickest way through is
[Motor GUI](https://motorgui.com/) in the browser; every step also shows the terminal commands.

!!! danger "Read first"
    Reversed supply polarity, a daisy-chain cable the wrong way round, or 5 V on the UART port destroys the driver.
    The motor turns during calibration. The [Safety](https://docs.source-robotics.com/Spectral-BLDC-docs/110/02-safety/) chapter is two minutes long.

## Before you start

You start from the box: a driver, a motor and the parts below. The wiring needs a multimeter and a soldering iron.

Nothing else is assumed: no experience with motor drivers, a terminal or a program.

## The four parts

| Part | What you do | What you end with |
|---|---|---|
| [1. Fit the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/110/quick-start/1-motor/) | Fit the magnet, mount the board behind the motor, solder the three phases | A driver on its motor, wired |
| [2. Connect](https://docs.source-robotics.com/Spectral-BLDC-docs/110/quick-start/2-connect/) | Connect the supply and the PC, open Motor GUI or a terminal | A driver that talks to your PC |
| [3. Calibrate](https://docs.source-robotics.com/Spectral-BLDC-docs/110/quick-start/3-calibrate/) | Restore the defaults, calibrate, set the current limit, save | A calibrated driver that keeps its settings |
| [4. First moves](https://docs.source-robotics.com/Spectral-BLDC-docs/110/quick-start/4-first-moves/) | Turn the motor at a speed, move it to a position, stop it | A motor that follows commands |

Each step links the page that explains it. Follow the link when a step is not clear or something fails.

## What you need

| | Where to get it |
|---|---|
| **Spectral Micro driver** | [single driver](https://source-robotics.com/products/spectral-micro-bldc-controller) or the [starter kit](https://source-robotics.com/products/spectral-micro-bldc-starter-kit), which has everything below except the motor, the bracket and the supply |
| **A brushless motor** with a phase resistance of 2 to 24 Ω and 2.8 A or less: a gimbal motor, from the 2804 class to the 8108 class | the [tested motors](https://docs.source-robotics.com/Spectral-BLDC-docs/110/03-technical-data/tested-motors/) are safe choices |
| **The encoder magnet**, diametrically magnetised; the stock one is 6 × 2.5 mm, another thickness is fine if it gives the 1 mm gap | [magnet](https://source-robotics.com/products/6x2-5mm-diametrical-neodymium-magnet) |
| **A bracket** that holds the board behind the motor, and M3 screws | the [example bracket](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files) to adapt and print; a NEMA 17-format motor needs only a spacer |
| **USB-to-serial adapter**, 3.3 V, and its cable | [serial adapter](https://source-robotics.com/products/usb-to-serial-adapter), [UART cable](https://source-robotics.com/products/uart-cable) |
| **Power cable** | [power cable](https://source-robotics.com/products/spectral-micro-power-cable) |
| **A 12 to 29 V supply**, 24 V recommended | a bench supply with a current limit is the safest start |
| For CAN later: **CANvas USB-to-CAN adapter** and a **CAN cable** | [CAN adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter), [CAN cable](https://source-robotics.com/products/spectral-micro-can-cable) |
| Optional: **100 kΩ NTC thermistor** for motor temperature protection | [thermistor](https://source-robotics.com/products/100k-ntc-thermistor) |
| **Software**: Motor GUI in Chrome or Edge, or a serial terminal | [motorgui.com](https://motorgui.com/); PuTTY, the PlatformIO monitor or the Arduino serial monitor |

More: [What you need](https://docs.source-robotics.com/Spectral-BLDC-docs/110/01-overview/what-you-need/).
