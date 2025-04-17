# Assembly From Scratch
This document describes how to assemble the racetrack from scratch. If you're just assembling from storage, see [assembly_from_storage.md](docs/assembly_from_storage.md).

## Parts
See [the bill of materials](docs/bill_of_materials.md) for a list of parts.

## Electronics
### Motor controller
1. Solder an Adafruit Perma-Proto Bonnet Mini according to the [wiring diagram](circuit/outputs/motorcontrollerwiring.png). [Here](doc-pics/motorcontroller-bottom.jpg) are [some](doc-pics/motorcontroller-top-withoutpico.jpg) [pictures](doc-pics/motorcontroller-top-withpico.jpg) of what it should look like (albeit without the battery and switch).
2. Print out the (yet-to-be-designed) front pieces.
3. Mount the servo motors...
TODO: update 

### Mainboard
1. If you're using a generic OLED instead of an Adafruit OLED, bridge the jumpers on the mainboard PCB accordingly.
2. Solder headers and breakout boards to the mainboard PCB according to the [schematic](circuit/outputs/mainboard.pdf). I reccommend soldering female headers to the board for the Pico, RJ45 breakout and OLED but you can choose to solder them directly to the board if you wish.
3. Run a bodge wire from GP20 on the unused pins header to an SDA pin. This corrects for the board incorrectly wiring GP22 to SDA.
### LED board
1. 

## Structure
1. Print out the 3D-printed parts.
2. Using a soldering iron, insert the heat-set inserts. It may help to slightly counterbore the holes with a 1/8in bit, to help the inserts seat. It's important that the inserts go in as straight as possible.
3. Modify the beam-break sensors by carefully drilling out their bolt holes to 1/8 in. Then, for the emitters, terminate their wires with a female DuPont connector. For the receivers, extend their wires to ~320mm and terminate with female DuPont.
4. Bolt the various electronics onto the 3D-printed frame. The mainboard, motor controller, and LED board are installed on standoffs. 
5. Neaten up the cables with zip ties.
6. Bolt the pieces together and connect the electronics to the mainboard according to the silkscreened pinouts.

By this point you have all the subassemblies needed to follow [the assembly from storage instructions](docs/assembly_from_storage.md).
