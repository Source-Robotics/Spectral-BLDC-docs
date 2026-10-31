# Safety

The Spectral Micro is a bare circuit board that drives a motor from a supply of up to 29 V. Read this chapter before you
connect anything; the few rules here are the ones that destroy a driver, a motor or a finger when they are ignored.

## Electrical

!!! danger "Supply polarity"
    Reversing the polarity on DC+ and DC− destroys the driver at once. Check the polarity of every power cable
    before you plug it in, every time.

!!! danger "Cable orientation on the daisy chain"
    The CAN and power cables that link one driver to the next are keyed by their orientation, not by their
    connector: a cable plugged in the wrong way round puts the supply on the wrong pins and destroys the driver.
    Use the cables from the Source Robotics shop, or make yours exactly as shown in
    [Power and the CAN daisy chain](04-mounting/power-and-can.md).

!!! danger "UART is 3.3 V"
    The UART port runs at 3.3 V. A 5 V serial adapter destroys the board. Use a 3.3 V adapter, such as the one
    from the shop.

!!! warning "Supply voltage"
    12 to 29 V DC. The driver raises a Vbus error outside 9 to 29.5 V, but the hardware limit is 29 V: do not
    connect a supply that can rise above it, and allow for the voltage a decelerating motor pushes back into the
    supply. A bench supply with a current limit is the safest way to start.

!!! warning "Do not disconnect a running motor"
    Never unplug a motor, or a power cable in the daisy chain, while the driver is powered. The inductive kick of
    the windings and the arcing at the connector damage the driver stage.

## Mechanical

!!! danger "Moving parts"
    A calibrating or running motor turns without warning, in both directions, and a motor in position mode pushes back hard against a hand. Keep fingers, hair and cables away from the shaft and whatever is mounted on
    it, fix the motor to the bench before the first test, and test without a load on the shaft.

!!! warning "The encoder magnet"
    The magnet sits about 1 mm above the encoder chip. A magnet that touches the chip, or sits far too close, can
    damage the microcontroller; a magnet too far away gives a wrong position. Mount it as described in
    [The encoder magnet](04-mounting/magnet.md).

!!! warning "Hot motor and driver"
    A motor running at its rated current gets hot enough to burn. Set the current limit for your motor
    ([Current limit and loop tuning](05-setup/tuning.md)), use the thermistor, and give the driver airflow when it
    runs near 2.8 A.

## Stopping the motor

- `Send_ESTOP` over CAN, or `#Idle` over UART, stops the motor at once; the E-stop error stays until it is cleared.
- Cutting the supply stops the motor as well; the motor then holds nothing, so a vertical axis drops.
- The watchdog ([Send_Watchdog](reference/can/system.md)) stops the motor by itself when the host stops talking.

Nothing on the driver is a certified safety function. A machine that can hurt someone needs an emergency stop
that cuts the motor supply, independent of the driver.

## Firmware updates and programming

When you connect a programming adapter to the JTAG connector, disconnect the motor supply and the UART adapter
first. Updating over the bootloader needs no adapter; see [Firmware](07-firmware/index.md).

## Liability

The Spectral Micro is sold as a component for people who build their own machines. Its hardware designs, firmware and this
documentation are under development and may contain errors.
Whoever builds a machine with it is responsible for its safe design, assembly and operation.
