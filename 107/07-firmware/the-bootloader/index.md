# The bootloader

Every driver shipped with firmware 105 or newer carries a small bootloader in the first 12 KB of its flash. It
starts the firmware on a normal boot, and it loads a new firmware over UART or CAN when a host asks, so a driver is
updated without a programming adapter and without opening anything. The bootloader is open source:
[stm32f103c-bootloader](https://github.com/Source-Robotics/stm32f103c-bootloader), shared with STEPFOC.

## Memory layout

| Address | Contents |
|---|---|
| `0x08000000` – `0x080022FF` | the bootloader (about 9 KB) |
| `0x08002C00` – `0x08002FFF` | the bootloader's configuration page: the board ID, the firmware's page count and CRC, the bootloader's build version |
| `0x08003000` – `0x0801FFFF` | the firmware (up to 116 KB) |
| RAM `0x20001000` | a magic word the bootloader sets to hand over to the firmware |

The firmware is linked to start at `0x08003000` and sets its vector table there (`VECT_TAB_OFFSET=0x3000`); the
first `0x3000` bytes belong to the bootloader and the firmware never touches them.

## What happens at boot

1. On a reset, the bootloader runs first. If the magic word is in RAM and the reset was a software reset, it
   checks the firmware's stack pointer and reset vector and jumps straight into the firmware: about 10 ms, the
   normal boot.
2. Otherwise it initialises the clocks, CAN, UART and its watchdog, and **listens for a host for 2 s**.
3. With no host, and a firmware whose stored CRC is valid, it sets the magic word and resets; the next boot takes
   the fast path.
4. With a host talking, it stays as long as the host keeps talking: 3 s after the last command, 60 s once a flash
   is in progress. Any `PING` resets the timer.
5. With no valid firmware (never flashed, or a flash that was interrupted), it stays in bootloader mode and waits.
   The LED is off; the driver answers nothing on `#Info`.

## Entering the bootloader

- **From the firmware**: `#Reset` over UART or Send_Reset (command 14) over CAN. Since firmware 105 both reset
  the driver into the bootloader's 2 s window; the host tools send them for you.
- **At power-on**: the 2 s window after every power-up, if the host is already polling.
- **Always**, when there is no valid firmware.

## The board ID

The bootloader has a board ID of its own, 0 to 13, stored in its configuration page. 14 and 15 do not exist
for it: its command frame, identifier `0x700`, decodes as node 14 in the firmware's identifier scheme, so those
two node IDs are reserved. **Give drivers node IDs 0 to 13.** The firmware accepts `#CANID 14` and `15`, but the
bootloader then keeps its old board ID and a firmware update over CAN cannot reach the driver. The firmware keeps it in step with its CAN node ID: setting the node ID (`#CANID`,
Send_CAN_ID) writes the bootloader's board ID too, so a driver answers the host tools under its node ID. A
replacement board ships as ID 0; two boards with the same ID on one bus corrupt each other's flash stream, so
give the new board its ID alone on the bus first (`set-id` in the host tool).

## Transports and protocol

Over **CAN** (1 Mbit/s, standard 11-bit identifiers) the host commands on identifier `0x700` with 8 data bytes
(`board_id`, `cmd`, two parameters); the board replies on `0x701 + board_id` with 5 bytes (`board_id`, `cmd`,
error code, a 16-bit parameter); the firmware image streams in bulk frames on `(board_id << 7) | sequence`,
16 frames of 8 bytes per chunk, with no reply per frame. Over **UART** (256000 baud) the same commands travel in
framed packets `[0xBB][CMD][LEN][BOARD_ID][DATA…][CRC16]` with the same 5-byte reply.

Commands: `WBUF` (1), `WPAGE` (2), `WCRC` (3), `PING` (4), `SET_ID` (5), `ERASE_APP` (6), `STREAM_BEGIN` (7),
`STREAM_STATUS` (8). Error codes: `0` OK, `1` invalid offset, `2` invalid CRC, `3` flash write failed, `4` invalid
page number. A flash is: ping, reset the firmware if it answers, ping until the bootloader answers, `ERASE_APP`
(about 3.5 s), then for each 1 KB page `STREAM_BEGIN`, 8 chunks of 16 frames, `STREAM_STATUS`, `WPAGE` with the
page's CRC32; finally `WCRC` with the page count and the image's CRC32. The bootloader stores the CRC and
reboots into the new firmware. The full wire protocol is in the bootloader repository's `docs/PROTOCOL.md`.

## The host side

| Tool | Transport | Use |
|---|---|---|
| [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/motor-gui/) | serial adapter (Web Serial) or CANvas | one driver on the bench, releases fetched from GitHub |
| `host_tools/bl_flash.py` in the bootloader repository | slcan or gs_usb CAN adapters, or UART | scripts, several boards, `list`, `set-id`, `flash --erase-first` |
| the PAR6 control box's `flash_motor_firmware.py` and the dashboard's Firmware tab | the robot's own CAN bus | every joint of a robot, from the box |

[Updating through the bootloader](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/update/) has the commands.

## Recovery

An interrupted flash leaves an invalid CRC; the bootloader refuses to start the firmware and waits, so the board is
not lost: flash again. A board that answers nothing at all: power-cycle it with the host already polling, to catch
the 2 s window. The one thing the tools refuse, and that would need a programming adapter to undo, is flashing an
image linked for `0x08000000` (a firmware from the `main` branch) over the firmware region.

## Installing it

Boards shipped with firmware 104 or older have no bootloader. [Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/bootloader/)
puts it there once, with a programming adapter at `0x08000000`; from then on the board updates like any other.
