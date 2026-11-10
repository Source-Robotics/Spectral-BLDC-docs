---
status: new
---

# The watchdog

The watchdog stops the motor when the host stops talking: a host program that crashes, a cable that comes out,
a USB adapter that hangs. It is a timer in the driver. Every valid motion frame and every request the driver
answers starts it again; when it runs out, the driver raises the watchdog error and does what its **action**
says. From firmware 109 the action can hold the position, brake, coast, or let a joint down slowly; before, the
driver always disabled the motor, which then coasted.

## Setting it

=== "Python"
    ```python
    motor.Send_Watchdog(_rate=100, _action='Hold')   # 100 ms, then hold the position
    ```
    The library 1.20 knows the actions 'Idle', 'Hold' and 'Brake'; 'Coast' and 'Descend' come with its next
    release.

=== "CAN"
    Send_Watchdog (ID 15): the time in ms (4 bytes) and the action (1 byte). Or the parameters 6 (time) and 7
    (action) with Send_Parameter.

=== "Motor GUI"
    *Watchdog ms* in the settings.

0 ms switches it off, the default. Set it to a few of your host's cycle times: with a 100 Hz loop, 30 to 100 ms.
Send_Save_config keeps it, and a kept watchdog runs from power-up: a host that does not start sending within the
time finds the driver in watchdog error and clears it with Send_Clear_Error.

What starts the timer again: Send_data_pack_1, Send_data_pack_PD, Send_gripper_data_pack, the
status requests (Send_Respond_…), Send_Get_Parameter and Send_Buffer_Read. Setting the watchdog time
(Send_Watchdog, parameter 6) starts a fresh window, and so does Send_Save_config, whose save takes time. What
does not: the other setting frames (gains, limits, Idle, Clear, Settings, Send_Parameter) and every UART command
(known issue KI-11). While the encoder table or the anti-cogging is measured, the driver feeds it itself.

## What a trip does

| Action | Name | What the driver does |
|---|---|---|
| 0 | legacy | what firmware 107 and older did: the motor driver is disabled and the motor coasts |
| 1 | hold | holds the position the motor had at the trip, for the fallback time; then the after-action |
| 2 | brake | shorts the phases at once; the braking current is not limited |
| 3 | coast | leaves the phases open at once: the motor turns freely |
| 4 | descend | applies the fallback current, but never lets the motor turn faster than the fallback speed, for the fallback time; then the after-action |

Any other action byte acts as 0. 0 is also what an unchanged host sends: the Python library's default, and what
the PAR6 runtime sends.

Three rules keep a gentler action from softening the response to a real fault:

- **Only a trip of the watchdog alone** gets the action. If another error is active as well (E-stop, encoder,
  supply voltage, temperature, not calibrated, a gripper E-stop), the driver gives the legacy response.
- **Hold and descend take over only from a running motor**: position, velocity, current, PD or gripper mode. A
  driver that was idle when the watchdog ran out gives the legacy response: the motor coasts, also when it
  braked in idle (`#Brake 1`).
- **Hold and descend always end** after the fallback time, at most 60 s, so a lost host never leaves a motor
  driven for good. The after-action follows: 0 legacy, 2 brake or 3 coast.

The driver reports the watchdog error the whole time, and Send_Clear_Error (or `#Clear`) ends the action at
once and goes to idle; the next motion frame takes over.

### Hold

Hold keeps the position loop on the position the shaft had at the trip. Coming from position or velocity mode it
keeps the velocity integral too, so a joint under load does not sag at the moment of the trip. A host that recovers within the fallback time (a USB
hiccup) finds the joint where it left it. On the bench a gimbal motor held within 6 ticks; with a load pulling on
its shaft the holding current rose to 440 mA while the shaft crept 59 ticks.

### Descend

Descend applies the fallback current and limits the speed in both directions to the fallback speed. Inside the
cap the speed limiter's integral relaxes back to zero (within about 0.25 s), so it holds back only what keeps the
speed at the cap and never more:

- a joint under gravity with 0 mA lowers itself at no more than the cap speed and rests on whatever stops it;
- a gripper with its gripping current keeps its grip, and its jaws cannot slam shut;
- a free motor with a current turns at about the cap speed: on the bench a gimbal motor with 200 mA and a 1000
  ticks/s cap turned at 1145 to 1163 ticks/s, about 15 % over the cap, which is soft because the limiter's
  integral relaxes inside it.

It starts with the velocity integral at zero, so gravity can take the joint down.

## The fallback

Four values, kept by Send_Save_config in settings block 2:

| Parameter | `#WdFb` position | What | Default |
|---|---|---|---|
| 2 | 1st | how long hold or descend runs, ms (0 to 60000) | 2000 |
| 3 | 2nd | the current descend applies, mA (signed) | 0 |
| 4 | 3rd | the speed cap of descend, ticks/s (0 to 65535) | 1000 |
| 5 | 4th | the after-action: 0 legacy, 2 brake, 3 coast | 0 |

=== "Terminal"
    ```
    #WdFb 2000,0,1000,2
    #Save
    ```
    Four numbers, commas, no spaces. `#WdFb` alone prints them, and `#Info` prints the watchdog with them.

=== "Python"
    ```python
    motor.Send_Watchdog_Fallback(2000, current_mA=0, speed=1000, after='Brake')
    motor.Send_Save_config()
    ```
    From the library's next release; with 1.20, Send_Parameter frames 2 to 5 do the same.

## Choosing an action

- **A bare motor on the bench, a conveyor, a wheel**: brake (2) stops it fastest; coast (3) or legacy (0) lets it
  run out.
- **A joint that carries a load**: hold (1) for a second or two, so a short loss of the host does not move it,
  then descend (4) with 0 mA for a joint that gravity pulls down, or brake for one it does not. Choose the cap
  speed for a joint you can still catch by hand.
- **A gripper**: descend with the gripping current, its sign the closing direction, keeps an object held.

These suggestions are untested on an assembled robot arm; try the action on your machine before you rely on it.
Brake is not current-limited (known issue KI-12): a load that drives a braking motor fast drives a large current
through the phases; try it with the motor still first.

## Seeing a trip

A capture armed with the error trigger (parameter 28 = 2) records the moments before and after a trip, the
watchdog's included: [Status and diagnostics](diagnostics.md#a-capture).
