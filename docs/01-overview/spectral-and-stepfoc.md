# Spectral Micro and STEPFOC

The [STEPFOC stepper driver](https://docs.source-robotics.com/STEPFOC-docs/) is built on the same board and the
same firmware as the Spectral Micro. The Spectral Micro drives three-phase brushless motors; STEPFOC drives
two-phase stepper motors. Everything else is shared: the microcontroller, the encoder, the connectors, the CAN and
UART interfaces, the Python library, Motor GUI and the bootloader.

What this means in practice:

- **The commands are the same.** Every CAN message and UART command in the API reference exists on both drivers,
  with the same IDs, names and layouts; STEPFOC adds a few that only make sense on a stepper (homing against a
  sensor, open-loop stepping). A program written for one runs on the other.
- **The firmware releases go in step.** A Spectral Micro release has a STEPFOC counterpart with the same changes;
  the [compatibility table](../appendix/compatibility.md) lists the pairs. The numbers differ by one (Spectral
  Micro 107 is STEPFOC 108).
- **Calibration differs.** The Spectral Micro measures the motor's resistance and inductance and finds its pole
  pairs; STEPFOC cannot, so there the three values are entered from the motor's datasheet first.
- **The motor terminals differ.** U, V and W for the three phases, instead of A+, A−, B+, B− for the two coils of
  a stepper.
- **The grippers differ.** The [SSG-48 gripper](https://docs.source-robotics.com/SSG48-gripper-docs/) is driven by
  a Spectral Micro, the [MSG gripper](https://docs.source-robotics.com/MSG-gripper-docs/) by STEPFOC; both use the
  driver's [gripper mode](../06-operation/gripper-mode.md).

The guides under the Guides tab were written with the Spectral Micro; the code in them runs unchanged on STEPFOC.
