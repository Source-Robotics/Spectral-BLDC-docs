# Status and diagnostics

What the driver tells about itself, from firmware 109: what is in force, who it is, its state in one frame, how
long its control loop takes, and recordings of its own signals made inside the control loop. The error flags and
what to do about each are on [Errors and recovery](https://docs.source-robotics.com/Spectral-BLDC-docs/110/06-operation/errors/).

## What is in force

`#Info` ends with the section `In force:`, and parameter 79 holds the same as bits
([What is in force: parameter 79](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can/parameters/#what-is-in-force-parameter-79)):

| Line | Says |
|---|---|
| `encoder table:` | `on, error … deg p-p`, `measured, off` or `not measured` ([Encoder table and anti-cogging](https://docs.source-robotics.com/Spectral-BLDC-docs/110/05-setup/anti-cogging/)) |
| `anti-cogging:` | `on (harmonics)`, `on (table)`, `identified, off` or `not identified`, and `, saved` when it is the saved set |
| `current-sense zero trim:` | the two trims in counts, and whether the zero measured with the bridge switching is in use |
| `delay compensation:` | the commutation delay in µs, or `off` ([Commutation delay compensation](https://docs.source-robotics.com/Spectral-BLDC-docs/110/05-setup/tuning/#commutation-delay-compensation)) |
| `speed estimate:` | `moving average`, `PLL, … Hz` or `direct PLL, … Hz` ([The speed estimate](https://docs.source-robotics.com/Spectral-BLDC-docs/110/05-setup/tuning/#the-speed-estimate)) |
| `input filter:`, `integral deadband:` | parameters 74 and 75, or `off` |
| `running:` | only while one runs: `calibration`, `encoder table`, `anti-cogging identification`, or `the runs after the calibration` |

Before that section `#Info` prints, beside what it printed before:

- `Build:` the git commit the firmware was built from, 7 hex digits, with a `+` when it was built with
  uncommitted changes. `Board ID:` this board, 8 hex digits made from the chip's unique number; it never changes,
  and it is not the bootloader's board ID (0 to 13). `Calibration ID:` a new number at every successful
  calibration, kept by Save; `00000000` before the first. Over CAN they are parameters 84, 86 and 87; parameter
  85 is the build time in Unix seconds.
- `CAN RX overruns` and `CAN TX dropped`: frames the driver lost because its receive buffer was full, and answers
  it gave up after waiting 1 ms for a free transmit mailbox. Both should stay 0; they count from power-up. From
  firmware 109 the CAN controller passes only the frames addressed to the driver's own node ID, and the driver
  sends from all three transmit mailboxes, so a busy bus costs it less.
- `Product:` this firmware, Spectral Micro.
- `Current sense zero:` the zeros in use, in ADC counts from 2048, measured at start-up with the bridge off (one
  count is about 1.6 mA), and what the second measurement with the bridge switching found. On the bench the zeros
  were −8 and −7 counts, and the current read 3.9 mA with nothing flowing, where it read −20 to +19 mA before. A zero more than 200
  counts from 2048 is not trusted: the driver then uses 2048 and says `not measured or out of range`.
  The current sensors need the motor supply. If the driver starts without it (USB plugged in before the supply),
  it waits up to half a second for the supply, then uses 2048 and says
  `no motor supply at start-up: 2048 used; measured once the supply is there`. When the supply comes, the driver
  measures the zero by itself at rest, coasting for about 100 ms even if it is set to brake, and the line shows the
  new zeros. The Vbus error the late supply latched stays until `#Clear`.
- `Tool ID`, `Watchdog: … ms, action …, fallback …`, `Settings block 2: ok` and `Anti-cogging: …, scale … %` with
  whether it is saved.

## Who the drive is: the identity frame

Send_Respond_Identity (ID 39, a remote frame) answers with the product (1 STEPFOC, 2 Spectral Micro), the tool id,
the firmware release, the hardware version, the pole pairs, whether it is calibrated, and eight flags: set up as
a gripper, brakes in idle, coils reversed, settings block 2 available, wrong product, current-sense zero measured,
anti-cogging saved, switching zero in use ([Send_Respond_Identity](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can/status/#send_respond_identity)).

A host can read it before it commands or flashes a drive, to know it talks to the drive it expects.

The **tool id** says what the drive is built into:

- 0: none (a joint or a bare driver);
- 1: an SSG-48;
- 11 to 33: an MSG (the tens digit the rail, 1 = 100, 2 = 150, 3 = 200 mm; the units digit the stepper, 1 = 21.5,
  2 = 40, 3 = 60 mm);
- 200 to 254: your own tools.

Set it with `#Tool` or parameter 1 and save.

## Everything at once: telemetry

Send_Respond_Telemetry (ID 40, a remote frame) answers with the temperature, the supply voltage, both error bytes
and the current, all from the same moment: one request instead of four, for a host that watches many drives
([Send_Respond_Telemetry](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can/status/#send_respond_telemetry)).

## The product lock

STEPFOC and the Spectral Micro use the same bootloader and the same file name for their firmware, and each
firmware drives the other board wrongly: the Spectral Micro firmware on a STEPFOC drove a coil at about 1.7 A in
every mode on the bench.

From firmware 109 a board remembers which product calibrated it, a stamp in the EEPROM written at the first start-up
of a calibrated board and at every save.

A firmware that finds the other product's stamp, or no stamp but a calibration its own product cannot make (the
Spectral Micro firmware treats 50 pole pairs or more as a STEPFOC calibration), reads and writes nothing more, drives
no pin (its gate driver is enabled only after the check) and starts no control loop.

It stays reachable: it reports an error, `Wrong firmware for this board (product lock)` in `#Error`, the
`wrong_product` bit in the error state and the identity, and a warning in `#Info`. Flash the right firmware and the
board runs as before; nothing was written.

`#Product` shows the stamp. On a board the rule misjudges, `#Product claim` stamps it as this product and
`#Product clear` removes the stamp; power-cycle after either. Both are UART commands only.

## How long the control loop takes

The control loop runs every 200 µs (5000 Hz) and has to finish inside that. `#Info` prints the last loop's time.
On the bench an early build of firmware 109 took about 80 µs of the 200; anti-cogging and the commutation delay
compensation each add some 10 µs (measured on STEPFOC).

The section timing and the register fast paths of the STEPFOC firmware (its parameters 66 to 72) are not in the
Spectral Micro firmware.

## A capture

The capture records three signals inside the control loop, sample by sample, 1024 samples per channel: what the
loop saw and did, which a host polling over the bus cannot see. Parameters 24 to 33 set it up and report on it,
Send_Buffer_Read with kind 0 reads it ([Reading the capture](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can/parameters/#reading-the-capture);
the signals are listed under [Capture and histogram](https://docs.source-robotics.com/Spectral-BLDC-docs/110/reference/can/parameters/#capture-and-histogram)).

A step response, 1024 samples of speed, current and position error, one every 2 loops (0.41 s):

```python
import time
import Spectral_BLDC as Spectral

comms = Spectral.CanCommunication(bustype='slcan', channel='COM41', bitrate=1000000)
motor = Spectral.SpectralCAN(node_id=0, communication=comms)

def read_all(seconds):
    end = time.time() + seconds
    while time.time() < end:
        message, ids = comms.receive_can_messages(timeout=0.01)
        if message is not None:
            motor.UnpackData(message, ids)

for number, value in ((24, 4), (25, 1), (26, 7), (27, 2), (28, 1)):
    motor.Send_Parameter(number, value)     # A speed, B Iq, C position error; every 2nd loop; start now
motor.Send_data_pack_1(1000, 0, 0)          # the step: to position 1000
read_all(0.5)
motor.Send_Get_Parameter(32)                # how many samples
read_all(0.1)
count = motor.parameters.get(32, 0)
motor.Send_Buffer_Read(0, 0, count)         # kind 0, from sample 0
read_all(3.0)
for i in sorted(motor.capture):
    speed, iq, position_error = motor.capture[i]
    print(i, speed, iq, position_error)
```

Trigger 2 records up to an error instead: armed with a pre-trigger, it keeps the moments before a trip, the
watchdog's included, and the time after it. The capture calls (`Send_Parameter`, `Send_Get_Parameter`,
`Send_Buffer_Read`) need the Spectral-BLDC library 1.21 or newer.

## Memory

The drive's microcontroller has 128 KB of flash, of which the bootloader takes 12 KB, and 20 KB of RAM. Firmware
109 uses about 91.5 % of the 116 KB application flash and 65 % of the RAM for fixed data, which leaves about
7 KB for the stack and the heap.

Parameter 83 (`#Par 83`, or Send_Get_Parameter(83)) is the margin check: the bytes of that RAM the stack has never
reached since start-up. The stack needs about 1.5 to 2 KB; read parameter 83 after the drive has run its hardest work
(a calibration, the encoder table, the anti-cogging, sound) and see that plenty is left.

## A histogram

The histogram adds one signal into 256 bins over the electrical angle or over one motor turn, every control loop,
until it is stopped or a bin holds 65535 samples (about an hour): the mean per bin shows what repeats with the
angle, such as the cogging current at a steady speed.

Parameter 35 picks the signal, 34 starts it (1 electrical angle, 2 motor turn) and stops it (0), 36 counts the
samples, and Send_Buffer_Read with kind 1 reads the count and the sum of each bin. The anti-cogging identification
uses it the same way.
