# drag-racer-track-v2
A new and improved version of [mini-drag-racetrack](https://github.com/rivques/mini-drag-racetrack).

## Contact Me
While this racetrack was designed to be maintainable by people other than me, please don't hesitate to contact me if you run into an issue that these docs don't cover.
You can open an issue on this repository or email me at `web (at) rivques (dot) dev`.

## How To Use
To be written.

## Assembly (from storage)

## Assembly (from scratch)
### Motor controller
1. Solder an Adafruit Perma-Proto Bonnet Mini according to the [wiring diagram](circuit/outputs/motorcontrollerwiring.png). [Here](doc-pics/motorcontroller-bottom.jpg) are [some](doc-pics/motorcontroller-top-withoutpico.jpg) [pictures](doc-pics/motorcontroller-top-withpico.jpg) of what it should look like (albeit without the battery and switch).
2. Print out the (yet-to-be-designed) front pieces.
3. Mount the servo motors...
TODO: finish this section once CAD happens
### Mainboard
1. If you're using a generic OLED instead of an Adafruit OLED, bridge the jumpers on the mainboard PCB accordingly.
2. Solder headers and breakout boards to the mainboard PCB according to the [schematic](circuit/outputs/mainboard.pdf). I reccommend soldering female headers to the board for the Pico, RJ45 breakout and OLED but you can choose to solder them directly to the board if you wish.
3. Run a bodge wire from GP20 on the unused pins header to an SDA pin. This corrects for the board incorrectly wiring GP22 to SDA.
### LED board
1. 
### Structure
1. Print out the 3D-printed parts.
2. Using a soldering iron, insert the heat-set inserts. It may help to slightly counterbore the holes with a 5/32in bit, to help the inserts seat. It's important that the inserts go in as straight as possible.
3. Modify the beam-break sensors by carefully drilling out their bolt holes to 1/8 in. Then, for the emitters, terminate their wires with a female DuPont connector. For the receivers, extend their wires to ~320mm and terminate with female DuPont.
4. Bolt the various electronics onto the 3D-printed frame. The mainboard, motor controller, and LED board are installed on standoffs. 


## Bill Of Materials
* 2x [Adafruit beam-break 3mm sensors](https://www.adafruit.com/product/2167)
* 4x [SparkFun RJ45 breakouts](https://www.sparkfun.com/sparkfun-rj45-breakout.html) with [SparkFun RJ45 conectors](https://www.sparkfun.com/rj45-8-pin-connector.html)
* 12x #4-40 McMaster heat-set inserts
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
