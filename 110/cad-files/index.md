# Downloads and files

Everything to download for the Spectral Micro, at the versions these pages describe. The versions come from one file,
`versions.yml`, so this page changes with them; which versions work together is in
[Versions and compatibility](https://docs.source-robotics.com/Spectral-BLDC-docs/110/appendix/compatibility/).

## Firmware and software

| What | Version | Download | How to install |
|---|---|---|---|
| Firmware image (`spectral-bldc-firmware-V<number>.bin`), its manifest `firmware.json` and the release notes | [110](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/V110) (2026-11-13) | [the GitHub release](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/releases/tag/V110) | [Updating through the bootloader](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/update/) |
| Firmware source, a PlatformIO project | the same release | [the firmware folder at the tag](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/V110/Spectral%20BLDC%20Firmware) | [Building from source](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/building/) |
| The bootloader binary, for a board without one | [0.1](https://github.com/Source-Robotics/stm32f103c-bootloader/tree/V0.1) (2026-06-05) | [bin](https://github.com/Source-Robotics/stm32f103c-bootloader/tree/V0.1/bin) | [Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/bootloader/) |
| The bootloader's host tool `bl_flash.py` | the same release | [host_tools](https://github.com/Source-Robotics/stm32f103c-bootloader/tree/V0.1/host_tools) | [Updating through the bootloader](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/update/) |
| Python library (`Spectral-BLDC`) | [1.22](https://github.com/Source-Robotics/Spectral-BLDC-Python/tree/v1.22) (2026-11-13) | `pip install Spectral-BLDC`; the source and examples on GitHub, [at that version](https://github.com/Source-Robotics/Spectral-BLDC-Python/tree/v1.22) | [With Python](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/python/) |
| Motor GUI | runs in the browser, always the latest | [motorgui.com](https://motorgui.com/) | [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/110/05-setup/motor-gui/) |
| CAN definitions for this release: JSON, and DBC files for the motion layouts | this site's release | [CAN frame tool and downloads](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can-tools/) | |
| ST-LINK USB driver, for the programming adapter on Windows | | [STSW-LINK009](https://www.st.com/en/development-tools/stsw-link009.html) | [Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/bootloader/) |
| STM32CubeProgrammer, for the programming adapter | | [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) | [Installing the bootloader on an older board](https://docs.source-robotics.com/Spectral-BLDC-docs/110/07-firmware/bootloader/) |

The version links open the files at exactly that release; the dates are those of the releases on GitHub, and on
PyPI for the Python library.
Motor GUI has no versions to choose: the page is always the current one. Known faults of the firmware are on
[Known issues](https://docs.source-robotics.com/Spectral-BLDC-docs/110/08-troubleshooting/known-issues/).

## CAD and hardware files

The latest files, on the main branch of the [firmware repository](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller).

| What | Where |
|---|---|
| STEP model of the board and the example mounting bracket | [STEP files](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files) |

## More

| What | Where |
|---|---|
| Source Robotics Toolbox (joints from encoder ticks) | [Source-Robotics-Toolbox](https://github.com/Source-Robotics/Source-Robotics-Toolbox) |
| SimpleFOC examples for the board | [Spectral-Micro-Simple-FOC](https://github.com/Source-Robotics/Spectral-Micro-Simple-FOC) |
| Arduino library for controlling the driver from an Arduino | [SpectralMicroArduino](https://github.com/Source-Robotics/SpectralMicroArduino) |
| CANvas USB-to-CAN adapter | [CANvas-adapter](https://github.com/Source-Robotics/CANvas-adapter) |
| All firmware releases | [Releases](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/releases) |
| This documentation | [Spectral-BLDC-docs](https://github.com/Source-Robotics/Spectral-BLDC-docs) |
| Shop | [source-robotics.com](https://source-robotics.com/products/spectral-micro-bldc-controller) |
