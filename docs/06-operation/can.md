# Over CAN

CAN is the interface for running a machine: compact frames, a fixed cost per message, up to 16 drivers on one bus,
and a host that can be a PC, a microcontroller or a robot control box. The driver answers a motion command with
its position, speed and current in the same frame exchange, so a control loop on the host needs one frame out and
one frame back per motor and cycle.

## The frame

CAN 2.0 data frames with 11-bit identifiers at 1 Mbit/s. The identifier carries the node, the command and the
error state:

<figure markdown="span">
  ![The CAN identifier](../assets/CANID.PNG){ width="600" }
  <figcaption>Figure 16: Bits 10 to 7 of the identifier are the node ID, bits 6 to 1 the command ID, bit 0 the error bit.</figcaption>
</figure>

- **Node ID**, bits 10 to 7: which driver, 0 to 15. A driver acts only on frames with its own node ID and sends
  with it. Set it with `#CANID` or Send_CAN_ID and save; every driver ships as node 0.
- **Command ID**, bits 6 to 1: which message, 0 to 63. The [CAN reference](../reference/can/index.md) lists all of
  them.
- **Error bit**, bit 0: in a frame from the driver, 1 while any error is active. In a frame from the host it is
  ignored.

So a host sends Send_data_pack_1 (command 2) to node 3 with the identifier `(3 << 7) | (2 << 1)` = 0x184, and the
driver answers with command 3 under `(3 << 7) | (3 << 1) | error`. A lower node ID wins the bus arbitration.

Multi-byte values are big-endian: the most significant byte is in data[0] and goes first. Floats are IEEE 754
single precision. Flags inside a byte are numbered from the most significant bit.

## Three kinds of message

- **Send_…**: the host sends data. Some of these are answered (a motion command with Respond_data_pack_1, the
  gripper command with Respond_Gripper_data_pack); most are not.
- **Send_Respond_…**: the host asks for data with a **remote frame** (the RTR bit set, no data) carrying the
  command ID; the driver answers with a data frame with the same command ID.
- **Respond_…**: frames only the driver sends: the answers above, and the heartbeat.

## A control loop

Send Send_data_pack_1 at a fixed rate, 100 Hz to 1 kHz, with the setpoint for this cycle; read Respond_data_pack_1
for the position, speed and current of the last cycle. Every valid frame resets the watchdog, so with
Send_Watchdog set to a few cycle times the motor stops when the host stops. The heartbeat is the other way round:
Send_Heartbeat_Setup makes the driver send a frame on its own every N ms when it has nothing else to send, so the
host can see it is alive.

## From a PC

The [CANvas adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter) shows up as a serial port and
speaks slcan; `python-can` opens it with `bustype='slcan'`. The Python library wraps the whole protocol, see
[With Python](python.md). Any CAN adapter that `python-can` supports works the same way.

## Several drivers

Give each driver its own node ID before you put them on one bus (a bus with two node 0s cannot tell them apart):
connect one driver at a time over UART, `#CANID 3`, `#Save`. Terminate the first and the last node, and wire the
daisy chain as in [Power and the CAN daisy chain](../04-mounting/power-and-can.md).
