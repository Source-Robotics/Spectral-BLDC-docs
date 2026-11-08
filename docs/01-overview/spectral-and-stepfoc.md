# Spectral Micro and STEPFOC

The Spectral Micro and the [STEPFOC stepper driver](https://docs.source-robotics.com/STEPFOC-docs/) are sister
drivers: similar hardware and similar firmware, each made for its kind of motor. The Spectral Micro drives
three-phase brushless motors; STEPFOC drives two-phase stepper motors. They are not the same board and do not run
the same firmware, but they are controlled and run practically the same way: the same CAN and UART commands, the
same Python library, Motor GUI and bootloader.

What this means in practice:

- **The commands are practically the same.** The CAN messages and UART commands of the API reference exist on both drivers,
  with the same IDs, names and layouts; STEPFOC adds a few that only make sense on a stepper (homing against a
  sensor, open-loop stepping). A program written for one runs on the other. The idle behaviour is the exception
  over UART: the Spectral Micro sets it with `#Brake 0` or `#Brake 1` and coasts by default, STEPFOC has the
  actions `#Brake` and `#Coast`. Send_Settings over CAN is the same on both.
- **The firmware releases go in step, and from 109 share their numbers.** From release 109 the two drivers are
  released together under the same version number; the Spectral Micro went from 107 straight to 109, so there is
  no Spectral Micro 108. Before, the numbers did not always match (Spectral Micro 107 went with STEPFOC 108); the
  [compatibility table](../appendix/compatibility.md) lists the pairs. In 109 some new features were tested on the
  STEPFOC bench first, so the Spectral Micro keeps its earlier defaults for them (the speed estimate, the delay
  compensation, the runs after a calibration) until they are measured on it.
- **Calibration differs.** The Spectral Micro measures the motor's resistance and inductance and finds its pole
  pairs; STEPFOC cannot, so there the three values are entered from the motor's datasheet first. See
  [Calibration](../05-setup/calibration.md).
- **The motor terminals differ.** U, V and W for the three phases, instead of A+, A−, B+, B− for the two coils of
  a stepper.
- **The grippers differ.** The [SSG-48 gripper](https://docs.source-robotics.com/SSG48-gripper-docs/) is driven by
  a Spectral Micro, the [MSG gripper](https://docs.source-robotics.com/MSG-gripper-docs/) by STEPFOC; both use the
  driver's [gripper mode](../06-operation/gripper-mode.md).

The guides under the Guides tab were written with the Spectral Micro; the code in them runs unchanged on STEPFOC.
