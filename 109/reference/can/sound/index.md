# Sound

Sound through the motor: tones, a queue of timed events and samples, added to the output voltage while the
driver holds or moves. [Sound](https://docs.source-robotics.com/Spectral-BLDC-docs/109/06-operation/sound/) explains how to use them; parameters 80 to 82 are in the
[parameter table](https://docs.source-robotics.com/Spectral-BLDC-docs/109/reference/can/parameters/#sound).

### Send_Sound

<div class="cmd-facts" markdown><span class="fact">ID 44</span><span class="fact">host → driver</span><span class="fact">8 bytes</span><span class="fact">Python: `Send_Sound()`</span></div>

Plays sound through the motor: a tone now, a queue of timed events, or samples. The sound is added to the output voltage, on the q axis by default (parameter 82), and only while the driver holds or moves (position, velocity, current or PD mode); idle or an error stops all of it. Up to 4 tones sound at once (channels 0 to 3), from 20 Hz to below 2500 Hz, half the control-loop rate. Loudness is given as a current: the driver turns it into a voltage with the coil's impedance at that pitch, so low and high notes sound alike. The total voltage is limited to parameter 81 (2000 mV by default; 0 refuses sound). Added in firmware 109. The driver does not answer; parameter 80 says what plays. The Python library wraps the operations as Send_Tone, Send_Sound_Stop, Send_Sound_Event, Send_Sound_Play, Send_Sound_Clear, Send_Samples_Play and Send_Samples_Stop.

**8 bytes**

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | Operation | unsigned 8-bit | 0 stop everything (tones, queue, samples); 1 a tone now; 2 add an event to the queue; 3 play the queue; 4 play the samples; 5 samples off, buffer cleared; 6 clear the queue (tones that sound keep sounding) |
| 1 |  | Channel | unsigned 8-bit | the tone channel, 0-3 (operations 1 and 2) |
| 2-3 |  | A | unsigned 16-bit | 1, 2: the pitch in Hz (2: 0 silences the channel); 4: the sample rate in Hz, at most the loop rate |
| 4-5 |  | B | unsigned 16-bit | 1, 2: the loudness in mA; 4: the voltage of a full-scale sample in mV |
| 6-7 |  | C | unsigned 16-bit | 1: the duration in ms, 0 = until stopped; 2: the wait in ms before the next event, 0 = the next one starts with it |

The driver does not answer this command.

The queue holds 31 events and is played by the control loop with loop-exact timing: an event sets one channel's pitch and loudness, then waits. A chord is three events with wait 0 and a fourth with the chord's length. When the queue runs out, every channel falls silent. An event sent to a full queue is dropped. Samples: send them first with Send_Sound_Samples, then operation 4; the driver plays them at the given rate and stops when the buffer runs dry. A frame of another length, or a remote frame, is ignored. It does not reset the watchdog.

---

### Send_Sound_Samples

<div class="cmd-facts" markdown><span class="fact">ID 45</span><span class="fact">host → driver</span><span class="fact">1 to 8 bytes</span><span class="fact">Python: `Send_Samples()`</span></div>

Appends 1 to 8 samples (signed 8-bit, one per byte, −127 to 127 = full scale) to the driver's 1024-place sample buffer, which holds 1023 samples. Samples that do not fit are dropped; parameter 80 says how many are buffered. Send_Sound with operation 4 plays them. Added in firmware 109. The driver does not answer.

**8 bytes** — eight samples; a shorter frame carries fewer

| Byte | Bit | Field | Type | Meaning |
|---|---|---|---|---|
| 0 |  | Sample 1 | signed 8-bit | the next sample |
| 1 |  | Sample 2 | signed 8-bit |  |
| 2 |  | Sample 3 | signed 8-bit |  |
| 3 |  | Sample 4 | signed 8-bit |  |
| 4 |  | Sample 5 | signed 8-bit |  |
| 5 |  | Sample 6 | signed 8-bit |  |
| 6 |  | Sample 7 | signed 8-bit |  |
| 7 |  | Sample 8 | signed 8-bit |  |

The driver does not answer this command.

---
