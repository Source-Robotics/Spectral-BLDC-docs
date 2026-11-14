# Building from source

The firmware is a PlatformIO project for the Arduino core on the STM32F103CB, in the `Spectral BLDC Firmware` folder
of the [firmware repository](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/Bootloader_main/Spectral%20BLDC%20Firmware)
on the `Bootloader_main` branch.

## Building

1. Install [Visual Studio Code](https://code.visualstudio.com/download) and the PlatformIO extension.
2. Clone the repository and check out `Bootloader_main`.
3. Open the `Spectral BLDC Firmware` folder in VS Code; PlatformIO fetches the platform (`ststm32@15.4.1`) and builds
   with the PlatformIO *Build* button or `pio run`. The image is `.pio/build/genericSTM32F103CB/firmware.bin`.

The project is linked for the bootloader: `VECT_TAB_OFFSET=0x3000`, the linker script `ldscript_bootloader.ld`,
the upload offset `0x08003000` and a maximum size of 118784 bytes, in `platformio.ini`. A build that exceeds the
size fails to link.

!!! success "Check"
    PlatformIO ends the build with `SUCCESS`, and `.pio/build/genericSTM32F103CB/firmware.bin` is there. If it
    fails, the first error above the summary names the cause.

## Uploading

PlatformIO runs on Windows, Linux and macOS alike. On Linux, an upload with the programming adapter also needs
PlatformIO's udev rules (`99-platformio-udev.rules`, in the PlatformIO documentation), and a serial port the
`dialout` group.

- **Through the bootloader**: flash the built `firmware.bin` with `bl_flash.py` or Motor GUI as in
  [Updating through the bootloader](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/update/). This is how a release is installed, and works on any driver with
  the bootloader.
- **With the programming adapter**: *Upload* in PlatformIO uses ST-LINK and writes the image at `0x08003000`. The
  bootloader must already be on the board; the upload does not touch it. The serial monitor (the plug icon) opens
  the UART at 256000 with `send_on_enter`, so you can type commands to the driver from the same window.

![Build, upload and the serial monitor in PlatformIO's status bar.](https://docs.source-robotics.com/Spectral-BLDC-docs/110/assets/VSUPLOAD.png){ width="700" }

## Where things are

| | |
|---|---|
| `src/constants.h` | `FIRMWARE_VERSION`, the CAN command IDs, the EEPROM map, the loop and PWM frequencies |
| `src/common.h` | the controller and PID structures with their defaults |
| `src/communication.cpp` | the UART command handlers |
| `src/communication_CAN.cpp` | the CAN receive switch and the transmit functions |
| `src/SerialPacketParser.cpp` | the UART parser: it splits a line into the command and its argument (up to 107 it also kept the list of names it accepted) |
| `src/motor_control.cpp` | the control loops, the calibration routine, the gripper state machine |
| `src/bootloader_config.cpp` | the vector table offset and the reset into the bootloader |
| `release_guide.md` | how a release is cut: version bump, build, tag, GitHub release with `firmware.json` |

## Making a release

`release_guide.md` in the repository is the procedure: bump `FIRMWARE_VERSION`, build, commit the source change, tag
`V<number>`, create the GitHub release with the image, `firmware.json` and the release notes. This site's
`tools/sync_firmware.py` reads a release by its tag; the version box names the release.

## A firmware for a board without a bootloader

The `main` branch builds a firmware linked at `0x08000000` for boards that have no bootloader. Its last tagged
release is 101; it is not maintained. Install the bootloader instead:
[Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/bootloader/).
