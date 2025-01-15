# drag-racer-track-v2
A new and improved version of [mini-drag-racetrack](https://github.com/rivques/mini-drag-racetrack).

## How To Use
To be written.

## Bill Of Materials
* 2x [Adafruit beam-break 3mm sensors](https://www.adafruit.com/product/2167)
* 4x [SparkFun RJ45 breakouts](https://www.sparkfun.com/sparkfun-rj45-breakout.html) with [SparkFun RJ45 conectors](https://www.sparkfun.com/rj45-8-pin-connector.html)
## Project Proposal
Available at [this Google doc](https://docs.google.com/document/d/1fPM3jAb2btpLcQTNEUYPZXAGJ7guPSih1aArkj4l1_s/edit?usp=sharing).

## Circuit Diagram
### Commmunication
The three modules communicate over straight-through CAT-5 (aka Ethernet) cable. This is a convenient, flexible multi-conductor cable. 

This pinout is constructed to allow near-unambiguous determination by the main processor of 1. if a cable is connected and 2. if the cable is connected to the motors or the screen.
To do this it can do the following:
```mermaid
flowchart TD
    Start-->
    Watch7{Watch pin 7}
    -->|High|Nothing([Nothing Connected])-->
    Watch7
    -->|Low|Something[Something Connected]
    -->Set5[Set 5 HIGH]
    -->Watch3{Check Pin 3}
    -->|High|Controller([Connected to Controller])
    Watch3-->|Low|Motor([Connected to Motor])
```
This approach does fail if the smart controller is plugged in while the reset button is pressed. However, it should catch most crossed wires.

The pinout is as follows (assuming T568A terminations):
#### Main-Motor (purpose and direction from Main's perspective):
RJ-45 Pin # | T568A color | Pico pin | Purpose | Direction | Notes
---|---|---|---|---|---
1|Wh/Gr|GND|GND|Bidirectional|Shared ground reference
2|Gr|GP0|TX|OUTPUT|UART 8N1@9600 baud
3|Wh/Or|GP2|Discrim|INPUT|Tied to GND at Motor
4|Bl|NC|NC||
5|Wh/Bl|3V3OUT|3V3|OUTPUT|
6|Or|GP1|RX|INPUT|UART 8N1@9600 baud
7|Wh/Br|GP3|Presence|INPUT|Tied to GND at Motor
8|Br|NC|NC||

#### Main-Button Controller (purpose and direction from Main's perspective):
RJ-45 Pin # | T568A color | Pico pin | Purpose | Direction | Notes
---|---|---|---|---|---
1|Wh/Gr|GND|GND|OUTPUT|
2|Gr|GP17|LED_RACE|OUTPUT|
3|Wh/Or|GP8|Discrim|INPUT|Tied to LED_RACE at Controller
4|Bl|GP4|RESET|INPUT|
5|Wh/Bl|GP16|LED_ARM|OUTPUT|
6|Or|GP5|ARM|INPUT|
7|Wh/Br|GP7|Presence|INPUT|Tied to GND at Controller
8|Br|GP6|RACE|INPUT|

To be created.

## 