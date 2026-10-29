# Flashing firmware

!!! note "Firmware 101 and the bootloader"
    Firmware 101, like every release on the firmware repository's `main` branch, is flashed with a programming adapter as
    described here. Releases from 105 on run above a bootloader and update over UART or CAN; the current version of this
    site (the version selector in the header) describes that.

!!! note "You can check what is the latest firmware release in the github page of Spectral micro! To check what software release is on your driver use command #Info"

!!! tip "Note"
    When flashing new firmware make sure you disconnect power connection and uart connection.

<iframe width="560" height="315" src="https://www.youtube.com/embed/fcvL_6R1Je4?si=I4g3wQzkeJV9rXRw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

| | Needed hardware |
|---|---|
| You can change all variables using UART and CAN so flashing firmware a lot is not necessary<br /> You will usually flash it when:<br />  1. New version of Spectral BLDC firmware is available <br />2. You are doing custom code development <br /> 3. You are using SimpleFOC firmware | You will need programming adapter from [here!](https://source-robotics.com/products/jtag-programming-adapter-1-27-pitch?variant=47293352903004) <p align="left"> <img src="../assets/ADAPTER-Photoroom.png" alt="ADAPTER" width="600"/> <br /> </p>
    
## Connecting to PCB

=== "Using [Adapter](https://source-robotics.com/products/jtag-programming-adapter-1-27-pitch?variant=47293352903004) "

    Step 1 | Step 2
    ---- | ---- 
    Locate JTAG PINS | Press programming adapter like shown in the picture (apply small amount of pressure on the pins to get a good contact)
    <p align="left"> <img src="../assets/JTAG_PINS.png" alt="JTAG PINS" width="750"/> <br /> </p> | <p align="left"> <img src="../assets/FLASHING2-Photoroom.png" alt="FLASHING2" width="500"/> <br /> </p> 

## Flashing using visual studio code
Download [Visual Studio Code](https://code.visualstudio.com/download).<br />

1. Open [Spectral BLDC firmware](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/Spectral%20BLDC%20Firmware) folder in VS code. (You need to have platformio installed)
2. Press upload in VS code (Bottom left corner in VS code)
<p align="left"> <img src="../assets/VSUPLOAD.png" alt="VSUPLOAD" width="800"/> <br /> </p>

## Flashing using STM32 ST-LINK Utility
Download the [STM32 ST-LINK utility](https://www.st.com/en/development-tools/stsw-link004.html).

!!! note "HEX and binaries"
    Using STM32 ST-LINK Utility you can flash only Binary or HEX files. These can be obtained from compiling source code of spectral BLDC firmware

**Open STM32 ST-LINK utility Drag and drop the [binary file](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/Binaries) inside.**

<p align="left"> <img src="../assets/stlink2.PNG" alt="stlink2" width="700"/> <br /> </p>

**Go to Target/settings and make sure they look like this.**

<p align="left"> <img src="../assets/stlink1.PNG" alt="stlink1" width="700"/> <br /> </p>

**Go to Target/connect. In case you get an error try to install stlink drivers from [here!](https://www.st.com/en/development-tools/stsw-link009.html)**

<p align="left"> <img src="../assets/stlink_conn.png" alt="stlink conn" width="700"/> <br /> </p>

**Go to Target/program and verify. You should get pink output msg like below.**

<p align="left"> <img src="../assets/stlink_prog.png" alt="stlink prog" width="700"/> <br /> </p>
