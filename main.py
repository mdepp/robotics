"""
Sample usage which waits for something to pass in front of the sensor before
running two motors for one revolution
"""

from stepper import Stepper, Mode, Direction
from sensor import Sensor
from concurrent.futures import ThreadPoolExecutor
from RPi import GPIO
import time


# Set up GPIO
GPIO.setmode(GPIO.BCM)

stepper1_pins = [5, 6, 13, 19]
stepper2_pins = [22, 27, 17, 4]
rps = 0.25
revolutions = 1


with Sensor(trigger_pin=23, echo_pin=24) as sensor, \
        Stepper(stepper1_pins, Mode.FourStep) as stepper1, \
        Stepper(stepper2_pins, Mode.FourStep) as stepper2, \
        ThreadPoolExecutor(max_workers=5) as executor:

    direction = Direction.Clockwise

    while sensor.sense_distance() > 0.3:
        pass

    run1_result = executor.submit(stepper1.run, rps, revolutions, direction)
    run2_result = executor.submit(stepper2.run, rps, revolutions, direction)
    run1_result.result()
    run2_result.result()