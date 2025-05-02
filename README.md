# drag-racer-track-v2
A new and improved version of [mini-drag-racetrack](https://github.com/rivques/mini-drag-racetrack).
![A photo of the complete assembly](doc-pics/full_assembly.jpg)

## Contact Me
While this racetrack was designed to be maintainable by people other than me, please don't hesitate to contact me if you run into an issue that these docs don't cover.
You can open an issue on this repository, email me at `web (at) rivques (dot) dev`, or check [my website](https://rivques.dev) for my latest contact information.

## Troubleshooting
See [troubleshooting.md](docs/troubleshooting.md)

## How to Use
See [how_to_use.md](docs/how_to_use.md)

## Bill Of Materials
See [bill_of_materials.md](docs/bill_of_materials.md)

## Assembly From Storage
See [assembly_from_storage.md](docs/assembly_from_storage.md)

## Assembly From Scratch
See [assembly_from_scratch.md](docs/assembly_from_scratch.md)

## CAD
See [the CAD folder](cad) or [this Onshape document](https://cvilleschools.onshape.com/documents/214ca204c2fbd1332e8a9828/w/7c57c6410ddb9c7d8c5eff08/e/c34b4d3245393d7aa3c3b2bb).

## Project Proposal
Available at [this Google doc](https://docs.google.com/document/d/1fPM3jAb2btpLcQTNEUYPZXAGJ7guPSih1aArkj4l1_s/edit?usp=sharing), viewable from a CCS account.

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
3|Wh/Or|GP8|Discrim|INPUT|Tied to RESET at Controller
4|Bl|GP4|RESET|INPUT|
5|Wh/Bl|GP16|LED_ARM|OUTPUT|
6|Or|GP5|ARM|INPUT|
7|Wh/Br|GP7|Presence|INPUT|Tied to GND at Controller
8|Br|GP6|RACE|INPUT|

To be created.

### Motor Controller Board
The motor controller is build on an Adafruit Perma-Proto Mini Bonnet. That board is designed for a Pi Zero but I take advantage of internal
connections to make it work for this board. As a result of this, the labels on the board have no meaning. The schematic and wiring diagrams are in
/circuit/output. 
