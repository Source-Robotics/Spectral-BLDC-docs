# Saving the configuration

Nothing you set survives a power cycle until you save it.

=== "Motor GUI"
    **Save**. The GUI marks *Unsaved changes* until you do.

=== "Terminal"
    ```
    #Save
    ```

Saving writes the configuration to the EEPROM: the motor parameters and the calibration, every gain and limit,
the CAN node ID, the heartbeat and watchdog settings, the thermistor and LED settings, the temperature and voltage
limits and the gripper flag. Over CAN, Send_Save_config does the same. Saving also copies the node ID into the
bootloader's board ID ([The bootloader](../07-firmware/the-bootloader.md#the-board-id)). Save after calibration,
after tuning, and after changing the node ID.

!!! warning "Set the current limit before you save a calibration"
    Calibration leaves the current limit at 1600 mA. Set the limit for your motor (`#Ilim`) before you save, or the
    1600 mA are saved with the calibration.

## What is not saved

These settings are lost at a power cycle, whatever you save. The driver starts with the values in the
[Defaults](../reference/defaults.md) reference:

- the idle behaviour (`#Brake`, Send_Settings): the driver coasts after every power-up;
- the calibration settings `#Cbw`, `#Resv`, `#Calpwr`, `#Openv`, `#Opens`, `#Vp` and `#Iqoffset`: set them again
  before each calibration that needs other values;
- the cyclic output (`#Cyc`, `#Cyca`);
- the serial number. Saving writes it, but the firmware does not read it back at power-up: after a power cycle
  the driver reports 1, and the next save writes that 1 over the stored number.

## The defaults

=== "Motor GUI"
    *Default* in the settings.

=== "Terminal"
    ```
    #Default
    ```

Restoring the defaults writes the factory values to the EEPROM and loads them. It erases the calibration (the
driver reports *Not calibrated*), sets the CAN node ID back to 0, clears the gripper flag, the heartbeat rate and
the watchdog, sets the hardware version to 1 and the batch date to 24092024, and stores 1111 as the serial number.
Note what the driver reports before you use it, and give a driver on a bus its node ID again afterwards. The
values are listed in the [Defaults](../reference/defaults.md) reference.

Use it before the first calibration of a motor, after a firmware update when the driver behaves oddly, and when
the state shows nonsense values (a `-1` where a number should be).

## The check at power-up

Since firmware 106 the saved configuration is two blocks, each with its own checksum: the calibration (the
motor's resistance, inductance, pole pairs, phase order, direction, angle offset, Kt, KV and the current loop
gains) and the settings (the other gains, the limits, the node ID, the watchdog, the heartbeat and the flags). At
power-up the driver checks both. A block that fails, after a power loss during a save for instance, is replaced
by its factory values without a message: a failed settings block puts the driver on node ID 0 with the default
gains and limits, a failed calibration block leaves it *Not calibrated*. The other block is kept.

A board that comes from a release before 106 has no checksums yet: the driver keeps its values once and seals
them. A value that was already wrong (a `-1` in `#Info`, for instance) then stays, and `#Default` with a new
calibration is the fix.

## What the driver reports

`#Info` prints the identity and the motor: hardware version, batch date, firmware version, CAN ID, whether the
motor is calibrated, temperature, supply voltage, the phase order and direction, the pole pairs, resistance,
inductance, Kt and KV. `#SERNUM` prints the serial number, `#Param` the gains and limits, `#Error` the active
errors. They are the first thing to look at when something is off, and the thing to copy into a bug report.
