# Dimensions and CAD

The board is 39 × 39 mm with four mounting holes on the NEMA 17 pattern (31 mm apart). The encoder chip is
exactly in the middle of the board, so a bracket that centres the board on the motor shaft puts the chip on the
shaft's axis.

<div class="gripper-viewer" data-base="../../assets/models/spectral/" markdown="0">
  <canvas class="gripper-viewer__canvas" aria-label="The Spectral Micro driver in 3D: drag to turn, scroll to zoom"></canvas>
  <div class="gripper-viewer__controls">
    <button type="button" name="reset" class="md-button">Reset view</button>
  </div>
  <p class="gripper-viewer__hint">Drag to turn the board, scroll to zoom. The model is the board's STEP file from the <a href="https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files">repository</a>, the PCB and everything mounted on it.</p>
</div>

![Board dimensions and hole pattern.](../assets/micro_dimensions.webp#only-light){ width="600" }
![Board dimensions and hole pattern.](../assets/micro_dimensions_dark.webp#only-dark){ width="600" }

![The board's model, from its STEP file: the PCB and everything mounted on it.](../assets/renders/spectral_board_studio.webp#only-light){ width="520" }
![The board's model, from its STEP file: the PCB and everything mounted on it.](../assets/renders/spectral_board_studio_dark.webp#only-dark){ width="520" }

The STEP files of the board and of an example mounting bracket are in the firmware repository, in
[STEP files](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files):
`Spectral_micro_STEP.STEP` is the board, `Spectral_micro_bracket.STEP` the bracket to adapt to your motor
([Mounting on the motor](../04-mounting/mounting.md)).

[Downloads and files](../cad-files.md) lists everything that can be downloaded.
