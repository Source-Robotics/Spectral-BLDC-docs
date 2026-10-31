# Spectral Micro Manual

![Spectral Micro driver](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/spectral-Photoroom.webp)

<div class="doc-meta" markdown>

**Document number:** SR-5002

**Firmware version:** 107

**Revision:** 2026.A (draft)

**Published:** —

**Applies to:** Spectral Micro driver PCB v2.0, firmware 107

*Original instructions*

</div>

[Quick start](https://docs.source-robotics.com/Spectral-BLDC-docs/107/quick-start/) [About this manual](https://docs.source-robotics.com/Spectral-BLDC-docs/107/about/)

Source Robotics d.o.o. publishes this document for the Spectral Micro BLDC driver. It is revised as the product and
its firmware change; the document number, firmware version, revision and date above identify the version you are
reading, and the document history on the About page says what changed. Take care that the firmware version named
under *Applies to* matches what `#Info` reports on your driver: the version selector in the header switches
between firmware releases. The text and the images are licensed CC BY-SA 4.0, the code examples MIT.

<div class="gripper-viewer" data-base="assets/models/spectral/" markdown="0">
  <canvas class="gripper-viewer__canvas" aria-label="The Spectral Micro driver in 3D: drag to turn, scroll to zoom"></canvas>
  <div class="gripper-viewer__controls">
    <button type="button" name="reset" class="md-button">Reset view</button>
  </div>
  <p class="gripper-viewer__hint">Drag to turn the board, scroll to zoom. The model is the board's STEP file from the <a href="https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller">repository</a>, the PCB and everything mounted on it.</p>
</div>

<div class="grid cards" markdown>

-   :material-rocket-launch: **Quick start**

    ---

    [One page](https://docs.source-robotics.com/Spectral-BLDC-docs/107/quick-start/) from the box to a calibrated motor that follows commands, through Motor GUI or the
    terminal, with a link into the manual at every step.

-   :material-book-open-variant: **The manual**

    ---

    [Safety](https://docs.source-robotics.com/Spectral-BLDC-docs/107/02-safety/), [Technical data](https://docs.source-robotics.com/Spectral-BLDC-docs/107/03-technical-data/), [Mounting and wiring](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/),
    [First setup](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/), [Operation](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/), [Firmware](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/),
    [Troubleshooting](https://docs.source-robotics.com/Spectral-BLDC-docs/107/08-troubleshooting/).

-   :material-monitor-dashboard: **Motor GUI**

    ---

    The usual way to set up and test: [the tool](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/motor-gui/) and [working in it](https://docs.source-robotics.com/Spectral-BLDC-docs/107/06-operation/motor-gui/)
    — connect, calibrate, tune with live plots, record telemetry, update the firmware.

-   :material-code-braces: **API reference**

    ---

    Every [CAN message](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/can/) and [UART command](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/uart/), the
    [defaults](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/defaults/), the [errors](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/errors/) and the [Python library](https://docs.source-robotics.com/Spectral-BLDC-docs/107/reference/python/),
    read from the firmware.

-   :material-school: **Learn**

    ---

    [Guides](https://docs.source-robotics.com/Spectral-BLDC-docs/107/guides/) with code, from a mobile robot to a quadruped leg, the
    [bootloader](https://docs.source-robotics.com/Spectral-BLDC-docs/107/07-firmware/the-bootloader/), and the [theory corner](https://docs.source-robotics.com/Spectral-BLDC-docs/107/appendix/theory/) on FOC, the cascade and
    impedance control.

</div>
