# the software for the motor controllerboard. Listens to the mainboard over UART and controls the motors accordingly.

import board
import digitalio
import busio
import time
import asyncio
import pwmio

from adafruit_motor import servo

class MotorController():
    def __init__(self):
        self.conn_led = digitalio.DigitalInOut(board.GP18)
        self.conn_led.direction = digitalio.Direction.OUTPUT
        self.conn_led.value = False

        self.motor_led = digitalio.DigitalInOut(board.GP28)
        self.motor_led.direction = digitalio.Direction.OUTPUT
        self.motor_led.value = False

        self.buzzer = pwmio.PWMOut(board.GP0, frequency=440, duty_cycle=0)

        self.uart = busio.UART(board.GP12, board.GP13, baudrate=9600, receiver_buffer_size=1, timeout=0.05)
        self.connected = False
        self.last_packet_time = time.monotonic()

        servo_left_pwm = pwmio.PWMOut(board.GP27, frequency=50)
        self.servo_left = servo.Servo(servo_left_pwm)

        servo_right_pwm = pwmio.PWMOut(board.GP26, frequency=50)
        self.servo_right = servo.Servo(servo_right_pwm)

        self.motors_down = False
    
    async def manage_buzzer(self):
        # beep the buzzer if the connection is lost
        # this is intended as a battery-saving feature
        # to make sure the user doesn't turn off the mainboard
        # and forget about the motor controller
        while True:
            if not self.connected:
                self.buzzer.duty_cycle = 2**15
                await asyncio.sleep(0.5)
                self.buzzer.duty_cycle = 0
                await asyncio.sleep(0.5)
            else:
                self.buzzer.duty_cycle = 0

            await asyncio.sleep(0)

    async def manage_motors(self):
        # control the motors based on the state
        while True:
            if self.motors_down:
                self.servo_left.angle = 90
                self.servo_right.angle = 90
                self.motor_led.value = True
            else:
                self.servo_left.angle = 0
                self.servo_right.angle = 180
                self.motor_led.value = False

            await asyncio.sleep(0)
    
    async def comms_read(self):
        # watch the UART for incoming packets, and update the state accordingly
        while True:
            if self.uart.in_waiting:
                packet = self.uart.read(1)
                if packet == b'U':
                    self.motors_down = False
                elif packet == b'D':
                    self.motors_down = True
                else:
                    print("Invalid packet received")
                    continue
                self.last_packet_time = time.monotonic()
            
            # this logic looks a little weird because it has to interoperate with blink_conn_led
            # but it really just checks if the connection is alive and sets the led accordingly
            if self.last_packet_time + 1 < time.monotonic():
                if self.connected:
                    # connection was just lost
                    self.conn_led.value = False
                self.connected = False
            else:
                if not self.connected:
                    # connection was just established
                    self.conn_led.value = True
                self.connected = True
            await asyncio.sleep(0)

    async def blink_conn_led(self, time):
        # helper for comms_heartbeat
        # this logic looks a little weird because the led has to both communicate heartbeats and connection status
        print(f"blink_conn_led {time} (connected: {self.connected})")
        if self.connected:
            self.conn_led.value = False
        else:
            self.conn_led.value = True
        await asyncio.sleep(time)
        if self.connected: # re-check because it may have changed during the sleep
            self.conn_led.value = True
        else:
            self.conn_led.value = False

    async def comms_heartbeat(self):
        # send a heartbeat to the mainboard every 0.5sec
        # so that it knows this board is not only connected but alive
        while True:
            self.uart.write(b'HB')
            await self.blink_conn_led(0.1)
            await asyncio.sleep(0.4) # then wait for 0.4sec for a total of 2Hz heartbeat

    async def run(self):
        buzzer_task = asyncio.create_task(self.manage_buzzer())
        motor_task = asyncio.create_task(self.manage_motors())
        comms_read_task = asyncio.create_task(self.comms_read())
        comms_heartbeat_task = asyncio.create_task(self.comms_heartbeat())

        await asyncio.gather(buzzer_task, motor_task, comms_read_task, comms_heartbeat_task)


motor_controller = MotorController()
asyncio.run(motor_controller.run())
