# 3. Calibrate

The driver learns your motor. There is nothing to enter: calibration measures the motor's resistance and
inductance and finds its pole pairs and phase order by itself.

## 1. Restore the defaults

First the factory defaults, so that calibration does not start from another motor's values or from junk in the
EEPROM.

=== "Motor GUI"

    Press *Default* in the settings.

=== "Terminal"

    ```
    #Default
    ```

??? info "What else #Default resets"
    It also sets the hardware version and batch date to factory values; from firmware 109 it keeps the CAN node ID.

## 2. Calibrate

!!! tip "We recommend a Motor GUI preset"
    In Motor GUI's **Presets** tab, apply *Generic motor*, *BLDC motor on Spectral Micro (soft)* before you
    calibrate. It writes a low current limit and soft loops and leaves the resistance, the inductance and the pole
    pairs to the calibration, which measures them, so the motor calibrates safely. Raise the limits and the gains
    from there ([Current limit and loop tuning](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/tuning/)). More: [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/motor-gui/).

1. Fix the motor to the bench, with nothing on the shaft.
2. Set the supply to 24 V.
3. Start the calibration:

    === "Motor GUI"

        Start the calibration. The GUI switches to *Calibration mode* and shows the driver's log step by step.

    === "Terminal"

        ```
        #Cal
        ```

4. Keep the shaft free until the end, about a minute more after the log below.

The LED flashes, the motor clicks, then turns in both directions, and the driver reports each step: the magnet,
the supply, the resistance and inductance, the pole pairs, the phase order, the motor constants, and finally

```
Calibration success!
Next, by itself: the encoder table, then anti-cogging (about a minute; keep the shaft free). Everything is saved when they finish (#Encal state, #Cogcal state)
Going to idle!
```

The driver then goes on to measure the encoder table and the anti-cogging, and saves everything when they succeed.

A failed step names itself:

- `Magnet test: Failed` is the magnet;
- `Resistance test: Failed` means a phase is not connected or the motor is outside the 2 to 24 Ω range;
- `Open loop: Failed` means the rotor did not follow the field: check the three wires and that the shaft is free;
- `Commutation/alignment check failed!` means the motor did not respond: check the three wires, the supply, and
  that the magnet does not slip.

!!! success "Check"
    The calibration log ends with `Calibration success!`. If it does not, use the failed step in
    [Calibration troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/calibration/#troubleshooting); do not treat a stopped motor as
    success.

More: [Calibration](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/calibration/), with the whole log and every message.

## 3. Set the current limit and save

The current limit is the current the motor may draw, in mA; it is also the grip of the motor against a load.

From firmware 109 calibration puts back the limit that was in force (107 and older left 1600 mA), so check it now,
before you save. 1000 mA suits the gimbal motors in the tested list; a small 2804 is better at 500 mA, a motor
rated for more can go up to 2800 mA.

=== "Motor GUI"

    Set the current limit in the limits, then **Save** (the GUI warns about unsaved changes until you do).

=== "Terminal"

    ```
    #Ilim 1000
    #Save
    ```

Without saving, the calibration is gone at the next power cycle. The LED now shows three short flashes and a
pause: normal operation.

![Three short flashes and a pause](https://docs.source-robotics.com/Spectral-BLDC-docs/109/assets/Normal.webp){ width="180" }

!!! success "Check"
    After **Save**, Motor GUI no longer marks unsaved changes, and after a power cycle `#Info` prints
    `Calibrated`. [Saving](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/saving/) explains which settings are kept.

More: [Current limit and loop tuning](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/tuning/) · [Saving the configuration](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/saving/).
