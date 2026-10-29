# The serial terminal

Motor GUI is the usual way to work with the driver; a plain serial terminal is the alternative, and it is what
the console inside Motor GUI is. Everything in this manual that is done in the GUI is also one `#` command, and
the terminal shows the driver's answers exactly as it prints them, which is useful when something does not work.

The driver talks on its UART connector at 256000 baud, 8N1, 3.3 V. Any terminal that sends a line ending in
CR+LF works.

<figure markdown="span">
  ![The UART connector and the adapter](../assets/UART connection.PNG){ width="700" }
  <figcaption>Figure 12: The UART connector. TX of the driver goes to RX of the adapter and RX to TX.</figcaption>
</figure>

## Connecting

1. Plug the [USB-to-serial adapter](https://source-robotics.com/products/usb-to-serial-adapter) into the UART
   connector with the [UART cable](https://source-robotics.com/products/uart-cable). With another adapter: 3.3 V
   only, and cross TX and RX.
2. Power the driver. The USB adapter does not power it.
3. Find the adapter's port: `COM…` on Windows, `/dev/ttyUSB…` or `/dev/ttyACM…` on Linux and macOS.

!!! danger
    5 V on the UART pins destroys the board.

## A terminal

=== "PuTTY"
    PuTTY needs to send CR+LF when you press Enter, which the stock build cannot. Use the
    [modified PuTTY](https://www.grzegorz.net/pliki/putty-crlf.zip): under *Terminal → Keyboard* select the CR LF
    option, then open the serial port at 256000.

    | Keyboard setting | Session |
    |---|---|
    | ![PuTTY keyboard tab](../assets/PUTTY2.PNG){ width="420" } | ![PuTTY session](../assets/PUTTY1.PNG){ width="420" } |

=== "VS Code (PlatformIO)"
    With the [firmware project](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller/tree/Bootloader_main/Spectral%20BLDC%20Firmware)
    open in VS Code with the PlatformIO extension, the serial monitor (the plug icon in the status bar) uses the
    speed and the `send_on_enter` filter from `platformio.ini`, so a line goes out with CR+LF when you press
    Enter.

    | platformio.ini | The monitor |
    |---|---|
    | ![platformio.ini](../assets/vscode1.PNG){ width="420" } | ![The serial monitor](../assets/vscode2.PNG){ width="420" } |

=== "Arduino IDE"
    Select the adapter's port under *Tools*, any board (the monitor does not care), open the serial monitor, set
    256000 baud and *Both NL & CR* as the line ending.

    ![Arduino serial monitor](../assets/Arduino3.PNG){ width="420" }

## The first commands

```
#Info
```

prints the driver's identity: the hardware and firmware version, the serial number, the motor parameters and the
calibration state. `#Help` (firmware 106 and newer) prints a short command reference, `#Error` the active errors.

Every command starts with `#`, and a Set/Get command takes one number after a space: `#P 16384` moves to position
16384; `#P` alone prints the position. Names are case-sensitive. The whole set is in the
[UART commands](../reference/uart/index.md) reference, and [Over UART](../06-operation/uart.md) explains the
protocol.
