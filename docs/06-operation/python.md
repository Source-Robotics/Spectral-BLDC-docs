# With Python

The `Spectral-BLDC` library wraps the CAN protocol: one method per message, and the driver's answers unpacked into
attributes. It runs on Windows, Linux and macOS with any adapter `python-can` supports, such as the CANvas adapter
over slcan.

## Installing

```
pip install Spectral-BLDC
```

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
motor.Send_data_pack_1(Position=16384, Speed=0, Current=0)   # one revolution, position mode

while True:
    message, ids = comms.receive_can_messages(timeout=0.2)
    if message is None:
        continue
    motor.UnpackData(message, ids)        # fills motor.position, motor.speed, motor.current, ...
    print(motor.position, motor.speed, motor.current, ids.error_bit)
    time.sleep(0.01)
```

`receive_can_messages` returns the raw `python-can` message and a tuple with the node ID, the command ID and the
error bit of the identifier; `UnpackData` decodes the message into the attributes the message carries.

## What is where

| Library call | Message | What you get back |
|---|---|---|
| `Send_data_pack_1(Position, Speed, Current)` | Send_data_pack_1 | `position`, `speed`, `current` |
| `Send_data_pack_PD(...)` | Send_data_pack_PD | `position`, `speed`, `current` |
| `Send_Respond_Encoder_data()` | Send_Respond_Encoder_data | `position`, `speed` (32-bit) |
| `Send_Respond_State_of_Errors()` | Send_Respond_State_of_Errors | the error attributes |
| `Send_gripper_data_pack(...)` | Send_gripper_data_pack | `gripper_position`, `gripper_current`, the gripper state bits |
| `Send_Limits(...)`, `Send_Velocity_Gains(...)`, ... | the setting messages | nothing; `Send_Save_config()` keeps them |

The complete map of calls to messages is in the [Python library](../reference/python.md) reference, and each
message's bytes in the [CAN reference](../reference/can/index.md).

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

The [Guides](../guides/index.md) build on this: a quadruped leg, gravity compensation, bilateral teleoperation.
