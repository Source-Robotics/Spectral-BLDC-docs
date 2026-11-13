# 4. First moves

The motor is calibrated and saved. Now it moves on command.

## 1. Move it

=== "Motor GUI"

    Use the jog controls:

    - *Jog velocity* turns the motor at a speed;
    - *Jog position* moves it to a position;
    - *Jog current* applies a torque;
    - *Send setpoint* sends a value in the current control mode.

    The plots show position, speed and current while it moves.

    ![Motor GUI simulated motor: device state, controls and live telemetry](https://docs.source-robotics.com/Spectral-BLDC-docs/109/assets/motor-gui/motor-demo.jpg){ width="800" }

=== "Terminal"

    ```
    #V 16384        one revolution per second
    #V 0
    #P 0            back to where it started
    #P 16384        one revolution forward
    #Idle
    ```

Position is in encoder ticks, 16384 per revolution; speed in ticks per second; current in mA. If the motor hums
or whines, lower the current limit or tune the loops.

!!! success "Check"
    The position and speed feedback follow the request, and **Idle** stops driving the motor. A motor that
    does not follow needs [Troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/109/08-troubleshooting/) before a load is attached.

More: [Control modes](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/modes/) · [Current limit and loop tuning](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/tuning/).

## 2. Where to go next

| You want to | Read |
|---|---|
| get to know Motor GUI: the screen, the plots, recordings, several motors | [Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/109/05-setup/motor-gui/), [Working in Motor GUI](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/motor-gui/) |
| control the driver from a program over CAN | [Over CAN](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/can/), then [With Python](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/python/) |
| put several drivers on one bus | give each a node ID and terminate the ends: [Power and the CAN daisy chain](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/power-and-can/) |
| protect the motor from overheating | [Thermistor](https://docs.source-robotics.com/Spectral-BLDC-docs/109/04-mounting/thermistor/) |
| update the firmware | [Firmware](https://docs.source-robotics.com/Spectral-BLDC-docs/109/07-firmware/) |
| look up a message or a command | [API reference](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/) |
| build something: a wheeled robot, a leg, a compliant arm | [Guides](https://docs.source-robotics.com/Spectral-BLDC-docs/109/guides/) |
| understand why it does not work | [Errors and recovery](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/errors/), [Troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/109/08-troubleshooting/) |
