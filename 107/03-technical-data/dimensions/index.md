# Dimensions and CAD

The board is 39 × 39 mm with four mounting holes on the NEMA 17 pattern (31 mm apart). The encoder chip is
exactly in the middle of the board, so a bracket that centres the board on the motor shaft puts the chip on the
shaft's axis.

<div class="gripper-viewer" data-base="../../assets/models/spectral/" markdown="0">
  <canvas class="gripper-viewer__canvas" aria-label="The Spectral Micro driver in 3D: drag to turn, scroll to zoom"></canvas>
  <div class="gripper-viewer__controls">
    <button type="button" name="reset" class="md-button">Reset view</button>
  </div>
  <p class="gripper-viewer__hint">Drag to turn the board, scroll to zoom. The model is the board's STEP file from the <a href="https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller">repository</a>, the PCB and everything mounted on it.</p>
</div>

<figure markdown="span">
  ![Dimensions of the board](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/micro_dimensions.webp){ width="600" }
  <figcaption>Figure 4: Board dimensions and hole pattern.</figcaption>
</figure>

<figure markdown="span">
  ![The STEP model of the driver](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/bldc_step.webp){ width="520" }
  <figcaption>Figure 5: The STEP model.</figcaption>
</figure>

The STEP files of the board and of an example mounting bracket are in the firmware repository, in
[STEP files](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files):
`Spectral_micro_STEP.STEP` is the board, `Spectral_micro_bracket.STEP` the bracket to adapt to your motor
([Mounting on the motor](https://docs.source-robotics.com/Spectral-BLDC-docs/107/04-mounting/mounting/)).

[CAD and downloads](https://docs.source-robotics.com/Spectral-BLDC-docs/107/cad-files/) lists everything that can be downloaded.
