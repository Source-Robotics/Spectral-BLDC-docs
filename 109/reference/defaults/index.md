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

`#Default` also erases the calibration; from firmware 109 it keeps a valid stored CAN node ID (`existing_id` in
the table; 0 when none is stored); see [Saving the configuration](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/saving/). A name after a value,
such as `160 (CURRENT_BANDWIDTH_DEFAULT)`, is the constant in `constants.h` the value comes from. The settings of
firmware 109 that are parameters, the anti-cogging and the encoder table among them, are in the
[parameter table](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#every-parameter) with their defaults.

<div class="ref-table defaults" markdown>

| Variable and firmware comment | Start value | After `#Default` | Kept by `#Save` |
|---|---|---|---|
| `SERIAL_NUMBER` | 1 | 1111 in the EEPROM, not read back | written, not read back |
| `HARDWARE_VERSION`<br><span class="meta">Version of the Spectral BLDC driver PCB</span> | 1 | 1 | yes |
| `BATCH_DATE`<br><span class="meta">Date the batch was produced</span> | 1 | 24092024 | yes |
| `SOFTWARE_VERSION`<br><span class="meta">Software release</span> | 1 | 109 | no: set by the firmware |
| `I_AM_GRIPPER`<br><span class="meta">Is motor controller gripper (1) or not (0)</span> | 1 | 0 | yes |
| `LED_ON_OFF`<br><span class="meta">Use LED for status indication</span> | 1 | 1 | yes |
| `theta_offset`<br><span class="meta">will be determined at calibration</span> | 0.0f | 0 | yes |
| `pole_pairs`<br><span class="meta">Number of pole pairs of your BLDC motor</span> | 11 | 7 | yes |
| `current_control_bandwidth`<br><span class="meta">Hz: the current PI gains come from R, L</span> | 160 (CURRENT_BANDWIDTH_DEFAULT) | — | no |
| `DIR_`<br><span class="meta">When looking at the magnetic encoder counter-clockwise is POSITIVE rotation.</span> | 1 | 0 | yes |
| `Phase_order` | 2 | 0 | yes |
| `commutation_dir`<br><span class="meta">+1 or -1, auto-detected at calibration so +Iq/+velocity/+rotation map to +encoder rotation</span> | 1 | 1 | yes |
| `Thermistor_on_off`<br><span class="meta">Are we taking termistor mesurements? 0 is off, 1 is on</span> | 0 | 0 | yes |
| `brake_coast`<br><span class="meta">Idle-mode (Controller_mode == 0) phase behavior: 0 = coast (driver disabled, Hi-Z), 1 = brake (driver stays enabled, zero-voltage PWM vector shorts the phases together)</span> | 0 | — | no |
| `Resistance`<br><span class="meta">Resistance of SINGLE PHASE of your BLDC motor</span> | 0 | 0 | yes |
| `Total_Resistance`<br><span class="meta">= 2 * Resistance + 2 * R_sense + 2 *Rdson</span> | 0 | 0 | yes |
| `Inductance`<br><span class="meta">Inductance of SINGLE PHASE of your BLDC motor</span> | 0 | 0 | yes |
| `Kt`<br><span class="meta">Torque constant of your BLDC motor</span> | 0 | 0 | yes |
| `flux_linkage`<br><span class="meta">Flux linkage of your BLDC motor</span> | 0 | 0 | yes |
| `KV` | 0 | 0 | yes |
| `Max_temperature`<br><span class="meta">Max temperature in degrees</span> | 75 | 75 | yes |
| `Min_temperature`<br><span class="meta">Min temperature in degrees</span> | -20 | — | no |
| `Max_Vbus`<br><span class="meta">Max vbus voltage in mV</span> | 29500 | 29000 | yes |
| `Min_Vbus`<br><span class="meta">Min vbus voltage in mV</span> | 9000 | — | no |
| `watchdog_time_ms` | 0 | 0 | yes |
| `watchdog_action`<br><span class="meta">0 legacy, 1 hold, 2 brake, 3 coast, 4 descend (watchdog_action.h)</span> | 0 | 0 | yes |
| `wd_fallback_time_ms`<br><span class="meta">how long hold/descend may run before the after-action</span> | 2000 | 2000 | yes |
| `wd_fallback_current`<br><span class="meta">mA, descend: the current applied (signed)</span> | 0 | 0 | yes |
| `wd_fallback_speed`<br><span class="meta">ticks/s, descend: the speed cap in either direction</span> | 1000 | 1000 | yes |
| `wd_after_action`<br><span class="meta">after hold/descend: 0 legacy, 2 brake, 3 coast</span> | 0 | 0 (WD_ACTION_LEGACY) | yes |
| `calibration_id`<br><span class="meta">parameter 87: new at every successful calibration</span> | 0 | 0 in the EEPROM, not read back | written, not read back |
| `tool_id`<br><span class="meta">what the drive is built into: 0 none, 1 SSG-48, 11-33 MSG, 200-254 custom</span> | 0 | 0 | yes |
| `board_product`<br><span class="meta">product lock stamp in block 2: 1 STEPFOC, 2 Spectral, 0 none</span> | 0 | 0 | yes |
| `sense1_offset`<br><span class="meta">current-sense zero of channel 1, ADC counts from 2048 (start-up)</span> | 0 | — | no |
| `sense2_offset`<br><span class="meta">current-sense zero of channel 2</span> | 0 | — | no |
| `comm_delay_us`<br><span class="meta">parameter 64: commutation delay compensation, us (0 = off)</span> | 234 (COMM_DELAY_DEFAULT_US) | — | no |
| `input_filter_hz`<br><span class="meta">parameter 74: the position input filter, Hz (0 = off)</span> | 0 | — | no |
| `vel_int_deadband`<br><span class="meta">parameter 75: the velocity integral's deadband, ticks (0 = off)</span> | 0 | — | no |
| `sound_limit_mv`<br><span class="meta">parameter 81: the sound's voltage at most (batch 22)</span> | 2000 (SOUND_LIMIT_DEFAULT_MV) | — | no |
| `sound_axis`<br><span class="meta">parameter 82: 1 the q axis (default: much louder on the bench), 0 the d axis</span> | 1 | — | no |
| `fast_trig`<br><span class="meta">parameter 65: 1 the transforms' sin/cos from the integer table (it was</span> | 0 | — | no |
| `speed_estimator`<br><span class="meta">parameter 50</span> | 2 (SPEED_ESTIMATOR_DEFAULT) | — | no |
| `speed_pll_bandwidth`<br><span class="meta">parameter 51, Hz</span> | 100 (SPEED_PLL_BANDWIDTH_DEFAULT) | — | no |
| `Heartbeat_rate_ms`<br><span class="meta">Motor controller will send data every Heartbeat_rate_ms</span> | 0 | 0 | yes |
| `Calibrated`<br><span class="meta">0 if motor is not calibrated, 1 if it is calibrated</span> | 0 | 0 | yes |
| `Resistance_calc_voltage`<br><span class="meta">Voltage used to calculate resistance //1000</span> | 1000 | — | no |
| `Calibration_power`<br><span class="meta">Max power that can dissipate during inductance test.</span> | 12 | — | no |
| `Open_loop_voltage`<br><span class="meta">Voltage to use when spinning the motor open loop. In mV</span> | 5000 | — | no |
| `Open_loop_speed`<br><span class="meta">Speed to be used when spinning the motor open loop. In RAD/s</span> | 20.0 | — | no |
| `Phase_voltage`<br><span class="meta">Max voltage to be used during Kv calculation</span> | 5000 | — | no |
| `cyclic_period`<br><span class="meta">We send messages every cyclic_period</span> | 0 | — | no |
| `CAN_ID`<br><span class="meta">CAN id of THIS motor driver! No 2 motor drivers can share the same ID.</span> | 0 | existing_id | yes |
| `calibration_offset_current` | 300 | — | no |
| `Voltage_limit`<br><span class="meta">Voltage limit for Ud and Uq voltages. If 0 value of controller.VBUS_mV will be used</span> | 0 | 0 | yes |
| `Reset_integral_accumulator` | 0 | 0 | yes |
| `Kp_p` | 11 | 11 | yes |
| `Position_setpoint` | 0 | — | no |
| `Kp_v`<br><span class="meta">0.006 basic values that work for most motors but not optimal</span> | 0.03 | 0.03 | yes |
| `Ki_v`<br><span class="meta">0.0001 basic values that work for most motors but not optimal</span> | 0.0003 | 0.0003 | yes |
| `Velocity_setpoint`<br><span class="meta">-1.5</span> | 0 | — | no |
| `Velocity_limit`<br><span class="meta">Clamp integrals to this  [TICKS/s]</span> | 800000 | 800000 | yes |
| `Velocity_limit_error`<br><span class="meta">[TICKS/s] ; Velocity when we will report error</span> | 20000000 | — | no |
| `Kp_id` | 3 | 3 | yes |
| `Ki_id` | 1.5 | 1.5 | yes |
| `Id_setpoint` | 0 | — | no |
| `Kp_iq` | 3 | 3 | yes |
| `Ki_iq` | 1.5 | 1.5 | yes |
| `Iq_current_limit` | 1000 | 1000 | yes |
| `Id_current_limit` | 0 | 0 | yes |
| `Feedforward_current` | 0 | — | no |
| `KD`<br><span class="meta">[Nm*s/rad]  KD 0.002800</span> | 0.002800 | 0.0028 | yes |
| `KP`<br><span class="meta">[Nm/rad] KP 0.14000</span> | 0.14000 | 0.1400 | yes |
| `Uq_setpoint` | 0 | — | no |
| `Ud_setpoint` | 0 | — | no |
| `position_setpoint` | 0 | — | no |
| `speed_setpoint` | 20 | — | no |
| `current_setpoint` | 200 | — | no |
| `action_status`<br><span class="meta">-0 Stopped(or performing activation /automatic release).</span> | 0 | — | no |
| `activated` | 0 | — | no |
| `release_direction` | 0 | — | no |
| `estop_status` | 0 | — | no |

</div>
