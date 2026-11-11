# Calibration

Calibration teaches the driver its motor. It checks the magnet and the supply, then measures the motor's phase
resistance and inductance and computes the current loop gains from them.

It spins the motor in open loop to find the pole pairs and the direction, checks the order of the phases and
aligns the encoder to the rotor field, and measures the motor constants Kt, KV and the flux linkage. Nothing about
the motor has to be entered first.

It runs once per motor; the result is kept by saving. From firmware 109 every `#Cal` goes on by itself to two more
runs, the [encoder table and the anti-cogging](anti-cogging.md), and saves. `#Calonly` is the calibration alone.

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
| Current loop bandwidth | 160 Hz | `#Cbw` | the bandwidth the current loop gains are computed for (Kpiq ≈ ω·L, Kiiq = ω·R·T, with ω = 2π × the bandwidth and T the 200 µs control period); too high makes the motor vibrate and whine. 500 Hz up to firmware 107 |
| Resistance voltage | 1000 mV | `#Resv` | the voltage the resistance measurement starts at; it rises until the power reaches the limit below |
| Max power dissipation | 12 W | `#Calpwr` | the power the resistance and inductance measurements may put into the motor |
| Open loop voltage | 5000 mV | `#Openv` | the voltage of the open-loop spin that finds the pole pairs |
| Open loop speed | 20 rad/s | `#Opens` | the electrical speed of that spin |
| Phase search voltage | 5000 mV | `#Vp` | the voltage of the spin that checks the phase order |

A seventh setting is not printed: `#Iqoffset`, 300 mA by default, the current of the angle-offset search and of
the commutation check. None of the seven is saved; after a power cycle they are back at these defaults. The
current gains the bandwidth gives are saved with the calibration.

!!! danger "Low-resistance motors"
    These voltages are made for motors of 2 Ω and more. On a motor with a much lower resistance, such as a drone
    motor, they drive a destructive current. The Spectral Micro is not made for such motors; if you must try one,
    lower the three voltages first. Lowering the current limit does not help: calibration sets its own.

!!! warning "Calibration sets its own current limit"
    The routine does not use the current limit you set. It raises the limit to 1600 mA, and drives the motor with
    up to 1250 mA while it measures Kt and KV and with `#Iqoffset` while it aligns the encoder. From firmware 109 it
    puts the limit that was in force back when it ends; firmware 107 and older left 1600 mA in force (known issue
    KI-2).

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

This also sets the hardware version and batch date to factory values, and clears an encoder table and an
anti-cogging set from another motor; note what `#Info` printed if you need them. From firmware 109 the CAN node
ID is kept. [Saving the configuration](saving.md) says what else it does.

## 2. Run it

=== "Motor GUI"
    Start the calibration. The driver enters *Calibration mode* and the GUI shows its log step by step; when it
    finishes, the resistance, inductance and pole pairs it measured, the phase order and direction, Kt, KV and the
    flux linkage appear in the settings.

=== "Terminal"
    ```
    #Cal
    ```

The LED flashes fast, about 10 times a second, while the routine runs, and the driver prints each step as it
goes. The numbers below are those of one tested motor; yours will differ:

```
----------------
Calibration mode
-----Settings-----
Current loop bandwidth: 160.00Hz
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
Calibrating angle offset... stage 1/13, sweep point 0
Calibrating angle offset... stage 2/13, sweep point 0
...
Phase order = 2
Phase order is good!
KV is: ...
Kt is: ...
KV runs: ... ... ... ... (same direction within ... %)
Flux linkage is: ...
----------------
Calibration success!
Next, by itself: the encoder table, then anti-cogging (about a minute; keep the shaft free). Everything is saved when they finish (#Encal state, #Cogcal state)
Going to idle!
----------------
```

The `Calibrating angle offset...` lines come every half second while the encoder is aligned, which can take
about 40 seconds; the routine has not stopped.

`#Calonly` runs the same calibration and nothing after it; it ends with `Save config with #Save` instead.

What the steps are:

