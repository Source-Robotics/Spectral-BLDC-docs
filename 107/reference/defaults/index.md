# Defaults

The values the firmware starts with, from its source (`common.h`) at the release this site describes. `#Default` writes the EEPROM defaults, which are the same unless the firmware comment says otherwise.

| Variable | Default | Firmware comment |
|---|---|---|
| `SERIAL_NUMBER` | 1 |  |
| `HARDWARE_VERSION` | 1 | Version of the Spectral BLDC driver PCB |
| `BATCH_DATE` | 1 | Date the batch was produced |
| `SOFTWARE_VERSION` | 1 | Software release |
| `I_AM_GRIPPER` | 1 | Is motor controller gripper (1) or not (0) |
| `LED_ON_OFF` | 1 | Use LED for status indication |
| `interrupt_tick` | 0 | Ticks of our interrupt routine |
| `TEMP_DEG` | 23 | Temperature in degrees celsius |
| `theta_offset` | 0.0f | will be determined at calibration |
| `pole_pairs` | 11 | Number of pole pairs of your BLDC motor |
| `current_control_bandwidth` | 500 | default 200 HZ; Will set PI gains for Q and D current loops based on phase resistance |
| `sleep_pin_state` | 0 |  |
| `reset_pin_state` | 0 |  |
| `Crossover_frequency` | 0.0 | Crossover frequency, in Radians per sample |
| `DIR_` | 1 | When looking at the magnetic encoder counter-clockwise is POSITIVE rotation. |
| `Phase_order` | 2 |  |
| `commutation_dir` | 1 | +1 or -1, auto-detected at calibration so +Iq/+velocity/+rotation map to +encoder rotation |
| `Thermistor_on_off` | 0 | Are we taking termistor mesurements? 0 is off, 1 is on |
| `Controller_mode` | 0 | 0 -> idle, 1 -> Positon, 2 -> Speed, 3 -> Current, 4 -> PD, 5 -> Open-loop speed, 6 -> Gripper mode, 7-> Calibrate gripper, 8 -> Voltage Torque mode |
| `brake_coast` | 0 | Idle-mode (Controller_mode == 0) phase behavior: 0 = coast (driver disabled, Hi-Z), 1 = brake (driver stays enabled, zero-voltage PWM vector shorts the phases together) |
| `Resistance` | 0 | Resistance of SINGLE PHASE of your BLDC motor |
| `Total_Resistance` | 0 | = 2 * Resistance + 2 * R_sense + 2 *Rdson |
| `Inductance` | 0 | Inductance of SINGLE PHASE of your BLDC motor |
| `Kt` | 0 | Torque constant of your BLDC motor |
| `flux_linkage` | 0 | Flux linkage of your BLDC motor |
| `KV` | 0 |  |
| `Max_temperature` | 75 | Max temperature in degrees |
| `Min_temperature` | -20 | Min temperature in degrees |
| `Max_Vbus` | 29500 | Max vbus voltage in mV |
| `Min_Vbus` | 9000 | Min vbus voltage in mV |
| `execution_time` | 0 | Execution time of our interrupt loops |
| `watchdog_time_ms` | 0 |  |
| `watchdog_reset` | 1 |  |
| `watchdog_action` | 0 | Hold position, Idle, brake |
| `Heartbeat_rate_ms` | 0 | Motor controller will send data every Heartbeat_rate_ms |
| `Send_heartbeat` | 0 |  |
| `Activated` | 0 | If controller is activated or not |
| `Error` | 0 | General error |
| `temperature_error` | 0 | Termistor reported error |
| `encoder_error` | 0 | Encoder magnet is not alligned error |
| `Vbus_error` | 0 | Vbus voltage is too small or too large |
| `Driver_error` | 0 | Driver reported error. 3 possible conditions: Undervoltage, thermal shutdown, overcurrent |
| `Velocity_error` | 0 | We are moving too fast |
| `Current_error` | 0 | We go past max current |
| `ESTOP_error` | 0 | If we received estop command |
| `Watchdog_error` | 0 | If we pass watchdog timeout time |
| `CAN_init_error` | 0 | Set if CAN peripheral failed to initialize; CAN bus is skipped, UART stays usable |
| `commutation` | 0 | 0 is space vector, 1 is sine |
| `Calibration` | 0 | 0 - outside of calibration, 1 inside of calibration, 2 failed calibration, 3 success calibration |
| `Calibrated` | 0 | 0 if motor is not calibrated, 1 if it is calibrated |
| `Resistance_calc_voltage` | 1000 | Voltage used to calculate resistance //1000 |
| `Calibration_power` | 12 | Max power that can dissipate during inductance test. |
| `Calibration_Inductance_voltage` | 0 | Calculated from Calibration power and resistance |
| `Open_loop_voltage` | 5000 | Voltage to use when spinning the motor open loop. In mV |
| `Open_loop_speed` | 20.0 | Speed to be used when spinning the motor open loop. In RAD/s |
| `Number_of_rotations` | 8 | Number of open loop electrical rotations during calibration |
| `Phase_voltage` | 5000 | Max voltage to be used during Kv calculation |
| `Calib_error` | 0 |  |
| `Magnet_cal_status` | 0 |  |
| `Vbus_cal_status` | 0 |  |
| `Resistance_cal_status` | 0 |  |
| `Inductance_cal_status` | 0 |  |
| `Open_loop_cal_status` | 0 |  |
| `Kt_cal_status` | 0 |  |
| `Phase_order_status` | 0 |  |
| `KV_status` | 0 |  |
| `cyclic` | 0 | If 1 we Periodically send messages without request from host. |
| `cyclic_a` | 0 | If 1 we Periodically send messages without request from host. |
| `cyclic_period` | 0 | We send messages every cyclic_period |
| `CAN_ID` | 0 | CAN id of THIS motor driver! No 2 motor drivers can share the same ID. |
| `Wrong_DL` | 0 |  |
| `temp` | 0 |  |
| `temp1` | 0 |  |
| `temp2` | 0 |  |
| `handle_can` | 0 |  |
| `hall_trigger` | 1 | used to record if hall sensor was triggered or not, normal state of hall is high (1) |
| `trigger_value` | 0 |  |
| `calibration_offset_current` | 300 |  |
| `temp_var_offset_calib` | 0 |  |
| `align_state` | 0 |  |
| `align_counter` | 0 |  |
| `aligned_angle` | 0 |  |
| `align_done` | false |  |
| `calib_done` | false |  |
| `calib_reset` | false |  |
| `Velocity_fwd` | 0 |  |
| `Velocity_bwd` | 0 |  |
| `Align_stage` | 0 | Calibrate_Angle_Offset_Align() progress: state index (0 = not running) |
| `Align_point` | 0 | sweep index within the current stage |
| `Spin_confirm_delta` | 0 | diagnostic: encoder ticks moved during the "confirm commutation" spin test, on failure |
| `Spin_confirm_vbus_mV` | 0 | diagnostic: VBUS_mV sampled at that same failure |
| `microstep` | 16 |  |
| `gosteps` | 0 |  |
| `step_interval` | 1000 | step interval in microseconds |
| `open_loop_move_done` | 0 | 1 = finished, cleared by user |
| `Voltage_limit` | 0 | Voltage limit for Ud and Uq voltages. If 0 value of controller.VBUS_mV will be used |
| `Reset_integral_accumulator` | 0 |  |
| `Kp_p` | 11 |  |
| `Position_setpoint` | 0 |  |
| `P_errSum` | 0 |  |
| `Kp_v` | 0.03 | 0.006 basic values that work for most motors but not optimal |
| `Ki_v` | 0.0003 | 0.0001 basic values that work for most motors but not optimal |
| `V_errSum` | 0 |  |
| `Feedforward_speed` | 0 |  |
| `Velocity_setpoint` | 0 | -1.5 |
| `Velocity_limit` | 800000 | Clamp integrals to this  [TICKS/s] |
| `Velocity_limit_error` | 20000000 | [TICKS/s] ; Velocity when we will report error |
| `Ki` | 0 | zero location |
| `Kp_id` | 3 |  |
| `Ki_id` | 1.5 |  |
| `Id_setpoint` | 0 |  |
| `Kp_iq` | 3 |  |
| `Ki_iq` | 1.5 |  |
| `Iq_current_limit` | 1000 |  |
| `Id_current_limit` | 0 |  |
| `Feedforward_current` | 0 |  |
| `KD` | 0.002800 | [Nm*s/rad]  KD 0.002800 |
| `KP` | 0.14000 | [Nm/rad] KP 0.14000 |
| `Uq_setpoint` | 0 |  |
| `Ud_setpoint` | 0 |  |
| `Same_command` | 0 |  |
| `At_position` | 0 |  |
| `position_setpoint` | 0 |  |
| `speed_setpoint` | 20 |  |
| `current_setpoint` | 200 |  |
| `position` | 0 |  |
| `speed` | 0 |  |
| `current` | 0 |  |
| `calibrated` | 0 |  |
| `action_status` | 0 | -0 Stopped(or performing activation /automatic release). |
| `activated` | 0 |  |
| `object_detection_status` | 3 |  |
| `temperature_error` | 0 |  |
| `timeout_error` | 0 |  |
| `estop_error` | 0 |  |
| `release_direction` | 0 |  |
| `estop_status` | 0 |  |
| `max_open_position` | 10329 |  |
| `max_closed_position` | -229 |  |
| `position_ticks` | 0 |  |
| `max_speed` | 80000 |  |
| `min_speed` | 40 |  |
| `In_calibration` | 0 |  |
