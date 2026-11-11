# Gripper mode

A driver can run a gripper instead of a joint: the same board, with a state machine that moves a jaw to a
position between open and closed, at a speed, with a current limit that becomes the grip force, and that reports
when it holds something. The [SSG-48 gripper](https://docs.source-robotics.com/SSG48-gripper-docs/) is built on the Spectral Micro this way.

## Turning it on

```
#Gripper 1
#Save
```

`#Default` clears the flag again. A driver in gripper mode still answers every other command; the gripper
commands only work with the flag set, except the gripper calibration, which runs with or without it.

## Calibrating the gripper

After every power-up the gripper has to find its end stops: `#Gripcal` or Send_gripper_calibrate. The jaws move
to both ends; the positions become 0 (open) and 255 (closed). The motor itself must be calibrated (`#Cal`) and
saved before that, once.

While the gripper calibrates, send only empty status polls. A 5-byte Send_gripper_data_pack, Send_Clear_Error
or `#Clear` stops the calibration without a message, and the next one then starts part way through, where the
stopped one left off: switch the driver off and on before you calibrate again
([known issue KI-7](../08-troubleshooting/known-issues.md)).

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
    [SSG-48 manual](https://docs.source-robotics.com/SSG48-gripper-docs/) gives it for that gripper. A gripper
    move also replaces the
    driver's current limit with the move's current, and a later `#Save` keeps that value.

## Where the details are

The bytes of the two gripper frames are in the [CAN reference](../reference/can/gripper.md), the UART commands in
the [UART reference](../reference/uart/gripper.md).
