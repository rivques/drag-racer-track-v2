import board
import digitalio
import asyncio
import displayio
import terminalio
import adafruit_displayio_ssd1306
import busio
from adafruit_ht16k33 import segments
from lib.errors import ErrorType, Error
import time
from adafruit_display_text import text_box

class Mainboard:
    def __init__(self):
        # state
        self.state = "IDLE" # IDLE, ARMED, COUNTDOWN, RACING

        self.error_type = ErrorType.NONE
        self.error = None

        self.race_start_time = 0
        self.left_finish_time = 0
        self.right_finish_time = 0

        self.controller_state = "UNPLUGGED"
        self.motor_state = "UNPLUGGED"
        self.last_motor_packet_time = 0

        # set up buses
        i2c = busio.I2C(board.GP21, board.GP22)
        self.uart = busio.UART(board.GP0, board.GP1, baudrate=9600)
    
        # error hardware
        self.error_led = digitalio.DigitalInOut(board.GP15)
        self.error_led.direction = digitalio.Direction.OUTPUT
        self.error_led.value = False
        displayio.release_displays()
        error_display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        self.error_display = adafruit_displayio_ssd1306.SSD1306(error_display_bus, width=128, height=64)
        self.error_display_text = text_box.TextBox(terminalio.FONT, width=128, height=64, align=text_box.TextBox.ALIGN_CENTER, text="Starting up...")
        self.error_display.root_group = self.error_display_text
        
        # time display hardware
        self.left_time_display = segments.BigSeg7x4(i2c, address=0x70)
        self.right_time_display = segments.BigSeg7x4(i2c, address=0x71)
        self.starting_leds = []
        for red_pin, green_pin in [(board.GP9, board.GP10), (board.GP11, board.GP12), (board.GP13, board.GP14)]:
            red_led = digitalio.DigitalInOut(red_pin)
            red_led.direction = digitalio.Direction.OUTPUT
            red_led.value = False
            green_led = digitalio.DigitalInOut(green_pin)
            green_led.direction = digitalio.Direction.OUTPUT
            green_led.value = False
            self.starting_leds.append((red_led, green_led))
        
        # beam watch hardware
        self.left_beam = digitalio.DigitalInOut(board.GP26)
        self.left_beam.direction = digitalio.Direction.INPUT
        self.left_beam.pull = digitalio.Pull.UP
        self.right_beam = digitalio.DigitalInOut(board.GP27)
        self.right_beam.direction = digitalio.Direction.INPUT
        self.right_beam.pull = digitalio.Pull.UP

        # controller hardware
        self.reset_button = digitalio.DigitalInOut(board.GP4)
        self.reset_button.direction = digitalio.Direction.INPUT
        self.reset_button.pull = digitalio.Pull.UP
        self.race_button = digitalio.DigitalInOut(board.GP6)
        self.race_button.direction = digitalio.Direction.INPUT
        self.race_button.pull = digitalio.Pull.UP
        self.arm_button = digitalio.DigitalInOut(board.GP5)
        self.arm_button.direction = digitalio.Direction.INPUT
        self.arm_button.pull = digitalio.Pull.UP
        self.controller_presence = digitalio.DigitalInOut(board.GP8)
        self.controller_presence.direction = digitalio.Direction.INPUT
        self.controller_presence.pull = digitalio.Pull.UP
        self.controller_discrim = digitalio.DigitalInOut(board.GP7)
        self.controller_discrim.direction = digitalio.Direction.INPUT
        # no pull for controller discrim
        self.arm_led = digitalio.DigitalInOut(board.GP16)
        self.arm_led.direction = digitalio.Direction.OUTPUT
        self.arm_led.value = True
        self.race_led = digitalio.DigitalInOut(board.GP17)
        self.race_led.direction = digitalio.Direction.OUTPUT
        self.race_led.value = False

        # motor hardware
        self.motor_presence = digitalio.DigitalInOut(board.GP3)
        self.motor_presence.direction = digitalio.Direction.INPUT
        self.motor_presence.pull = digitalio.Pull.UP
        self.motor_discrim = digitalio.DigitalInOut(board.GP2)
        self.motor_discrim.direction = digitalio.Direction.INPUT
        # no pull for motor discrim

    async def run_error_display(self):
        while True:
            if self.error_type == ErrorType.NONE:
                self.error_led.value = False
                self.error_display_text.text = "Drag Racer Track V2\n"+ self.state
            else:
                self.error_led.value = True
                self.error_display_text.text = f"{'RECOVERABLE' if self.error_type == ErrorType.RECOVERABLE else "FATAL"} Error: {self.error.error_code}\n{self.error.short_msg}\nSEE DOCS ON GITHUB AT\nrivques/drag-racer-track-v2\nOR AT rivques.dev/chs/drtv2 OR ON\n Wayback Machine AT THOSE URLs"
                if self.error_type == ErrorType.RECOVERABLE:
                    await self.blink_error_led()
            await asyncio.sleep(0)
    
    async def blink_error_led(self):
        while self.error_type == ErrorType.RECOVERABLE:
            self.error_led.value = True
            await asyncio.sleep(0.5)
            self.error_led.value = False
            await asyncio.sleep(0.5)
    
    async def manage_input(self):
        while True:
            await asyncio.sleep(0)
            old_state = self.controller_state
            if self.controller_presence.value == True:
                self.controller_state = "UNPLUGGED"
                if not self.error:
                    self.error_type = ErrorType.RECOVERABLE
                    self.error = Error(200, "Controller unplugged")
            else:
                self.controller_state = "PLUGGED"
                # we're plugged in
                if old_state == "UNPLUGGED":
                    # clear the error if it was set
                    if self.error and self.error.error_code == 200:
                        self.error_type = ErrorType.NONE
                        self.error = None
                    # check if discrim is correct
                    if self.controller_discrim.value == False:
                        if not self.error:
                            self.error_type = ErrorType.RECOVERABLE
                            self.error = Error(201, "Motor port wrong")
                            continue
                    else:
                        if self.error and self.error.error_code == 201:
                            self.error_type = ErrorType.NONE
                            self.error = None
                # by this point we've confirmed we have the correct cable in the correct port
                if self.state == "IDLE":
                    if self.arm_button.value == False:
                        self.state = "ARMED"
                    # we can't do anything else in IDLE
                elif self.state == "ARMED":
                    if self.race_button.value == False:
                        self.state = "COUNTDOWN"
                    if self.reset_button.value == False:
                        self.state = "IDLE"
                elif self.state == "COUNTDOWN":
                    if self.reset_button.value == False:
                        self.state = "IDLE"
                elif self.state == "RACING":
                    if self.reset_button.value == False:
                        self.state = "IDLE"
    
    async def blink_controller_leds(self):
        last_blink = time.monotonic()
        while True:
            asyncio.sleep(0)
            if self.controller_state == "UNPLUGGED":
                self.arm_led.value = True
            else:
                if self.state == "IDLE":
                    if last_blink + 0.5 < time.monotonic():
                        self.arm_led.value = not self.arm_led.value
                        last_blink = time.monotonic()
                    self.race_led.value = False
                elif self.state == "ARMED":
                    self.arm_led.value = True
                    if last_blink + 0.5 < time.monotonic():
                        self.race_led.value = not self.arm_led.value
                        last_blink = time.monotonic()
                elif self.state == "COUNTDOWN":
                    self.arm_led.value = True
                    self.race_button.value = True
                elif self.state == "RACING":
                    self.arm_led.value = False
                    if last_blink + 0.5 < time.monotonic():
                        self.race_led.value = not self.race_led.value
                        last_blink = time.monotonic()        
    
    async def watch_beams(self):
        while True:
            await asyncio.sleep(0)
            if self.state == "RACING":
                if self.left_beam.value == False:
                    self.left_finish_time = time.monotonic()
                if self.right_beam.value == False:
                    self.right_finish_time = time.monotonic()
                if self.left_finish_time > 0 and self.right_finish_time > 0:
                    self.state = "IDLE"

    async def run_time_display(self):
        def format_time(seconds):
            return f"{int(seconds)}:{int(seconds*100%100):02}"
        while True:
            await asyncio.sleep(0)
            if self.state == "IDLE":
                for red_led, green_led in self.starting_leds:
                    red_led.value = False
                    green_led.value = False
                if not self.left_finish_time:
                    self.left_time_display.print("DnF")
                if not self.right_finish_time:
                    self.right_time_display.print("DnF")
            elif self.state == "ARMED":
                self.left_time_display.print("00:00")
                self.right_time_display.print("00:00")
                for red_led, green_led in self.starting_leds:
                    red_led.value = False
                    green_led.value = False
            elif self.state == "COUNTDOWN":
                # here the standard flow of this loop is broken, this is the entire countdown sequence
                self.starting_leds[0][0].value = True
                await asyncio.sleep(0.5)
                self.starting_leds[1][0].value = True
                await asyncio.sleep(0.5)
                self.starting_leds[2][0].value = True
                await asyncio.sleep(0.5)
                # RACE STARTS HERE
                self.state = "RACING"
                for red_led, green_led in self.starting_leds:
                    red_led.value = False
                    green_led.value = True
                self.race_start_time = time.monotonic()
                self.left_finish_time = 0
                self.right_finish_time = 0
            elif self.state == "RACING":
                elapsed = self.race_start_time - time.monotonic()
                if self.left_finish_time:
                    self.left_time_display.print(format_time(self.left_finish_time - self.race_start_time))
                else:
                    self.left_time_display.print(format_time(elapsed))
                if self.right_finish_time:
                    self.right_time_display.print(format_time(self.right_finish_time - self.race_start_time))
                else:
                    self.right_time_display.print(format_time(elapsed))
   
    async def manage_motors(self):
        while True:
            await asyncio.sleep(0.1)
            old_state = self.motor_state
            if self.motor_presence.value == True:
                self.motor_state = "UNPLUGGED"
                if not self.error:
                    self.error_type = ErrorType.RECOVERABLE
                    self.error = Error(300, "Motor unplugged")
            else:
                self.motor_state = "PLUGGED"
                # we're plugged in
                if old_state == "UNPLUGGED":
                    # clear the error if it was set
                    if self.error and self.error.error_code == 300:
                        self.error_type = ErrorType.NONE
                        self.error = None
                    # check if discrim is correct
                    if self.motor_discrim.value == False:
                        if not self.error:
                            self.error_type = ErrorType.RECOVERABLE
                            self.error = Error(301, "Motor port wrong")
                            continue
                    else:
                        if self.error and self.error.error_code == 301:
                            self.error_type = ErrorType.NONE
                            self.error = None
                # by this point we've confirmed we have the correct cable in the correct port
                packet = ""
                while self.uart.in_waiting:
                    self.last_motor_packet_time = time.monotonic()
                    packet += self.uart.read(1).decode()
                # we don't actually care about the packet, only that it exists
                if self.last_motor_packet_time + 1 < time.monotonic():
                    if not self.error:
                        self.error_type = ErrorType.RECOVERABLE
                        self.error = Error(302, "Motor not responding")
                else:
                    if self.error and self.error.error_code == 302:
                        self.error_type = ErrorType.NONE
                        self.error = None
                # tell the motor what to do
                if self.state == "IDLE":
                    self.uart.write(b"UP\n")
                elif self.state == "ARMED":
                    self.uart.write(b"DOWN\n")
                elif self.state == "COUNTDOWN":
                    self.uart.write(b"DOWN\n")
                elif self.state == "RACING":
                    self.uart.write(b"UP\n")

    
    async def run(self):
        error_display_task = asyncio.create_task(self.run_error_display())
        input_task = asyncio.create_task(self.manage_input())
        controller_led_task = asyncio.create_task(self.blink_controller_leds())
        time_display_task = asyncio.create_task(self.run_time_display())
        motor_management_task = asyncio.create_task(self.manage_motors())
        beam_watch_task = asyncio.create_task(self.watch_beams())

        await asyncio.gather(error_display_task, input_task, controller_led_task, time_display_task, motor_management_task, beam_watch_task)

mainboard = Mainboard()
asyncio.run(mainboard.run())