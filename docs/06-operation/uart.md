# Over UART

The serial port is the interactive way to use the driver: you type a command, the driver answers in text. It is
the only way to calibrate, and the quickest way to try a setting. For real-time control of several motors use CAN.

## The protocol

A command is `#`, a name, optionally a space and one number, and a line ending:

```
#P 16384
#P
#Cal
```

- The name is case-sensitive and matches the firmware's spelling exactly (`#Kpiq`, not `#kpiq`); at most 19
  characters, the number at most 19 characters, both together at most 20.
- The line ends with LF (`\n`); a CR before it is accepted. Terminals send CR+LF when you press Enter, with the
  setting described in [The serial terminal](../05-setup/terminal.md).
- A **Set/Get** command with a number sets the value and prints it; without a number it only prints it. `#P 16384`
  moves to position 16384 and prints the position; `#P` prints the position.
- An **action** command takes no number: `#Cal`, `#Save`, `#Idle`.
- A command the parser does not know is answered with `Unknown command`. A few names the parser
  accepts have no handler and are answered with nothing; the [UART reference](../reference/uart/index.md) lists them.
- 256000 baud, 8N1, 3.3 V.

## The driver only answers

The driver never sends anything on its own, except with the cyclic commands: `#Cyc 100` makes it print position,
speed and Iq every 100 ms as `$ <position> <speed> <Iq>` (for BetterSerialPlotter), `#Cyca 100` as
`Position:x,Speed:y,Iq:z` (for the Arduino plotter); `#Cyc` or `#Cyca` without a number stops it.

## Typical sessions

A first test after calibration:

```
#Ilim 1500        current limit for the motor
#V 16384          one revolution per second
#V 0
#P 0              back to the start
#Idle
```

Tuning:

```
#Kpv 0.02
#Kiv 0.001
#V 30000
#Save
```

Status:

```
#Info
#Error
#Temp
#Vbus
```

Every command is in the [UART reference](../reference/uart/index.md), grouped by what it does.
