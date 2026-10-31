# Errors and recovery

When the driver detects a fault it stops the motor, goes to idle, turns the status LED on steadily and sets the
error bit in every CAN frame it sends. It stays there until the error is cleared.

## Seeing the error

- **The LED**: on and not flashing means error mode (or not calibrated). Three short flashes and a pause is
  normal operation; flashing every 0.5 s is calibration.
- **`#Error`** prints `In error state!` or `No errors!`, followed by one line per active error.
- **Send_Respond_State_of_Errors** returns every flag as a bit; **the error bit** of any frame says whether there
  is one.

| Normal operation | Calibration | Error mode |
|---|---|---|
| ![Three short flashes and a pause](../assets/Normal.webp){ width="180" } | ![Flashing every 0.5 s](../assets/Calib.webp){ width="180" } | ![On, steady](../assets/Error2.webp){ width="180" } |

In error mode the LED does not flash: it stays on, as in the photo on the right.

## The errors

| Error | `#Error` line | Cause | What to do |
|---|---|---|---|
| Vbus | `Vbus error` | the supply voltage is below 9 V or above 29.5 V (`#Vmax`) | check the supply and the cable; a decelerating motor can push the voltage up |
| Encoder | `Encoder error` | the magnet is not detected or the reading is invalid | magnet distance and type, see [The encoder magnet](../04-mounting/magnet.md) |
| Driver | `Driver error (undervoltage, thermal shutdown, or overcurrent)` | the MOSFET driver's own protection tripped | lower the current limit, cool the driver, check for a short between the motor leads |
| Velocity | `Velocity error` | the speed exceeded the limit | lower the commanded speed or raise `#Vlimit` |
| Temperature | `Temp error` | the thermistor reads more than `#Tlim` (75 °C by default), with `#Term 1` | let the motor cool; lower the current limit |
| E-stop | `Received ESTOP command` | Send_ESTOP was received | clear it when it is safe |
| Watchdog | `Watchdog error` | no valid CAN frame within the watchdog time (Send_Watchdog) | the host stopped sending; fix the host, then clear |
| Not calibrated | `Not calibrated` | the motor has not been calibrated since `#Default`, or the EEPROM is invalid | run `#Cal` and `#Save` |
| Current | `Current error` | reserved; this firmware never raises it | — |

## Clearing

`#Clear` or Send_Clear_Error clears the flags and goes to idle. An error whose cause is still present comes
straight back: a Vbus error at 2 V stays until the supply is right; once the supply is 24 V, one `#Clear` returns
the driver to normal operation. The calibration error clears only by calibrating (or, for a motor you know is
calibrated, `#Calibrated 1`).

## When the driver does not answer

- No LED at all: no power. Check DC+ and DC− and the cable orientation.
- LED on, no answer on UART: the baud rate (256000), TX and RX crossed, the adapter's port.
- No answer on CAN: the node ID, the termination (about 60 Ω across the bus, unpowered), 1 Mbit/s on the adapter.
- `#Info` shows `-1` or nonsense: the EEPROM holds a layout the firmware does not expect; `#Default`, then
  calibrate again.

[Troubleshooting](../08-troubleshooting.md) goes through the symptoms one by one.