| Step | What happens | Fails with |
|---|---|---|
| Magnet test | the encoder sees enough field: a magnet is there and close enough. The test says nothing about centring, the gap or the glue | `Magnet test: Failed`: magnet missing, too far, or axially magnetised |
| Vbus test | the supply is within limits | `Vbus test: Failed` |
| Resistance | a rising voltage is put on the windings and the current measured; the motor clicks. The resistance follows from the two | `Resistance test: Failed`: no current flows, a phase is not connected, or the motor is far outside the 2 to 24 Ω range |
| Inductance | a voltage step and the rate at which the current rises give the inductance. Kp_iq and Ki_iq are computed from R, L and the bandwidth | `Inductance test: Failed` |
| Open loop | the stator field is turned at the open-loop speed and the encoder watched: the pole pairs are the ratio of electrical to mechanical turns, and 1 to 49 are accepted. The direction the rotor turned is remembered as the commutation direction (`Commutation dir` in `#Info`); `Dir` is always 1 after a calibration | `Open loop: Failed`, then `The rotor did not follow the open-loop field (pole pairs must come out as 1 to 49).` and `Check the motor's three wires and that the shaft is free.` |
| Phase order | a current command must move the rotor the expected way, and the encoder's zero is aligned to the rotor field (the angle offset, `#Offset`). A motor that does not respond gets a second try at another angle | `Commutation/alignment check failed!`, `Motor did not respond as expected to a current command...` and a line `Spin-confirm delta: … ticks (need > 8192), Vbus: … mV` that says how far the motor turned (half a revolution is needed) and at what voltage |
| Kt, KV, flux linkage | four spins from standstill, about a second each and alternately forward and back; KV is the mean speed per volt available, and the constants follow from it. `KV runs:` in the log shows all four and how far they agree | nothing. `KV runs disagree` is a warning, not a failure: two runs in the same direction differ by more than 5 %. The shaft was not free, or something held it; calibrate again |

!!! note "The measured values are estimates"
    The resistance, the inductance and the motor constants differ a little from one run to the next, and KV, and
    with it Kt and the flux linkage, can be off by a factor of two or three on cheap motors with uneven windings.
    For the loops this does not matter; for a torque estimate in newton-metres, measure Kt yourself.

## What follows the calibration

Half a second after `Calibration success!` of a `#Cal` the driver starts two runs on its own: the encoder table,
then the anti-cogging identification. Keep the shaft free for about a minute more.

When they succeed, everything is saved. A command from a host (a motion command, `#Idle`) stops them; then nothing is
saved, and the calibration is kept only if you `#Save` it.

A host that takes the drive before they start has 3 s: after that the runs are dropped and do not start later. `#Cal`
always runs them; `#Calonly` never does. [Encoder table and anti-cogging](anti-cogging.md) explains both.

!!! warning "Set the current limit before you calibrate"
    The encoder table turns the field with a current of 80 % of the current limit, for about 20 s. Calibration uses
    its own 1600 mA for its steps and puts the limit that was in force back before the encoder table runs. So set
    `#Ilim` for the motor before `#Cal` (known issue KI-19).

## 3. Set the current limit and save

Calibration puts back the current limit that was in force when it started (firmware 107 and older left
1600 mA). If that is not your motor's yet, set it now ([Current limit and loop tuning](tuning.md)), then save. After
`#Cal` the driver saves by itself when the runs succeed; save anyway once they are done, or after `#Calonly`.

=== "Motor GUI"
    Set the current limit in the limits, then **Save**. The GUI marks *Unsaved changes* until you do.

=== "Terminal"
    ```
    #Ilim 1000
    #Save
    ```

Without it the calibration is gone at the next power cycle. After `#Calonly` the driver is idle. After `#Cal` it
ends the two runs holding the position the shaft reached: `#Idle` releases it. The LED shows normal
operation; `#Info` shows *Calibrated*, the pole pairs, the resistance and inductance, Kt and KV, the phase order
and the commutation direction.

!!! success "Check"
    After a power cycle `#Info` still prints `Calibrated`, and Motor GUI shows *Calibrated*. `Not calibrated`
    means the save did not happen: calibrate and save again.

## When to calibrate again

- After changing the motor, the magnet or the wiring.
- After restoring the defaults.
- After an update from firmware 107 or older to 109, where the motor can turn freely: the older calibration stored
  the resistance and the inductance too low. An assembled SSG-48 keeps its calibration and gets its preset
  ([Upgrading from older firmware](../07-firmware/upgrading.md)).
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
| `Open loop: Failed` | the rotor did not follow the field, or the pole pairs came out outside 1 to 49: a phase open, the shaft not free, the open-loop voltage (`#Openv`) too low for a high-resistance motor, the supply's current limit set too low |
| `Commutation/alignment check failed!` | the motor did not respond to the current command: a phase open, `#Iqoffset` set too low, a magnet that slips. Run `#Cal` again. Firmware 101 printed `Phase order is wrong! Switch motor phases and try again!` here; since 105 the wiring is compensated and swapping wires does not help |
| `Cal: not started, the E-stop is latched (#Clear first)`, or `Stopped by an E-stop: #Clear, then calibrate again.` after `Calibration failed!` | an E-stop is latched or ended the calibration: `#Clear`, then `#Cal`; the alignment starts again from its first stage |
| the routine stops in a step and prints nothing more | reset the driver (`#Reset`) and try again |
| success, but the LED stays on and no error is reported | `#Info` shows `-1` somewhere: the EEPROM holds a value from an older release ([The check at power-up](saving.md#the-check-at-power-up)); restore the defaults and calibrate again |
| the resistance, KV or Kt look wrong | the supply was not 24 V, or the motor is one of the uneven ones; see the note above |

Calibration runs over the serial connection only: a terminal, or Motor GUI over the serial adapter, not over CAN.
