# About this manual

## Scope and audience

The Spectral Micro Manual covers the Spectral Micro BLDC driver from unpacking to a tuned motor on a CAN bus: what
the driver is, how to mount it on a motor and wire it, the first setup with Motor GUI or the serial terminal,
calibration and tuning, how the driver is controlled over UART and CAN or from Python, and how its firmware is
updated. The API reference lists every CAN message and UART command of the firmware release named on the landing
page. The Guides are worked examples.

It is written for someone who builds a robot or a machine with the Spectral Micro: a maker, a student or an
engineer who can solder three motor wires and open a serial terminal. It does not assume any knowledge of
field-oriented control; the Theory corner in the appendix explains the concepts the control modes rely on.

Read the Safety chapter before you power anything. The [Quick start](https://docs.source-robotics.com/Spectral-BLDC-docs/107/quick-start/) is the whole first setup on
one page; the chapters are in the order you need them and go deeper.

## Finding your way

The header has four tabs. **Spectral Micro Manual** is the document you read from the start: the quick start, then
safety, technical data, mounting, the first setup, operation and firmware updates, in numbered chapters. Motor
GUI, the tool in the browser, is the usual way to do what the chapters describe; each procedure shows it first
and the terminal command beside it. **API reference** lists every CAN message, every UART command and the Python
library's calls for the firmware release this site describes, with the defaults and the error flags, and is where
you look things up. **Guides** are worked examples with code. **Support** says where to get help and how to report
a problem.

The whole site describes one firmware release. The dropdown next to the site name switches between releases, and a
page from an older release says so in a bar at the top. The repository card on the right of the header opens the
firmware repository; every page ends with a link to edit it and one to report a problem with it.
## Warnings and notes

Three kinds of highlighted text appear in this documentation. Read every Danger and Notice before you act on the
step it belongs to.

!!! note "Note"
    Points out something that is easy to miss or that changes what follows: a default, a limit, a side effect.

!!! warning "Notice"
    The robot, the tool, or data on the control box can be damaged or lost if this is ignored. Nobody is at risk.

!!! danger "Danger"
    Someone can be injured if this is ignored. Stop and read the whole box before acting on the step it belongs to.
## Related documents

| Document | Number | Covers |
|---|---|---|
| Spectral Micro Manual | SR-5002 | the Spectral Micro BLDC driver: quick start, safety, technical data, mounting, setup with Motor GUI or a terminal, operation, firmware; the API reference; guides |

A document marked with a firmware version describes that firmware release, here 107; the version selector in the header switches between releases. The compatibility table says which firmware, Python library and hardware revisions work together.

The STEPFOC stepper driver has similar hardware and firmware and is run the same way; its documentation is at
[docs.source-robotics.com/STEPFOC-docs](https://docs.source-robotics.com/STEPFOC-docs/). The SSG-48 gripper, which
is driven by a Spectral Micro, is documented at
[docs.source-robotics.com/SSG48-gripper-docs](https://docs.source-robotics.com/SSG48-gripper-docs/).

## Document history

The Spectral Micro Manual describes one firmware release; one revision is kept per release, and the version
selector in the header switches between them. The earlier version of this site, for firmware 101, is kept as
version `101`.

The text and the images of this documentation are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), the code examples under the [MIT licence](https://github.com/Source-Robotics/Spectral-BLDC-docs/blob/main/LICENSE-CODE). The Source Robotics name, the product names and the logos are not covered by either.

| Revision | Date | Changes |
|---|---|---|
| 2026.A (draft) | — | First version in this form: the manual chapters, the generated CAN and UART reference, firmware 107 |
