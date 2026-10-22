# Getting started

## **Spectral Micro BLDC driver** 

You can buy a Spectral Micro starter kit here: [Link](https://source-robotics.com/products/spectral-micro-bldc-starter-kit) <br />
Or buy a single motor driver here: [Link](https://source-robotics.com/products/spectral-micro-bldc-controller)  

## **Recommended hardware**

1. [Diametrically magnetized magnet](https://source-robotics.com/products/6x2-5mm-diametrical-neodymium-magnet)
2. BLDC motor; check [here](apage9_3_tested_motors.md) for all tested motors
3. [Programming adapter](https://source-robotics.com/products/jtag-programming-adapter-1-27-pitch)
4. [Serial adapter](https://source-robotics.com/products/usb-to-serial-adapter)
5. [CAN adapter](https://source-robotics.com/products/canvas-usb-to-can-adapter) 
6. [Termistor](https://source-robotics.com/products/100k-ntc-thermistor)
7. [CAN wires](https://source-robotics.com/products/spectral-micro-can-cable) and [power wires](https://source-robotics.com/products/spectral-micro-power-cable)

!!! Note annotate "" 

## **Hardware setup**

### **Mounting PCB to Motor**

To mount your BLDC to PCB you can use [example motor bracket](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/STEP%20files) and modify it for your motor.<br />
<p align="left"> <img src="../assets/brack.PNG" alt="drawing" width="500"/> <br /> </p>

Some hardware considerations:

* Distance between motor encoder and magnet should be around 1 mm.
* Hole spacing of Spectral micro is 31 mm

<p align="left"> <img src="../assets/mag_dist.png" alt="drawing" width="800"/> <br /> </p>

!!! Note annotate "" 

## **Electrical connections**
!!! Danger annotate "REVERSING POLARITIY ON DC+- WILL DESTROY YOUR BOARD." 

<p align="left"> <img src="../assets/con2.png" alt="drawing" width="800"/> <br /> </p>

1. Solder motor phases to **U,W,V**
2. Connect motor power to one of the **Power connectors** terminals
3. If you are using UART comms. Connect Uart adapter to **UART connector**
4. If you are using termistor, connect it to **Termistor connecor**
5. If you are using CAN comms. Connect CAN adapter to one of **CAN connectors**
6. When uploading code connect JTAG adapter to **JTAG connector**


!!! Danger annotate "**Cable orientation**" 
    **ALL cables used for dasiy chain (CAN and power) need to to follow orientation as shown on the image below! Failing to follow that will destroy your motor controller! All correct cables can be bought here: https://source-robotics.com/pages/connectors-and-cables** <br />

<p align="left"> <img src="../assets/Orientation.png" alt="drawing" width="700"/> <br /> </p> 

!!! Note annotate "" 

## **Connecting multiple motors (daisy chaining)**

Multiple Spectral BLDC drivers and nodes can be connected to single CAN bus using daisy-chaining. First an last nodes on can bus should have termination resistors. On Spectral micro you can flip the CAN switch to "ON" positon to enable termination resistor.

!!! Tip annotate "Power connectors can handle max 4 A DC. Usually if you are using 10ohm gimbal motor you can daisy chain 3-4 of them." 


<p align="left"> <img src="../assets/Daisy_chain-Photoroom.png" alt="drawing" width="700"/> <br /> </p> 

!!! Note annotate "" 

## **Thermistor connection**

Solder the termistor like shown in the image. 
!!! Tip annotate "Thermistor is disabled by default. To enable it use command #Term 1" 

<p align="left"> <img src="../assets/TERM1-Photoroom.png" alt="drawing" width="600"/> <br /> </p> 

Thermistor needs to be placed inside the motor coils. You can usually do that thru the one of the mounting holes on the bottom of the motor. You can apply thermal cement on the thermistor in the motor coils to secure it in place and improve termal conductivity.

<p align="left"> <img src="../assets/TERM2-Photoroom.png" alt="drawing" width="600"/> <br /> </p> 

!!! Note annotate "" 

## **Status**

Normal operation | Calibration | Error mode 
---- | ---- | ----
3 short flashed and a pause <p align="left"> <img src="../assets/Normal.gif" alt="drawing" width="180"/> <br /> </p> | Flashing every 0.5 seconds <p align="left"> <img src="../assets/Calib.gif" alt="drawing" width="180"/> <br /> </p> | Solid LED, no flashing. <p align="left"> <img src="../assets/Error2.PNG" alt="drawing" width="180"/> <br /> </p>

If you have [spectral firmware](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/Spectral%20BLDC%20Firmware) uploaded on your spectral BLDC LEDs will be in one of 3 states.

* **Normal operation** is when motor controller has no active errors and is calibrated
* **Error mode** is active if any error on the motor driver is active. List of possible errors:
    1. Temperature error
    2. Drv error
    3. Encoder error
    4. Vbus error
    5. Velocity error
    6. Current error
    7. Not calibrated 
    8. Received ESTOP
    9. Watchdog error
* **Calibration** will flash when in calibration routine

## **What next?**

* Flash the [latest firmware](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/main/Spectral%20BLDC%20Firmware) to your driver (Note that drivers arrive with preflashed firmware)
* You will need to [calibrate your motor](apage4_calibration.md)
* [Tune your PID loops](apage5_PID_tuning.md)
* Follow one of the guides or examples to start using Spectral driver
