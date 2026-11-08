---
status: new
---

# Sound

From firmware 108 the driver plays sound through its motor: tones, chords, tunes from a queue it plays by itself,
and recorded sound such as speech. A current at an audio frequency in the windings makes a small force at that
frequency, and the motor, and above all whatever it is fixed to, radiate it as sound.

## How it works

- **Where:** the driver adds the sound to its output voltage, after the current loop. By default it goes on the q
  axis (parameter 82 = 1), where it makes torque: the rotor rocks at the tone's pitch. On the bench that was much
  louder than the d axis (82 = 0), which makes no torque at all.
- **When:** only while the driver holds or moves: position, velocity, current or PD mode. Idle, or any error,
  stops all sound. A joint keeps holding its pose while it plays.
- **Tones:** up to 4 at once (channels 0 to 3), a chord on one motor, each with its own pitch, loudness and length.
- **Loudness** is given as a current, in mA. The coil's impedance rises with the pitch (√(R² + (2πfL)²), from the
  motor's R and L), so the same voltage would sound much quieter high than low; the driver turns the current into
  the voltage that pitch needs, and a note is as loud low as high.
- **Pitch:** 20 Hz up to just below 2500 Hz, half the 5000 Hz control loop. Tones are clean up to about a third of
  the loop rate; melodies sit well between C4 and C6 (262 to 1047 Hz).
- **The queue:** 31 events, each setting one channel's pitch and loudness and then waiting. The control loop plays
  them with loop-exact timing, so the host's own timing never reaches the music: it loads the queue and starts it.
- **Samples:** recorded sound, 8 bits, played from a 1024-place buffer at a rate the host sets, up to the loop
  rate. Speech comes through recognisable but muffled: the telephone band reaches 3400 Hz, the motor 2.5 kHz.
- **The cap:** all sound together is limited to the voltage of parameter 81, 2000 mV by default; 0 refuses sound.
  On a gimbal motor's high resistance the cap comes early: 250 mA in a 7 Ω coil already takes 1.75 V. None of the
  sound settings is saved.

## A tone over UART

```
#Tone 440,250,1000      440 Hz, 250 mA, 1000 ms
#Tone 880,200,0         until stopped
#Tone off               stops all sound
```

From idle, a calibrated driver first holds the position it is at and says so (`Holding the position while it
plays (#Idle releases it)`); `#Idle` releases it afterwards. Left out, the loudness is 200 mA and the length
500 ms. `Tone: not played` means the driver is not calibrated or in an error, the pitch is outside 20 Hz to half the
loop rate, or parameter 81 is 0.

## Over CAN and from Python

Send_Sound (ID 44) carries every operation: a tone now, an event for the queue, play the queue, play the samples,
stop. Send_Sound_Samples (ID 45) fills the sample buffer ([Sound](../reference/can/sound.md) in the CAN
reference). The Python calls below come with the Spectral-BLDC library's release after 1.20, as does its `music`
module (note names, ringtone melodies, MIDI files, WAV files).

Over CAN the host makes the driver hold first, for example with a position frame to where the motor is:

```python
import Spectral_BLDC as Spectral
from Spectral_BLDC import music

comms = Spectral.CanCommunication(bustype='slcan', channel='COM41', bitrate=1000000)
motor = Spectral.SpectralCAN(node_id=0, communication=comms)


def read_answers(seconds=0.1):
    message, ids = comms.receive_can_messages(timeout=seconds)
    while message is not None:
        motor.UnpackData(message, ids)
        message, ids = comms.receive_can_messages(timeout=0.005)


motor.Send_Respond_Encoder_data()                # where the motor is
read_answers()
motor.Send_data_pack_1(motor.position, 0, 0)     # hold it there
read_answers()

motor.Send_Tone(440, current_mA=250, duration_ms=1000)        # one tone
for channel, note in enumerate(('C4', 'E4', 'G4')):            # a chord: three channels at once
    motor.Send_Tone(music.note_hz(note), current_mA=200, duration_ms=1500, channel=channel)
```

