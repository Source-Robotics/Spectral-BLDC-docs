# Calibration

Calibration teaches the driver its motor: it checks the magnet and the supply, measures the motor's phase
resistance and inductance and computes the current loop gains from them, spins the motor in open loop to find
the pole pairs and the direction, checks the order of the phases and aligns the encoder to the rotor field, and
measures the motor constants Kt, KV and the flux linkage. Nothing about the motor has to be entered first. It
runs once per motor; the result is kept by saving.

!!! danger "The motor turns"
    Calibration spins the motor in both directions, fast at times. Fix the motor to the bench and take everything
    off the shaft.

!!! tip "Supply voltage"
    Calibrate at 24 V. At a lower voltage the resistance, the inductance, KV and Kt come out wrong.

## The settings

The routine uses six settings, which it prints when it starts. The defaults suit motors with a phase resistance
of 2 to 24 Ω; change them only for a motor outside that range.

| Setting | Default | Command | What it does |
|---|---|---|---|
| Current loop bandwidth | 500 Hz | `#Cbw` | the bandwidth the current loop gains are computed for; too high makes the motor vibrate and whine |
| Resistance voltage | 1000 mV | `#Resv` | the voltage the resistance measurement starts at; it rises until the power reaches the limit below |
| Max power dissipation | 12 W | `#Calpwr` | the power the resistance and inductance measurements may put into the motor |
| Open loop voltage | 5000 mV | `#Openv` | the voltage of the open-loop spin that finds the pole pairs |
| Open loop speed | 20 rad/s | `#Opens` | the electrical speed of that spin |
| Phase search voltage | 5000 mV | `#Vp` | the voltage of the spin that checks the phase order |

!!! danger "Low-resistance motors"
    These voltages are made for motors of 2 Ω and more. On a motor with a much lower resistance, such as a drone
    motor, they drive a destructive current. The Spectral Micro is not made for such motors; if you must try one,
    lower the three voltages and the current limit first.

## 1. Restore the defaults

The EEPROM of a new driver, or of one that ran another motor, can hold values that do not fit: another motor's
parameters, or junk that shows as `-1` in `#Info`. Calibration starts from what is there, so start from the factory
values.

=== "Motor GUI"
    *Default* in the settings.

=== "Terminal"
    ```
    #Default
    ```

This also resets the serial number, hardware version and batch date the driver reports; note what `#Info` printed
if you need them. [Saving the configuration](saving.md) says what else it does.

## 2. Run it

=== "Motor GUI"
    Start the calibration. The driver enters *Calibration mode* and the GUI shows its log step by step; when it
    finishes, the resistance, inductance and pole pairs it measured, the phase order and direction, Kt, KV and the
    flux linkage appear in the settings.

=== "Terminal"
    ```
    #Cal
    ```

The LED flashes every 0.5 s while the routine runs, and the driver prints each step as it goes. The numbers below
are those of one tested motor; yours will differ:

```
----------------
Calibration mode
-----Settings-----
Current loop bandwidth: 500.00Hz
Resistance voltage: 1000mV
Max Power dissipation: 12.00W
Open loop voltage: 5000mV
Open loop Speed: 20.00Rad/s
Phase search voltage: 5000mV
----------------
Magnet test: Passed
Vbus test: Passed
Resistance = 7.026575Ohm
Inductance = 0.001492H
Kp_iq = ...
Ki_iq = ...
Pole pair = 11
Dir = 1
Phase order = 2
Phase order is good!
KV is: ...
Kt is: ...
Flux linkage is: ...
----------------
Calibration success!
Save config with #Save
Going to idle!
----------------
```

What the steps are:

| Step | What happens | Fails with |
|---|---|---|
| Magnet test | the encoder sees enough field: a magnet is there and close enough. The test says nothing about centring, the gap or the glue | `Magnet test: Failed`: magnet missing, too far, or axially magnetised |
| Vbus test | the supply is within limits | `Vbus test: Failed` |
| Resistance | a rising voltage is put on the windings and the current measured; the motor clicks. The resistance follows from the two | `Resistance test: Failed`: no current flows, a phase is not connected, or the motor is far outside the 2 to 24 Ω range |
| Inductance | a voltage step and the rate at which the current rises give the inductance. Kp_iq and Ki_iq are computed from R, L and the bandwidth | `Inductance test: Failed` |
| Open loop | the stator field is turned at the open-loop speed and the encoder watched: the pole pairs are the ratio of electrical to mechanical turns, and the direction the rotor turned is remembered as `Dir` | `Open loop: Failed`: the encoder saw no rotation |
| Phase order | a current command must move the rotor the expected way, and the encoder's zero is aligned to the rotor field (the angle offset, `#Offset`). A motor that does not respond gets a second try at another angle | `Commutation/alignment check failed!`, `Motor did not respond as expected to a current command...` and a line `Spin-confirm delta: … ticks (need > …), Vbus: … mV` that says how far the motor turned and at what voltage |
| Kt, KV, flux linkage | the motor spins fast for a moment and the constants are computed from the back-EMF | — |

!!! note "The measured values are estimates"
    The resistance, the inductance and the motor constants differ a little from one run to the next, and KV, and
    with it Kt and the flux linkage, can be off by a factor of two or three on cheap motors with uneven windings.
    For the loops this does not matter; for a torque estimate in newton-metres, measure Kt yourself.

## 3. Save

=== "Motor GUI"
    **Save**. The GUI marks *Unsaved changes* until you do.

=== "Terminal"
    ```
    #Save
    ```

Without it the calibration is gone at the next power cycle. The driver goes to idle and the LED shows normal
operation; `#Info` shows *Calibrated*, the pole pairs, the resistance and inductance, Kt and KV, the phase order
and the commutation direction.

## When to calibrate again

- After changing the motor, the magnet or the wiring.
- After restoring the defaults.
- After a firmware update that clears the calibration (a release note says so when it does).

A calibration that reports success but a motor that runs badly afterwards usually means the magnet moved on the
shaft between calibration and use: fix the magnet and calibrate again.

## Troubleshooting

| Message | Cause |
|---|---|
| `Magnet test: Failed` | no magnet, magnet too far (more than about 1.5 mm), or an axially magnetised magnet |
| `Vbus test: Failed` | supply off, too low, or the cable the wrong way round (if the driver survived it) |
| `Resistance test: Failed`, `Inductance test: Failed` | a phase not connected or shorted; a motor far outside the 2 to 24 Ω range |
| the motor wobbles left and right and the routine fails | one phase is not connected |
| `Open loop: Failed` | the motor did not turn: a phase open, the open-loop voltage (`#Openv`) too low for a high-resistance motor, the supply's current limit set too low |
| `Commutation/alignment check failed!` | the motor did not respond to the current command: a phase open, a current limit at 0, a magnet that slips. Run `#Cal` again. Firmware 101 printed `Phase order is wrong! Switch motor phases and try again!` here; since 105 the wiring is compensated and swapping wires does not help |
| the routine stops in a step and prints nothing more | reset the driver (`#Reset`) and try again |
| success, but the LED stays on and no error is reported | `#Info` shows `-1` somewhere: the EEPROM is not in the firmware's layout; restore the defaults and calibrate again |
| the resistance, KV or Kt look wrong | the supply was not 24 V, or the motor is one of the uneven ones; see the note above |

Calibration runs over the serial connection only: a terminal, or Motor GUI over the serial adapter, not over CAN.
