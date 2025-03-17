import board
import digitalio

break_beam = digitalio.DigitalInOut(board.GP26)
break_beam.direction = digitalio.Direction.INPUT
break_beam.pull = digitalio.Pull.UP

led_built_in = digitalio.DigitalInOut(board.LED)
led_built_in.direction = digitalio.Direction.OUTPUT

while True:
    if break_beam.value:
        led_built_in.value = False
    else:
        led_built_in.value = True