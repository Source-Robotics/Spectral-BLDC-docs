# With Python

The `Spectral-BLDC` library wraps the CAN protocol: one method per message, and the driver's answers unpacked into
attributes. It runs on Windows, Linux and macOS with any adapter `python-can` supports, such as the CANvas adapter
over slcan.

## Installing

In a virtual environment:

=== "Windows"
    ```
    py -m venv .venv
    .venv\Scripts\activate
    pip install Spectral-BLDC
    ```
    The CANvas adapter is `COM` and a number (Device Manager, **Ports (COM & LPT)**): `channel='COM41'`.

=== "Linux"
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install Spectral-BLDC
    sudo usermod -aG dialout $USER     # access to the serial port; log out and in again once
    ```
    The CANvas adapter is `/dev/ttyACM0` (`ls /dev/ttyACM*` lists it): `channel='/dev/ttyACM0'`.

=== "macOS"
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install Spectral-BLDC
    ```
    The CANvas adapter is `/dev/cu.usbmodem` and a number (`ls /dev/cu.usbmodem*` lists it):
    `channel='/dev/cu.usbmodem1101'`, with your number.

!!! success "Check"
    `python -c "import Spectral_BLDC"` returns without an error message.

The source and the examples are in [Spectral-BLDC-Python](https://github.com/Source-Robotics/Spectral-BLDC-Python).
For joints with a gear ratio and an offset, the [Source Robotics Toolbox](https://github.com/Source-Robotics/Source-Robotics-Toolbox)
(`pip install SourceRoboticsToolbox`) turns encoder ticks into joint angles.

## The first program

```python
import Spectral_BLDC as Spectral
import time

# the adapter: a CANvas on COM41 (Windows) or /dev/ttyACM0 (Linux), 1 Mbit/s
comms = Spectral.CanCommunication(bustype='slcan', channel='COM41', bitrate=1000000)
# the driver with node ID 0
motor = Spectral.SpectralCAN(node_id=0, communication=comms)

motor.Send_Clear_Error()

# A configured, calibrated motor with a clear shaft: command one turn for five seconds.
# Each command requests a fresh position/speed/current reply; heartbeat is not required.
try:
    deadline = time.monotonic() + 5.0
    next_cycle = time.monotonic()
    while time.monotonic() < deadline:
        motor.Send_data_pack_1(Position=16384, Speed=0, Current=0)
        reply_deadline = min(deadline, time.monotonic() + 0.02)
        while time.monotonic() < reply_deadline:
            message, ids = comms.receive_can_messages(
                timeout=max(0.0, reply_deadline - time.monotonic()))
            if message is None:
                print("No motion feedback in this cycle; check the bus and node ID")
                break
            if ids.node_id != 0 or ids.command_id != 3:  # Respond_data_pack_1
                continue
            motor.UnpackData(message, ids)
            print(motor.position, motor.speed, motor.current, ids.error_bit)
            if ids.error_bit:
                raise RuntimeError("Driver fault: inspect State_of_Errors before retrying")
            break
        next_cycle += 0.02
        time.sleep(max(0.0, next_cycle - time.monotonic()))
finally:
    motor.Send_Idle()                    # also on Ctrl-C; the shaft no longer holds torque
```

`receive_can_messages` returns the raw `python-can` message and a tuple with the node ID, the command ID and the
error bit of the identifier; `UnpackData` decodes the message into the attributes the message carries. This example resends the same
setpoint at 50 Hz for five seconds, prints only matching motion feedback, and puts the motor in idle when it
ends. Idle releases torque: support any attached mechanism before running it. A missing reply is reported
without claiming that a move finished. Configure and calibrate the driver first ([Quick start](https://docs.source-robotics.com/Spectral-BLDC-docs/107/quick-start/)).

!!! success "Check"
    The program prints a line of position, speed, current and error bit for each cycle, the position moves to
    16384 and the error bit stays 0. `No motion feedback in this cycle` means no answer came back: the port, the
    node ID and the bus, see [Over CAN](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/can/).

## What is where

| Library call | Message | What you get back |
|---|---|---|
| `Send_data_pack_1(Position, Speed, Current)` | Send_data_pack_1 | `position`, `speed`, `current` |
| `Send_data_pack_PD(...)` | Send_data_pack_PD | `position`, `speed`, `current` |
| `Send_Respond_Encoder_data()` | Send_Respond_Encoder_data | `position`, `speed` (32-bit) |
| `Send_Respond_State_of_Errors()` | Send_Respond_State_of_Errors | the error attributes |
| `Send_gripper_data_pack(...)` | Send_gripper_data_pack | `gripper_position`, `gripper_current`, the gripper state bits |
| `Send_Limits(...)`, `Send_Velocity_Gains(...)`, ... | the setting messages | nothing; `Send_Save_config()` keeps them |

The complete map of calls to messages is in the [Python library](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/python/) reference, and each
message's bytes in the [CAN reference](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/).

## Several motors

One `CanCommunication` per bus, one `SpectralCAN` per driver with its node ID. Send to each, then read the bus:
every answer carries the node ID in `ids.node_id`, so route it to the right object.

```python
motors = [Spectral.SpectralCAN(node_id=i, communication=comms) for i in range(3)]
for m in motors:
    m.Send_Respond_Encoder_data()
for _ in motors:
    message, ids = comms.receive_can_messages(timeout=0.1)
    if message is not None:
        motors[ids.node_id].UnpackData(message, ids)
```

The [Guides](https://docs.source-robotics.com/Spectral-BLDC-docs/107/guides/) build on this: a quadruped leg, gravity compensation, bilateral teleoperation.
