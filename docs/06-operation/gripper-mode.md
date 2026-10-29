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
commands only work with the flag set.

## Calibrating the gripper

After every power-up the gripper has to find its end stops: `#Gripcal` or Send_gripper_calibrate. The jaws move
to both ends; the positions become 0 (open) and 255 (closed). The motor itself must be calibrated (`#Cal`) and
saved before that, once.

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

An empty Send_gripper_data_pack (0 bytes) only asks for the state. Send_gripper_data_pack's E-stop bit raises the
gripper E-stop error; `#Gripstop 1` does the same over UART.

!!! warning "Current"
    The firmware does not limit the current you give a gripper move. The safe range depends on the gripper's mechanics and motor; the
    [SSG-48 manual](https://docs.source-robotics.com/SSG48-gripper-docs/) gives it for that gripper. The driver's hard limit is 2800 mA.

## Where the details are

The bytes of the two gripper frames are in the [CAN reference](../reference/can/gripper.md), the UART commands in
the [UART reference](../reference/uart/gripper.md).
