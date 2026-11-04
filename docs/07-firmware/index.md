# Firmware

The driver's firmware is open source and released as numbered builds. Release 104 is the first release built
for the bootloader: a driver that runs 104 or newer carries a bootloader and updates itself over UART or CAN. A
driver that runs 101 or older needs the bootloader installed once with a programming adapter. A driver that
reports 101 can be either ([Drivers that report 101](releases.md#drivers-that-report-101) says how to tell).

## In this chapter

- [Releases and versions](releases.md): how releases are numbered, how to see which one a driver runs, what the
  release notes contain
- [The bootloader](the-bootloader.md): what it is, how the driver boots, how it is entered, its protocol and tools
- [Updating through the bootloader](update.md): the normal update, with Motor GUI, the bootloader's command-line
  tool, or a PAR6 control box
- [Installing the bootloader on an older board](bootloader.md): for a driver that runs firmware 101 or older
- [Building from source](building.md): PlatformIO, the memory layout, uploading with a programming adapter

The release notes of every release up to the one this site describes are in the appendix,
[Firmware release notes](../appendix/firmware-release-notes.md).
