# Updating through the bootloader

A driver with the bootloader (firmware 105 or newer) is updated over the UART connector or the CAN bus: the host
tells the driver to reset, the bootloader waits two seconds for a host, and the host streams the new image into it.
No programming adapter, and nothing to open.

!!! warning "Before you update"
    - Park the mechanism: the motor loses torque during the update and until the new firmware is calibrated and
      commanded.
    - An update may clear the calibration (the release notes say so when it does); plan to calibrate and `#Save`
      afterwards, and note the gains `#Info` prints.
    - On a bus with several drivers, update each node; a bus with mixed releases behaves unpredictably.

## With Motor GUI

[Motor GUI](https://motorgui.com/) in Chrome or Edge, connected over the serial adapter or the CANvas adapter:
choose the release, and the GUI fetches the image and its manifest from the GitHub release, verifies the size and
the SHA-256, resets the driver into its bootloader and flashes it. This is the way for one driver on the bench.

## With the bootloader's command-line tool

The [bootloader repository](https://github.com/Source-Robotics/stm32f103c-bootloader) has `host_tools/bl_flash.py`,
which flashes an image over CAN (slcan or candleLight/gs_usb adapters) or over UART:

```
cd host_tools
pip install -r requirements.txt

# over CAN with a CANvas (slcan) adapter on COM6, driver with board ID 0
python bl_flash.py --transport can --can-interface slcan --channel COM6 flash spectral-bldc-firmware-V107.bin --board 0 --erase-first

# over UART on COM7
python bl_flash.py --transport uart --port COM7 --baudrate 256000 flash spectral-bldc-firmware-V107.bin --board 0 --erase-first
```

The tool sends the reset command to the running firmware (`#Reset` over UART, Send_Reset over CAN), catches the
bootloader's two-second window, erases the application pages and streams the image page by page, each page
verified by a CRC; `list` shows the boards in bootloader mode, `set-id` changes a board's bootloader ID. The image
is the `spectral-bldc-firmware-V<number>.bin` from the GitHub release.

!!! note "Board ID and node ID"
    The bootloader has its own board ID (0 to 13), kept in its configuration page, separate from the firmware's
    CAN node ID. The firmware keeps the two in step when the node ID is set (`#CANID`, Send_CAN_ID), so a driver's
    bootloader ID is normally its node ID.

## From a PAR6 control box

A robot built on the Robot Control Box updates every joint from the box itself, over its own CAN bus, from the
dashboard's Firmware tab or with `tools/flash_motor_firmware.py`; the
[PAR6 documentation](https://docs.source-robotics.com/par6/) describes it.

## What happens in the driver

1. The host sends the reset; the firmware reboots into the bootloader.
2. The bootloader listens for two seconds. With no host it starts the firmware; with a host it stays as long as
   the host keeps talking (60 s during a flash).
3. The application pages are erased, then written page by page; each page is checked by a CRC.
4. The bootloader checks the whole image's CRC, records it, and starts the new firmware.

## When it fails

A flash that fails or is cancelled part way is not a brick: the stored CRC is invalid, so the bootloader refuses to
start the firmware and waits for a host. Run the flash again; `bl_flash.py list` (or a passive scan from the
control box) finds the board. A board that answers nothing: power-cycle it with the host already polling, to catch
the two-second window.

An image linked for `0x08000000` (a firmware from the `main` branch, release 104 and earlier) must never be
flashed through the bootloader: it would overwrite the bootloader's own region if the tool did not refuse it.
The tools validate the image first.
