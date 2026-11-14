# Gripper mode

A driver can run a gripper instead of a joint: the same board, with a state machine that moves a jaw to a
position between open and closed, at a speed, with a current limit that becomes the grip force, and that reports
when it holds something. The [SSG-48 gripper](https://docs.source-robotics.com/SSG48-gripper-docs/) is built on the Spectral Micro this way.

## Turning it on

```
#Gripper 1
#Save
```

`#Default` clears the flag again. Over CAN the flag is parameter 92 from firmware 110: write 1 while the driver is
idle (in any other mode the write is refused), then Send_Save_config.

A driver in gripper mode still answers every other command; the gripper commands only work with the flag set,
except the gripper calibration, which runs with or without it.

## Calibrating the gripper

After every power-up the gripper has to find its end stops: `#Gripcal` or Send_gripper_calibrate. The jaws open
slowly at 500 mA until they stop. Then the push eases to 100 mA for a quarter of a second, and the driver reads the
open end where the jaws rest against the stop. The closed end is found the same way.

Position 0 (open) lies 32 ticks inside the open end, and 255 (closed) 16 ticks inside the closed end. So a move to 0
or 255 ends in free travel: it does not press on the stop and reports no object.

Firmware 109 read the ends during the 500 mA push, so 0 and 255 lay inside the stops, and a full open or close kept
pressing on them.

If it has not found both ends within about 30 s it gives up, and the gripper stays uncalibrated. From firmware 110
it also stays uncalibrated when the two ends lie less than 1000 ticks apart: the jaws did not travel.

Check the result with `#Gripinfo` or the `gripper_calibrated` bit of Respond_Gripper_data_pack. From firmware 110
parameter 93 gives the stroke between 0 and 255 in ticks, and 0 while the gripper is not calibrated. The motor
itself must be calibrated (`#Cal`) and saved before that, once.

While the gripper calibrates, send only empty status polls. A 5-byte Send_gripper_data_pack, Send_Clear_Error
or `#Clear` stops the calibration without a message. From firmware 110 the next calibration starts from its first
step, and `#Gripcal` or Send_gripper_calibrate during a calibration starts it again. Firmware 109 went on where
the stopped one left off ([known issue KI-7](https://docs.source-robotics.com/Spectral-BLDC-docs/110/08-troubleshooting/known-issues/)).

## Moving

Over UART:

```
#Gripvel 100       speed, 0 to 255
#Gripcur 400       current limit of the move in mA, the grip force
#Grippos 200       go to position 200 (0 open, 255 closed); also activates the gripper
```

Over CAN, Send_gripper_data_pack carries position, speed and current in one frame with the activate and action
bits; the driver answers with Respond_Gripper_data_pack: the position, the measured current, whether it is moving,
and the object detection:

| Object detection | Meaning |
|---|---|
| 0 | moving |
| 1 | an object was detected while closing: the jaws stopped on it and hold it with the current limit |
| 2 | an object was detected while opening |
| 3 | the position was reached |

From firmware 110 an object (1 or 2) is reported once the jaws have stood still at nearly the move's current for
50 ms. Firmware 109 reported it at the first slow control cycle, also at the start of a move.

From firmware 110 a move starts at the slowest speed and picks up to its own speed within 0.1 s. It slows down over
the last stretch, so it arrives slowly. A new command in the same direction keeps the speed the jaws have, so a host
that streams positions is not slowed.

At the position the driver holds with a small dead zone, a quarter of a position count and at most 16 ticks, and
friction keeps the jaws there: a few mA are left after a move.

On firmware 109 the current took a second or more to settle after every move. From firmware 110 the position the
driver reports is also rounded to the nearest count; 109 cut it off.

An empty Send_gripper_data_pack (0 bytes) only asks for the state. The answer to a 5-byte command goes out
before the driver acts on it, so its object detection and error bits are still those of the moment before
(KI-6); the answers to the next frames show the new move.

The action bit in the answer is a copy of the last command's action bit and stays 1 after the move ends (KI-8): the
object detection tells when it has ended.

Send_gripper_data_pack's E-stop bit raises the gripper E-stop error; `#Gripstop 1` does the same over UART. The
error stays: while the E-stop bit is 1 the driver raises it again on every control cycle (KI-5). To recover,
clear the bit (`#Gripstop 0`, or a Send_gripper_data_pack with the bit 0), then `#Clear` or Send_Clear_Error.

!!! warning "Current"
    From firmware 109 the current you give a gripper move stops at the board's 2800 mA; firmware 107 and older
    did not limit it. The safe range depends on the gripper's mechanics and motor and is lower; the
    [SSG-48 manual](https://docs.source-robotics.com/SSG48-gripper-docs/) gives it for that gripper.

From firmware 110 the move's current is the gripper's own limit. The driver's current limit (`#Ilim`, parameter 16)
stays as you set it, and a `#Save` stores that. Firmware 109 wrote the current of each move into the driver's limit,
and a `#Save` then stored the gripper's current.

## Where the details are

The bytes of the two gripper frames are in the [CAN reference](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can/gripper/), the UART commands in
the [UART reference](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/uart/gripper/).
