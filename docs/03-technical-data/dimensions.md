# Dimensions and CAD

The board is 39 × 39 mm with four mounting holes on the NEMA 17 pattern (31 mm apart). The encoder chip is
exactly in the middle of the board, so a bracket that centres the board on the motor shaft puts the chip on the
shaft's axis.

<figure markdown="span">
  ![Dimensions of the board](../assets/micro_dimensions.PNG){ width="600" }
  <figcaption>Figure 4: Board dimensions and hole pattern.</figcaption>
</figure>

<figure markdown="span">
  ![The STEP model of the driver](../assets/bldc_step.PNG){ width="520" }
  <figcaption>Figure 5: The STEP model.</figcaption>
</figure>

The STEP files of the board and of an example mounting bracket are in the firmware repository, in
[STEP files](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files):
`Spectral_micro_STEP.STEP` is the board, `Spectral_micro_bracket.STEP` the bracket to adapt to your motor
([Mounting on the motor](../04-mounting/mounting.md)).

[CAD and downloads](../cad-files.md) lists everything that can be downloaded.
