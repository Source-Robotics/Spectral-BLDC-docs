# Defaults

The settings of the firmware, read from its source at the release this site describes. The table leaves out
the firmware's internal state (counters, flags, scratch variables).

- **Start value** is the value in the firmware's structures (`common.h`). At power-up the firmware loads the saved
  settings from the EEPROM over it, so for a setting that `#Save` keeps the start value only shows until the EEPROM
  is read.
- **After `#Default`** is what the driver runs with after `#Default`, which writes the factory values to the EEPROM
  and loads them. A fresh board, and a board whose saved configuration fails its check at power-up, gets the same
  values.
- **Kept by `#Save`** says whether the setting survives a power cycle. *No* means the driver starts with the start
  value again after every power-up.

`#Default` also erases the calibration; from firmware 108 it keeps a valid stored CAN node ID (`existing_id` in
the table; 0 when none is stored); see [Saving the configuration](../05-setup/saving.md). A name after a value,
such as `160 (CURRENT_BANDWIDTH_DEFAULT)`, is the constant in `constants.h` the value comes from. The settings of
firmware 108 that are parameters, the anti-cogging and the encoder table among them, are in the
[parameter table](can/parameters.md#every-parameter) with their defaults.

<!-- defaults-table -->
