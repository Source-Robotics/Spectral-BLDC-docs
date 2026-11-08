<!-- One shared glossary, included by the Glossary page. Keep entries alphabetical. -->

**Activated**
:   Two flags with the same name. The controller's flag is set by `#Activate` and reported in
    Send_Respond_State_of_Errors; nothing else uses it. The gripper's activate bit is set by `#Gripact`, `#Grippos`
    and Send_gripper_data_pack; in gripper mode a move is carried out only while it is set.

**Angle offset** (theta offset)
:   The angle between the encoder's zero and the motor's electrical zero, found by calibration and stored. The
    driver needs it to place the current vector relative to the rotor.

**Anti-cogging**
:   A current added to the current setpoint, a function of the electrical angle, that cancels the motor's own
    torque ripple (the pull of its magnets towards the stator's teeth and the ripple of current-sensing errors).
    Identified on the driver (`#Cogcal`, parameter 43; firmware 109 and newer).

**Back-EMF**
:   The voltage a turning motor generates in its own windings, proportional to speed. It opposes the supply, limits
    the top speed at a given voltage, and is what calibration measures to find KV, Kt and the flux linkage.

**Board ID**
:   The bootloader's own address, 0 to 13, stored in its configuration page. The firmware sets it to the CAN node
    ID when the configuration is saved.

**Bootloader**
:   The program in the first 12 KB of the driver's flash on boards that run firmware 104 or newer. It starts the
    firmware, and loads a new firmware over UART or CAN. See [The bootloader](07-firmware/the-bootloader.md).

**Calibration**
:   The routine (`#Cal`) that checks the magnet and the supply, measures the motor's resistance and inductance,
    computes the current loop gains, spins the motor in open loop to find the pole pairs and the phase order, aligns
    the encoder to the rotor field and measures Kt, KV and the flux linkage. Its result is kept with `#Save`.

**CAN ID** (node ID)
:   The address of the driver on the CAN bus, 0 to 13 (the field holds 0 to 15, but the bootloader reserves 14 and
    15). It occupies bits 10 to 7 of the 11-bit CAN frame identifier; the command ID occupies bits 6 to 1 and the
    error bit is bit 0.

**CANvas**
:   Source Robotics' USB-to-CAN adapter. It appears as a serial port and speaks slcan, which `python-can` and Motor
    GUI use.

**Clarke and Park transforms**
:   The two steps that turn the three phase currents into the two components FOC regulates: Clarke reduces the three
    phases to two axes fixed to the stator, Park turns those into the frame that rotates with the rotor (the d-q
    frame).

**Command ID**
:   The number, 0 to 63, in bits 6 to 1 of a CAN frame identifier that says which message the frame carries. The
    API reference lists every command ID.

**Commutation**
:   Placing the stator current so that it produces torque at the rotor's present angle. FOC does it continuously
    from the encoder angle and the angle offset; a hobby ESC does it in six steps from the back-EMF, which fails at
    standstill.

**Commutation delay compensation** (parameter 64)
:   Turning the output voltage forward by the angle the rotor covers between the angle reading and the moment the
    voltage reaches the motor. Off on the Spectral Micro until it is measured.

**Control mode**
:   What the driver is doing with the motor: idle, position, velocity, current, PD (impedance), voltage torque, open
    loop, gripper, or calibration. A command that carries a setpoint puts the driver in the matching mode.

**Current loop bandwidth** (`#Cbw`, parameter 49)
:   How fast the current loop follows a change of its setpoint, in Hz. The current loop gains follow from it and
    the motor's resistance and inductance: Kp = ω·L, Ki = ω·R. 160 Hz by default from firmware 109 (500 Hz before).

**Current-sense zero**
:   The reading of a current sensor with no current flowing. From firmware 109 the driver measures it at every
    start-up and subtracts it.

**Daisy chain**
:   Several drivers on one CAN bus and one supply, each driver's second CAN and power connector feeding the next.

**d-q frame**
:   The rotating frame of reference FOC works in: the q axis is at right angles to the rotor field and the current on
    it (Iq) produces torque; the d axis is along the field and its current (Id) produces none, so it is held at 0.

**Diametrical magnet**
:   A disc magnet whose poles are across its diameter, so the field turns with the shaft. The encoder needs this
    kind; an axially magnetised disc looks the same and does not work.

**EEPROM**
:   The non-volatile memory on the driver that holds the configuration and the calibration. `#Save` writes it,
    `#Default` restores the factory values.

**Encoder table**
:   A correction of the encoder's small angle error around the turn, measured on the driver (`#Encal`, parameter
    52) and saved with the configuration (firmware 109 and newer).

**Encoder ticks**
:   The unit of position: the 14-bit magnetic encoder gives 16384 ticks per revolution of the motor shaft, counted
    over as many revolutions as the motor makes. Speed is in ticks per second.

**Error bit**
:   Bit 0 of every CAN frame identifier the driver sends: 1 while any error is active.

