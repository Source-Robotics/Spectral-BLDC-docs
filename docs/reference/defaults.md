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

`#Default` also sets the CAN node ID to 0 and erases the calibration; see
[Saving the configuration](../05-setup/saving.md).

<!-- defaults-table -->
