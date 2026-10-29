# Saving the configuration

Nothing you set survives a power cycle until you save it.

=== "Motor GUI"
    **Save**. The GUI marks *Unsaved changes* until you do.

=== "Terminal"
    ```
    #Save
    ```

Saving writes the whole configuration to the EEPROM: the motor parameters and the calibration, every gain and
limit, the CAN node ID, the heartbeat and watchdog settings, the thermistor and LED settings and the gripper flag.
Over CAN, Send_Save_config does the same. Save after calibration, after tuning, and after changing the node ID.

## The defaults

=== "Motor GUI"
    *Default* in the settings.

=== "Terminal"
    ```
    #Default
    ```

Restoring the defaults writes the factory values to the EEPROM and reloads them. It also resets the serial
number, the hardware version and the batch date the driver reports, and clears the gripper flag, the heartbeat
rate and the watchdog; note what the driver reports before you use it. The defaults are listed in the
[Defaults](../reference/defaults.md) reference.

Use it before the first calibration of a motor, after a firmware update when the driver behaves oddly, and when
the state shows nonsense values (a `-1`
where a number should be): the EEPROM then holds a layout the firmware does not expect.

## What the driver reports

The state Motor GUI shows, and `#Info` prints, is what is in the EEPROM and what the driver measures: hardware
and firmware version, serial number, calibration state, resistance, inductance, pole pairs, Kt and KV, the gains
and limits, the CAN ID, and the active errors. It is the first thing to look at when something is off, and the
thing to copy into a bug report.
