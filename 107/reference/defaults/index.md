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
[Saving the configuration](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/saving/).

| Variable | Start value | After `#Default` | Kept by `#Save` | Firmware comment |
|---|---|---|---|---|
| `SERIAL_NUMBER` | 1 | 1111 in the EEPROM, not read back | written, not read back |  |
| `HARDWARE_VERSION` | 1 | 1 | yes | Version of the Spectral BLDC driver PCB |
| `BATCH_DATE` | 1 | 24092024 | yes | Date the batch was produced |
| `SOFTWARE_VERSION` | 1 | 107 | no: set by the firmware | Software release |
| `I_AM_GRIPPER` | 1 | 0 | yes | Is motor controller gripper (1) or not (0) |
| `LED_ON_OFF` | 1 | 1 | yes | Use LED for status indication |
| `theta_offset` | 0.0f | 0 | yes | will be determined at calibration |
| `pole_pairs` | 11 | 7 | yes | Number of pole pairs of your BLDC motor |
| `current_control_bandwidth` | 500 | — | no | default 200 HZ; Will set PI gains for Q and D current loops based on phase resistance |
| `DIR_` | 1 | 0 | yes | When looking at the magnetic encoder counter-clockwise is POSITIVE rotation. |
| `Phase_order` | 2 | 0 | yes |  |
| `commutation_dir` | 1 | 1 | yes | +1 or -1, auto-detected at calibration so +Iq/+velocity/+rotation map to +encoder rotation |
| `Thermistor_on_off` | 0 | 0 | yes | Are we taking termistor mesurements? 0 is off, 1 is on |
| `brake_coast` | 0 | — | no | Idle-mode (Controller_mode == 0) phase behavior: 0 = coast (driver disabled, Hi-Z), 1 = brake (driver stays enabled, zero-voltage PWM vector shorts the phases together) |
| `Resistance` | 0 | 0 | yes | Resistance of SINGLE PHASE of your BLDC motor |
| `Total_Resistance` | 0 | 0 | yes | = 2 * Resistance + 2 * R_sense + 2 *Rdson |
| `Inductance` | 0 | 0 | yes | Inductance of SINGLE PHASE of your BLDC motor |
| `Kt` | 0 | 0 | yes | Torque constant of your BLDC motor |
| `flux_linkage` | 0 | 0 | yes | Flux linkage of your BLDC motor |
| `KV` | 0 | 0 | yes |  |
| `Max_temperature` | 75 | 75 | yes | Max temperature in degrees |
| `Min_temperature` | -20 | — | no | Min temperature in degrees |
| `Max_Vbus` | 29500 | 29000 | yes | Max vbus voltage in mV |
| `Min_Vbus` | 9000 | — | no | Min vbus voltage in mV |
| `watchdog_time_ms` | 0 | 0 | yes |  |
| `watchdog_action` | 0 | 0 | yes | Hold position, Idle, brake |
| `Heartbeat_rate_ms` | 0 | 0 | yes | Motor controller will send data every Heartbeat_rate_ms |
| `Calibrated` | 0 | 0 | yes | 0 if motor is not calibrated, 1 if it is calibrated |
| `Resistance_calc_voltage` | 1000 | — | no | Voltage used to calculate resistance //1000 |
| `Calibration_power` | 12 | — | no | Max power that can dissipate during inductance test. |
| `Open_loop_voltage` | 5000 | — | no | Voltage to use when spinning the motor open loop. In mV |
| `Open_loop_speed` | 20.0 | — | no | Speed to be used when spinning the motor open loop. In RAD/s |
| `Phase_voltage` | 5000 | — | no | Max voltage to be used during Kv calculation |
| `cyclic_period` | 0 | — | no | We send messages every cyclic_period |
| `CAN_ID` | 0 | 0 | yes | CAN id of THIS motor driver! No 2 motor drivers can share the same ID. |
| `calibration_offset_current` | 300 | — | no |  |
| `Voltage_limit` | 0 | 0 | yes | Voltage limit for Ud and Uq voltages. If 0 value of controller.VBUS_mV will be used |
| `Reset_integral_accumulator` | 0 | 0 | yes |  |
| `Kp_p` | 11 | 11 | yes |  |
| `Position_setpoint` | 0 | — | no |  |
| `Kp_v` | 0.03 | 0.03 | yes | 0.006 basic values that work for most motors but not optimal |
| `Ki_v` | 0.0003 | 0.0003 | yes | 0.0001 basic values that work for most motors but not optimal |
| `Feedforward_speed` | 0 | — | no |  |
| `Velocity_setpoint` | 0 | — | no | -1.5 |
| `Velocity_limit` | 800000 | 800000 | yes | Clamp integrals to this  [TICKS/s] |
| `Velocity_limit_error` | 20000000 | — | no | [TICKS/s] ; Velocity when we will report error |
| `Kp_id` | 3 | 3 | yes |  |
| `Ki_id` | 1.5 | 1.5 | yes |  |
| `Id_setpoint` | 0 | — | no |  |
| `Kp_iq` | 3 | 3 | yes |  |
| `Ki_iq` | 1.5 | 1.5 | yes |  |
| `Iq_current_limit` | 1000 | 1000 | yes |  |
| `Id_current_limit` | 0 | 0 | yes |  |
| `Feedforward_current` | 0 | — | no |  |
| `KD` | 0.002800 | 0.0028 | yes | [Nm*s/rad]  KD 0.002800 |
| `KP` | 0.14000 | 0.1400 | yes | [Nm/rad] KP 0.14000 |
| `Uq_setpoint` | 0 | — | no |  |
| `Ud_setpoint` | 0 | — | no |  |
| `position_setpoint` | 0 | — | no |  |
| `speed_setpoint` | 20 | — | no |  |
| `current_setpoint` | 200 | — | no |  |
| `action_status` | 0 | — | no | -0 Stopped(or performing activation /automatic release). |
| `activated` | 0 | — | no |  |
| `release_direction` | 0 | — | no |  |
| `estop_status` | 0 | — | no |  |
