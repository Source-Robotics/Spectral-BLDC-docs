# Releases and versions

A firmware release is a number: 101, 104, 105, … Every release is a tag `V<number>` in the
[firmware repository](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller) and a GitHub release that
carries the image `spectral-bldc-firmware-V<number>.bin`, a manifest `firmware.json` with the image's size, SHA-256 and
the commit it was built from, and the release notes. The notes are the firmware's changelog; the
[appendix](https://docs.source-robotics.com/Spectral-BLDC-docs/107/appendix/firmware-release-notes/) collects them.

## Which release does my driver run?

```
#Info
```

prints `Software version: <number>` among the rest. Over CAN, Send_Respond_Device_Info returns it as the third
byte. From firmware 105 the number is the build's own version; before that it was read from the EEPROM and could
be stale after an update until `#Default`.

## Which release does this site describe?

The one in the version box on the [landing page](https://docs.source-robotics.com/Spectral-BLDC-docs/107/) and in the version selector in the header. When a
newer release changes what a page says, a new version of the site is published and the previous one stays
reachable from the selector. The [compatibility table](https://docs.source-robotics.com/Spectral-BLDC-docs/107/appendix/compatibility/) says which releases go with
which bootloader, Python library and PAR6 runtime.

## The STEPFOC counterpart

Each Spectral Micro release has a [STEPFOC](https://docs.source-robotics.com/STEPFOC-docs/) release with the same
changes; the numbers differ by one (Spectral Micro 107 is STEPFOC 108). The compatibility table lists the pairs.

## The two branches

Releases from 105 on are built from the `Bootloader_main` branch of the repository, whose firmware is linked
to run above the bootloader. The `main` branch holds the firmware of release 104 and earlier, linked to run without a bootloader, and is not
updated. A board running 101 or 104 is documented by version `101` of this site (104 differs from 101 only by the
Send_Voltage_Limit message); to move it to a current release, see [Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/bootloader/).
