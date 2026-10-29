# Firmware

The driver's firmware is open source and released as numbered builds. A driver shipped with firmware 105 or newer carries a bootloader and updates itself over UART or CAN; an older driver needs the bootloader installed once with
a programming adapter.

## In this chapter

- [Releases and versions](releases.md): how releases are numbered, how to see which one a driver runs, what the
  release notes contain
- [The bootloader](the-bootloader.md): what it is, how the driver boots, how it is entered, its protocol and tools
- [Updating through the bootloader](update.md): the normal update, with Motor GUI, the bootloader's command-line
  tool, or a PAR6 control box
- [Installing the bootloader on an older board](bootloader.md): for a driver that runs firmware 104 or older
- [Building from source](building.md): PlatformIO, the memory layout, uploading with a programming adapter

The release notes of every release up to the one this site describes are in the appendix,
[Firmware release notes](../appendix/firmware-release-notes.md).
