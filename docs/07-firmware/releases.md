# Releases and versions

A firmware release is a number: 101, 104, 105, … Every release is a tag `V<number>` in the
[firmware repository](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller) and a GitHub release that
carries the image `spectral-bldc-firmware-V<number>.bin`, a manifest `firmware.json` with the image's size, SHA-256 and
the commit it was built from, and the release notes. The notes are the firmware's changelog; the
[appendix](../appendix/firmware-release-notes.md) collects them.

## Which release does my driver run?

```
#Info
```

prints `Software version: <number>` among the rest. Over CAN, Send_Respond_Device_Info returns it as the third
byte. From firmware 105 the number is the build's own version; before that it was read from the EEPROM and could
be stale after an update until `#Default`.

## Which release does this site describe?

The one in the version box on the [landing page](../index.md) and in the version selector in the header. When a
newer release changes what a page says, a new version of the site is published and the previous one stays
reachable from the selector. The [compatibility table](../appendix/compatibility.md) says which releases go with
which bootloader, Python library and PAR6 runtime.

## The STEPFOC counterpart

Most Spectral Micro releases have a [STEPFOC](https://docs.source-robotics.com/STEPFOC-docs/) release with the
same changes. The numbers do not always match: the current pair is Spectral Micro 107 and STEPFOC 108, and the
[compatibility table](../appendix/compatibility.md) lists the others.

## The two branches

Releases from 104 on are built from the `Bootloader_main` branch of the repository, whose firmware is linked to
run above the bootloader; 104 is the first of them. The `main` branch holds the firmware linked to run without a
bootloader: release 101 and earlier, and a few later changes that were never tagged as a release (among them
the Kt request and the voltage limit message). It is not updated.

Version `101` of this site documents a board running 101. It also fits 104, which adds the Send_Respond_Kt
request, Send_Voltage_Limit (in the release image) and the bootloader. To move a board without a bootloader to a
current release, see [Installing the bootloader on an older board](bootloader.md).