**Feedforward**
:   A term added to a loop's output from what is known in advance rather than from the error: the motion frames
    carry a speed and a current feedforward so a host that knows the trajectory can command it directly, leaving
    the loops to correct the rest.

**Field-oriented control** (FOC)
:   Controlling a motor by regulating the stator current as a vector in the rotor's frame, from a measurement of the
    rotor angle. The three phase currents are reduced to a torque-producing and a field-producing component, each
    regulated by its own loop, which gives smooth torque at any speed down to standstill, a known position, and
    the most torque per ampere.

**Firmware release**
:   One build of the firmware, numbered 101, 104, 105, … and tagged `v101`, `V104`, `V105`, … in the firmware
    repository. `#Info` prints the release a driver runs. This documentation describes one release; the version
    selector switches between them.

**Flux linkage**
:   The rotor's magnetic flux as seen by a winding, in weber; found by calibration from the back-EMF, together with
    KV and Kt.

**Gimbal motor**
:   A brushless motor wound with many turns of thin wire for low speed and smooth torque at low current, originally
    for camera gimbals: a phase resistance of a few ohms to a few tens of ohms, and many pole pairs. The kind of
    motor the Spectral Micro is made for.

**Gripper mode**
:   The driver running a gripper (`#Gripper 1`): jaw positions from 0 (open) to 255 (closed), a speed, a current
    limit that becomes the grip force, and object detection.

**Heartbeat**
:   A frame (Respond_Heartbeat) the driver sends at a set interval so the host knows it is alive. Off by default.

**Iq, Id**
:   The two components of the motor current in the d-q frame: Iq produces torque, Id is normally held at 0. The
    current mode's setpoint and limit are Iq values.

**Impedance (PD) mode**
:   The control mode in which the driver behaves like a spring and a damper around a position setpoint, with the
    stiffness `KP` and the damping `KD`, plus a current feedforward.

**Kt, KV**
:   The motor's torque constant (torque per ampere) and velocity constant (speed per volt), found by calibration.
    Kt turns a current into an estimated torque; KV gives the top speed at a supply voltage.

**Motor GUI**
:   Source Robotics' browser tool for the driver: setup, calibration, tuning, plots and firmware updates over a
    serial or CAN adapter.

**Open loop**
:   Turning the stator field at a set electrical speed without the encoder in the loop, so that the rotor follows it
    like a stepper: `#Openloop`, and the open-loop spin of the calibration that finds the pole pairs.

**Parameter**
:   A setting reached by its number through Send_Parameter and Send_Get_Parameter (CAN 36 to 38) or `#Par`
    (firmware 109 and newer). The numbers are permanent.

**Phase order**
:   The order in which the motor's three phases are connected to U, V and W. Firmware 105 and newer learns it during
    calibration and compensates it; firmware 101 asks for two wires to be swapped when it is reversed.

**PIN** (ADDITIONAL)
:   The spare pin of the driver, on the three-pad header next to the UART connector, usable as an analog input or a
    digital input/output. The firmware's name for it is ADDITIONAL.

**PLL (speed estimate)**
:   A phase-locked loop that follows the encoder count and gives the speed with less lag than a moving average
    (parameter 50, firmware 109 and newer; the moving average stays the Spectral Micro's default).

**Pole pairs**
:   The number of electrical cycles per mechanical revolution, half the number of rotor magnets: 7 for a typical
    2804 gimbal motor, 11 for a 5208, 14 for an 8108. Calibration finds it; `#PP` sets it by hand.

**Product lock**
:   The stamp in the EEPROM of the product that calibrated a board. A firmware that finds the other product's
    stamp drives nothing (firmware 109 and newer).

**Remote frame**
:   A CAN frame with the RTR bit set and no data: a request. The host asks for data with a remote frame under a
    command ID, and the driver answers with a data frame under the same ID.

**Sound** (`#Tone`, CAN 44 and 45)
:   Tones, a queue of notes and recorded samples the driver adds to its output voltage while it holds or moves, so
    the motor plays them (firmware 109 and newer).

**STEPFOC**
:   Source Robotics' stepper driver, the Spectral Micro's sister: similar hardware and firmware and practically
    the same commands, for two-phase stepper motors.

**Termination**
:   The 120 Ω resistor the first and the last node of a CAN bus need. The switch on the driver turns it on.

**Tool id** (`#Tool`, parameter 1)
:   What a drive is built into: 0 none, 1 SSG-48, 11 to 33 an MSG, 200 to 254 a customer's tool.

**Vbus**
:   The supply voltage at the driver, measured and printed in mV. Outside the limits the driver raises a Vbus
    error.

**Watchdog**
:   A timer the driver resets with every motion command and status request it receives over CAN. When it is set
    (Send_Watchdog) and runs out, the driver reports a watchdog error and stops; from firmware 109 it holds,
    brakes, coasts or descends as the watchdog's action says.
