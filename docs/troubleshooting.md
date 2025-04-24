# Troubleshooting
## I'm getting an error code!
error code|problem|resolution
---|---|---
100|The left time display is not found.|Check that the wiring to the left display is accurate. Failing that, check that the battery is full.
101|The right time display is not found.|Check that the wiring to the right display is accurate. Failing that, check that the battery is full.
200|The race controller is unplugged.|Plug in the race controller. Failing that, check the ethernet cable. Failing that, check that the race controller's circuitry is accurate and not shorted.
201|The motor controller is plugged into the race controller port.|Plug the motor controller into the correct port. Failing that, check the ethernet cable.
300|The motor controller is unplugged.|Plug in the motor controller. Failing that, check the ethernet cable. Failing that, check that the motor controller's circuitry is accurate and not shorted.
301|The race controller is plugged into the motor controller port.|Plug the race controller into the correct port. Failing that, check the ethernet cable.
302|The motor controller is plugged in, but the race controller can't communicate with it.|Check that the motor controller is turned on. Failing that, check the ethernet cable.
## The mainboard is not powering on!
* Check that the battery is full. 
* Check that there is no short-circuit at the battery input.
## The motor controller is beeping!
* This means that it cannot communicate with the mainboard.
* Check that the mainboard is powered on.
* If the mainboard is showing an error code, resolve the error code.