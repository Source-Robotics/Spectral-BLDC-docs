# The encoder magnet

The encoder reads a diametrically magnetised magnet on the end of the motor shaft. The magnet must sit centred on
the shaft's axis, parallel to the board, about **1 mm** above the encoder chip, and it must not move. Every
calibration problem that is not a wiring problem comes from this magnet.

<figure markdown="span">
  ![Magnet distance to the encoder](../assets/mag_dist.png){ width="700" }
  <figcaption>Figure 6: About 1 mm between the magnet and the encoder chip in the middle of the board.</figcaption>
</figure>

## The magnet

A neodymium disc, **diametrically** magnetised (north and south across the diameter, not through the thickness).
The shop's [6 × 2.5 mm diametrical magnet](https://source-robotics.com/products/6x2-5mm-diametrical-neodymium-magnet)
is the stock size. An axially magnetised magnet looks the same and does not work: the magnet test may even pass,
and the position is wrong.

!!! note "The size is not fixed"
    6 × 2.5 mm is the stock size, not a requirement. Any diametrically magnetised disc of about 6 mm diameter
    works, and the thickness is a way to set the gap: a thicker magnet brings its face closer to the encoder, a
    thinner one farther, so with a shaft or a bracket that leaves the wrong distance you can pick the thickness
    that gives 1 mm instead of changing the bracket. What matters is the 1 mm from the magnet's face to the chip,
    the magnet centred on the shaft, and the diametrical magnetisation.

## Fitting it

1. The magnet goes on the end of the shaft that faces the board. On most gimbal motors the shaft ends at the
   bottom of the motor, flush with the housing or a little proud of it, and the board is mounted on that side
   ([Mounting on the motor](mounting.md)). On a motor whose shaft ends inside the housing, a short holder pressed
   into the shaft's end carries the magnet out to where the board can see it.
2. Press the magnet on, centred on the shaft's axis. A magnet that sits off-centre wobbles its field as the shaft
   turns and gives a position error that repeats every revolution.
3. Fix it with a drop of glue. A magnet that can turn on the shaft is the classic cause of a calibration that
   reports success and a motor that then runs badly: the magnet slipped between calibration and use.
4. Check the height after the board is mounted: 1 mm, the magnet not touching the chip. A magnet that touches
   the chip can destroy the microcontroller; a magnet 2 mm away or more gives a weak signal.

## Checking it

With the driver powered and the serial terminal open, `#Magnet` answers `Magnet Good` when the chip sees enough
field, `Magnet Bad` when it does not. The calibration routine runs the same test first. "Good" means the field is
strong enough; it does not prove the magnet is centred or that it cannot slip.
