# 1. Fit the motor

The driver goes behind the motor, over a magnet on the end of the motor shaft.

## 1. Fit the magnet

1. Press the magnet onto the end of the motor shaft, centred.
2. Glue it, so that it cannot turn on the shaft.

The magnet must end up about **1 mm** above the encoder chip in the middle of the board.

![About 1 mm between the magnet and the encoder chip in the middle of the board.](https://docs.source-robotics.com/Spectral-BLDC-docs/109/assets/mag_dist.webp){ width="560" }

A magnet that slips is the usual cause of a calibration that "succeeds" and a motor that then runs badly.

!!! success "Check"
    The magnet sits centred on the shaft, and once the glue has set it does not move when you push it with a
    finger. If it does: [The encoder magnet](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/magnet/).

More: [The encoder magnet](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/magnet/).

## 2. Mount the board

1. Bolt the bracket to the bottom of the motor.

    ![The example bracket. The motor bolts to one side, the board to the other; the hole in the middle is for the shaft and the magnet.](https://docs.source-robotics.com/Spectral-BLDC-docs/109/assets/brack.webp){ width="500" }

2. Bolt the board to the bracket, with the encoder chip (the bottom of the board) towards the magnet.
3. Check the gap between the magnet and the encoder chip: 1 mm, not touching.

A NEMA 17-format motor takes the board on a spacer with its own rear screws.

!!! success "Check"
    The board sits parallel to the motor, with about 1 mm between the magnet and the encoder chip, and the rotor
    turns by hand without the magnet touching the chip. If not: [Mounting on the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/mounting/).

More: [Mounting on the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/mounting/).

## 3. Wire the motor

Solder the motor's three wires to **U, V and W**. The order does not matter: calibration detects it.

![The connectors. The motor phases go to U, V, W; the supply to DC+ and DC−.](https://docs.source-robotics.com/Spectral-BLDC-docs/109/assets/con2.webp){ width="700" }

!!! success "Check"
    With the driver unpowered, a multimeter shows about the same resistance between U and V, V and W, and W
    and U, and no strand bridges two groups. If not: [Wiring the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/wiring/).

More: [Wiring the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/wiring/).
