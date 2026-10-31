# Tested motors

The Spectral Micro drives three-phase brushless motors with a phase resistance of about 2 to 24 Ω: the
calibration routine's default voltages are made for that range. The motors below have been run on it. Calibration
measures each motor's resistance, inductance and pole pairs, so nothing has to be looked up before the first run.

| | Motor | Kind | Where |
|---|---|---|---|
| ![BGM8108](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/BGM8108.webp){ width="90" } | BGM8108 | gimbal motor, 8108 class | [AliExpress](https://es.aliexpress.com/item/2008157492.html) |
| ![GM8112](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GM8112.webp){ width="90" } | GM8112 | gimbal motor, 8112 class | [AliExpress](https://s.click.aliexpress.com/e/_Dc6I1bx) |
| ![GM7008H](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GM7008H.webp){ width="90" } | GM7008H | gimbal motor, 7008 class | [AliExpress](https://s.click.aliexpress.com/e/_DBY6U9T) |
| ![GM6008H](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GM6008H.webp){ width="90" } | GM6008H | gimbal motor, 6008 class | [AliExpress](https://s.click.aliexpress.com/e/_DDPsXZn) |
| ![GBM5208](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GBM5208.webp){ width="90" } | GBM5208 | gimbal motor, 5208 class | [AliExpress](https://s.click.aliexpress.com/e/_okWNA7Z) |
| ![GM5208](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GM5208.webp){ width="90" } | GM5208 | gimbal motor, 5208 class | [AliExpress](https://s.click.aliexpress.com/e/_Dd82dTF) |
| ![GBM5010](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GBM5010.webp){ width="90" } | GBM5010 | gimbal motor, 5010 class | [AliExpress](https://s.click.aliexpress.com/e/_DlJ8vJb) |
| ![GB4114](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/GB4114.webp){ width="90" } | GB4114 | gimbal motor, 4114 class | [AliExpress](https://s.click.aliexpress.com/e/_DDVlOFR) |
| ![2804](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/2804_motor.webp){ width="90" } | 2804 | gimbal motor, 2804 class | [AliExpress](https://s.click.aliexpress.com/e/_DlEUo81) |
| ![2804 (RCTimer)](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/RCTIMER.webp){ width="90" } | 2804 (RCTimer) | gimbal motor, 2804 class | [AliExpress](https://s.click.aliexpress.com/e/_DlQJp3T) |
| ![2804 100KV](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/2804_100kv.webp){ width="90" } | 2804 100KV | gimbal motor, 2804 class, 100 KV | [AliExpress](https://s.click.aliexpress.com/e/_DdeNXK1) |
| ![42BLS40-24-01](https://docs.source-robotics.com/Spectral-BLDC-docs/107/assets/NEMA17%20format%20BLDC.webp){ width="90" } | 42BLS40-24-01 | NEMA 17-format brushless motor, 24 V, 26 W, 1.8 A, 219 g | [Stepperonline](https://www.omc-stepperonline.com/24v-4000rpm-0-0625nm-26w-1-8a-42x42x40mm-brushless-dc-motor-42bls40-24-01) |

Before the first test, set the current limit for the motor with `#Ilim`: the firmware's default of 1000 mA suits
the gimbal motors above; a motor rated for more can go up to the driver's 2800 mA. See
[Current limit and loop tuning](https://docs.source-robotics.com/Spectral-BLDC-docs/107/05-setup/tuning/).

!!! tip "Choosing a motor"
    A lower phase resistance and inductance give a higher speed at a given supply voltage; the velocity constant
    `KV` that calibration finds tells how fast the motor can turn: roughly 0.8 × Vbus × KV revolutions per minute.
    A high pole-pair count (the large gimbal motors have 11 to 14) gives smooth torque at low speed and limits the
    top speed through the driver's maximum electrical frequency. Motors with visibly uneven windings, a resistance
    that differs between the phases or an uneven back-EMF calibrate badly and run rough.

!!! danger "Drone motors"
    Motors with a phase resistance well under 1 Ω draw a destructive current at the calibration routine's default
    voltages. The Spectral Micro is not made for them.
