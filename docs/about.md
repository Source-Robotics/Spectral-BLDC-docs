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

Read the Safety chapter before you power anything. The [Quick start](quick-start.md) is the whole first setup on
one page; the chapters are in the order you need them and go deeper.

## Finding your way

--8<-- "navigation.md"

## Warnings and notes

Three kinds of highlighted text appear in this documentation. Read every Danger and Notice before you act on the
step it belongs to.

--8<-- "symbols.md"

## Related documents

<!-- documents-table -->

The STEPFOC stepper driver is built on the Spectral Micro's hardware and firmware; its documentation is at
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
