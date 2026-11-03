# Report a problem

Open an issue in the [firmware repository](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/issues)
for the driver and its firmware, or in [Spectral-BLDC-Python](https://github.com/Source-Robotics/Spectral-BLDC-Python/issues)
for the Python library. Include:

1. **The output of `#Info`, `#Error` and `#Param`**, copied from the terminal. They carry the hardware and
   firmware version, the motor parameters, the calibration state, the errors and the gains.
2. **The motor**: type, and the resistance, inductance and pole pairs calibration found (`#Info` prints them).
3. **The supply**: voltage, and whether it has a current limit.
4. **What you did and what happened**: the commands, in order, and the driver's answers; the calibration log if it
   is about calibration.
5. **How it is wired**: a photo of the board on the motor and of the cables helps more than a description.

For a problem with this documentation, the *Report it* link at the end of the page opens an issue in the
documentation repository with the page already named.
