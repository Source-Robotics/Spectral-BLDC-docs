# Ratings and limits

## Electrical

| | Value |
|---|---|
| Supply voltage | 12 to 29 V DC, 24 V typical; 10 V absolute minimum |
| Vbus error limits (firmware) | below 9 V or above 29.5 V |
| Phase current, continuous | 1.5 A typical |
| Phase current, maximum | 2.8 A, the firmware's limit (`#Ilim` is clamped to 2800 mA); needs good cooling and short bursts |
| Power, maximum | 80 W |
| Power, idle | 0.3 W |
| PWM frequency | 25 kHz |
| Control loop frequency | 5 kHz |
| Electrical frequency, maximum | 500 Hz |
| Current sensing | inline, on two phases |
| Encoder | 14-bit magnetic, 16384 ticks per revolution, diametrical magnet 1 mm above the chip |
| UART | 3.3 V, 256000 baud by default (1 000 000 tested) |
| CAN | CAN 2.0, 1 Mbit/s, 11-bit identifiers, node IDs 0 to 15, 120 Ω termination by switch |
| Thermistor input | 100 kΩ NTC, 54.9 kΩ pull-down |
| PIN | analog input or general-purpose input/output, 3.3 V |
| Driver stage protection | hardware overcurrent (trips at 3 to 5 A), undervoltage lockout (6.3 to 8 V) and thermal shutdown (150 to 180 °C); shown as a driver error |

!!! warning "Reversing the polarity on DC+ and DC− destroys the board."

## Thermal and environmental

| | Value |
|---|---|
| Operating temperature of the board | −20 to 130 °C |
| Motor temperature limit (firmware, with the thermistor) | 75 °C by default (`#Tlim`), −20 °C minimum |

## Mechanical

| | Value |
|---|---|
| Dimensions | 39 × 39 mm |
| Mass | 8 g |
| Mounting | four holes on the NEMA 17 pattern, 31 mm apart; the encoder chip in the middle of the board |

## Firmware limits

| | Value |
|---|---|
| Position | signed 24-bit over CAN (±8.4 million ticks, ±512 revolutions), 32-bit internally |
| Speed | signed 24-bit over CAN, encoder ticks per second |
| Current setpoint | signed 16-bit over CAN, mA |
| Motors the calibration defaults are made for | a phase resistance of 2 to 24 Ω |
| Configuration | kept in the EEPROM with `#Save` / `Send_Save_config` |

The defaults of every setting are listed in the [Defaults](../reference/defaults.md) reference.
