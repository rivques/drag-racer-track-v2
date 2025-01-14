# drag-racer-track-v2
A new and improved version of [mini-drag-racetrack](https://github.com/rivques/mini-drag-racetrack).

## How To Use
To be written.

## Bill Of Materials
* 2x [Adafruit beam-break 3mm sensors](https://www.adafruit.com/product/2167)

## Project Proposal
Available at [this Google doc](https://docs.google.com/document/d/1fPM3jAb2btpLcQTNEUYPZXAGJ7guPSih1aArkj4l1_s/edit?usp=sharing).

## Circuit Diagram
### Commmunication
The three modules communicate over straight-through CAT-5 (aka Ethernet) cable. This is a convenient, flexible multi-conductor cable. The pinout is as follows (assuming T568A terminations)
#### Main-Motor (purpose and direction from Main's perspective):
RJ-45 Pin # | T568A color | Purpose | Direction | Notes
---|---|---|---|---
1|Wh/Gr|GND|Bidirectional|Shared ground reference
2|Gr|TX|OUTPUT|
3|Wh/Or|GND(sense)|INPUT|Bridged to GND by Motor
4|Bl|NC||
5|Wh/Bl|NC||
6|Or|RX|INPUT|
7|Wh/Br|NC||
8|Br|NC||

#### Main-Controller (purpose and direction from Main's perspective):
RJ-45 Pin # | T568A color | Purpose | Direction | Notes
---|---|---|---|---
1|Wh/Gr|GND|OUTPUT|
2|Gr|NC||
3|Wh/Or|3V3(sense)|INPUT|Bridged to 3V3 by Controller
4|Bl|RESET|INPUT|
5|Wh/Bl|3V3|OUTPUT|Power supply for controller
6|Or|NC||
7|Wh/Br|ARM|INPUT|
8|Br|RACE|INPUT|

To be created.


## 