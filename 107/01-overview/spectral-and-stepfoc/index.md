# Spectral Micro and STEPFOC

The Spectral Micro and the [STEPFOC stepper driver](https://docs.source-robotics.com/STEPFOC-docs/) are sister
drivers: similar hardware and similar firmware, each made for its kind of motor. The Spectral Micro drives
three-phase brushless motors; STEPFOC drives two-phase stepper motors. They are not the same board and do not run
the same firmware, but they are controlled and run practically the same way: the same CAN and UART commands, the
same Python library, Motor GUI and bootloader.

What this means in practice:

- **The commands are practically the same.** The CAN messages and UART commands of the API reference exist on both drivers,
  with the same IDs, names and layouts; STEPFOC adds a few that only make sense on a stepper (homing against a
  sensor, open-loop stepping). A program written for one runs on the other.
- **The firmware releases go in step.** A Spectral Micro release has a STEPFOC counterpart with the same changes;
  the [compatibility table](https://docs.source-robotics.com/Spectral-BLDC-docs/107/appendix/compatibility/) lists the pairs. The numbers differ by one (Spectral
  Micro 107 is STEPFOC 108).
- **Calibration differs.** The Spectral Micro measures the motor's resistance and inductance and finds its pole
  pairs; STEPFOC cannot, so there the three values are entered from the motor's datasheet first.
- **The motor terminals differ.** U, V and W for the three phases, instead of A+, A−, B+, B− for the two coils of
  a stepper.
- **The grippers differ.** The [SSG-48 gripper](https://docs.source-robotics.com/SSG48-gripper-docs/) is driven by
  a Spectral Micro, the [MSG gripper](https://docs.source-robotics.com/MSG-gripper-docs/) by STEPFOC; both use the
  driver's [gripper mode](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/gripper-mode/).

The guides under the Guides tab were written with the Spectral Micro; the code in them runs unchanged on STEPFOC.