A tune goes into the queue and plays by itself. A melody becomes two events per note (the note, then a short
silence, so repeated notes are heard as two), so up to 15 notes fit at once:

```python
name, melody = music.parse_rtttl('scale:d=8,o=5,b=120:c,d,e,f,g,a,b,c6')
for channel, freq, current, wait in music.melody_events(melody, current_mA=250):
    motor.Send_Sound_Event(freq, current, wait, channel=channel)
motor.Send_Sound_Play()
```

For a longer tune, keep loading events while it plays: bits 0 to 7 of parameter 80 say how many are still
queued. `music.read_midi` reads a MIDI file, `music.split_voices` splits it into lines for the four channels, and
`music.lines_events` makes the queue's events from them.

Recorded sound: convert a WAV file to samples at the rate the motor plays, fill the buffer, start it, and keep it
filled:

```python
rate = 2500
samples = music.wav_samples('hello.wav', rate, coil_tau_s=0.00149 / 7.0, clip_percentile=0.95)
motor.Send_Samples(samples[:1000])               # fill the buffer first
motor.Send_Samples_Play(rate, full_scale_mV=2000)
sent = 1000
while sent < len(samples):
    motor.Send_Get_Parameter(80)
    read_answers(0.02)
    buffered = (motor.parameters.get(80, 0) >> 8) & 0x7FF
    room = 1000 - buffered
    if room > 0:
        motor.Send_Samples(samples[sent:sent + room])
        sent += room
```

`coil_tau_s` is the coil's L ÷ R (here 1.49 mH and 7.0 Ω, the motor of the calibration example): the function
raises the high frequencies the coil would otherwise swallow, and `clip_percentile` levels speech so that it plays
about four times louder. At 2500 samples a second a driver takes about 313 frames a second, some 4 % of the bus. When the buffer runs dry the
playing stops and bit 27 of parameter 80 says so.

Send_Sound and Send_Sound_Samples do not reset the watchdog: with a watchdog set, keep sending a status request
while the sound plays.

## Limits and care

- **Fix the motor to something that rings.** A box or a table is far louder than a motor in free air, and a loose
  motor jumps and distorts the sound. On the STEPFOC bench the motor was taped down.
- **Keep tones short and moderate.** `#Tone` and Send_Tone default to 200 mA; the bench played notes at 250 mA.
  The sound current comes on top of the holding current and heats the motor like any other current; a motor is
  made to turn, and long loud tones are hard on it.
- **On the q axis a tone is a small torque ripple:** a held joint vibrates slightly at the tone's pitch. Choose the
  d axis (parameter 82 = 0) when that matters; it is quieter.
- **The cap**, parameter 81, limits all sound together; the output also clamps at the supply voltage.

Sound has not been tested on a Spectral Micro yet; the code is the same as STEPFOC's. On the STEPFOC bench
(2026-11-08, a bare NEMA 17 taped down), tones, scales, a tune from the queue, four-note chords and streamed speech
all played. The q axis was much louder than the d axis, speech was audible but muffled, and there were no errors,
no warming and only small vibrations.

## The arm as an instrument

Every joint of a robot can play its own line, and because the sound rides on top of the control, the arm keeps
holding its pose while it plays. Load each driver's queue first, then start them one after another: the starts
are meant to fall within about a millisecond of each other, and from then on each driver keeps its own time
(whether they stay together over a whole song is still to be measured). Split a MIDI file
into as many lines as there are channels, four per driver, and give each driver its four. Through a gearbox the
sound changes with the joint; try each joint's range. Playing on an assembled arm has not been tested yet.

## Checking what plays

| Parameter | Says |
|---|---|
| 79, bit 24 | sound is playing |
| 80 | bits 0-7 events queued, 8-18 samples buffered, 24 a tone sounds, 25 the queue plays, 26 samples play, 27 the samples ran dry |
| 81 | the sound's voltage cap, mV |
| 82 | the axis: 1 q, 0 d |
