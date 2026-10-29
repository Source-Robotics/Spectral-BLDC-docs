---
hide:
  - toc
---

# Spectral Micro Manual

![Spectral Micro driver](assets/spectral-Photoroom.webp){ .hero }

<!-- doc-meta: spectral -->

[Quick start](quick-start.md){ .md-button .md-button--primary } [About this manual](about.md){ .md-button }

Source Robotics d.o.o. publishes this document for the Spectral Micro BLDC driver. It is revised as the product and
its firmware change; the document number, firmware version, revision and date above identify the version you are
reading, and the document history on the About page says what changed. Take care that the firmware version named
under *Applies to* matches what `#Info` reports on your driver: the version selector in the header switches
between firmware releases. The text and the images are licensed CC BY-SA 4.0, the code examples MIT.

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick start**

    ---

    [One page](quick-start.md) from the box to a calibrated motor that follows commands, through Motor GUI or the
    terminal, with a link into the manual at every step.

-   :material-book-open-variant:{ .lg .middle } **The manual**

    ---

    [Safety](02-safety.md), [Technical data](03-technical-data/index.md), [Mounting and wiring](04-mounting/index.md),
    [First setup](05-setup/index.md), [Operation](06-operation/index.md), [Firmware](07-firmware/index.md),
    [Troubleshooting](08-troubleshooting.md).

-   :material-monitor-dashboard:{ .lg .middle } **Motor GUI**

    ---

    The usual way to set up and test: [the tool](05-setup/motor-gui.md) and [working in it](06-operation/motor-gui.md)
    — connect, calibrate, tune with live plots, record telemetry, update the firmware.

-   :material-code-braces:{ .lg .middle } **API reference**

    ---

    Every [CAN message](reference/can/index.md) and [UART command](reference/uart/index.md), the
    [defaults](reference/defaults.md), the [errors](reference/errors.md) and the [Python library](reference/python.md),
    read from the firmware.

-   :material-school:{ .lg .middle } **Learn**

    ---

    [Guides](guides/index.md) with code, from a mobile robot to a quadruped leg, the
    [bootloader](07-firmware/the-bootloader.md), and the [theory corner](appendix/theory.md) on FOC, the cascade and
    impedance control.

</div>
