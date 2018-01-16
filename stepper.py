import sys
import time
import threading
from RPi import GPIO
from enum import Enum


class Direction(Enum):
    Clockwise = 1
    CounterClockwise = 2
class Mode(Enum):
    EightStep = 1
    FourStep = 2

class Stepper:
    """
    Class to encapsulate a 28BYJ-48 stepper motor. Constructor sets up
    constants; __enter__ and __exit__ used to control GPIO resources.
    """

    def __init__(self, out_pins, mode=Mode.EightStep, steps_per_revolution=4096):
        """
        Set up variables for controller with a set of output pins
        (IN1, IN2, IN3, IN4; by broadcom SOC number).
        """
        # Initialize variables and constants
        self.out_pins = out_pins
        self.out_sequence = [[False, False, False, True],
                                [False, False, True,  True],
                                [False, False, True,  False],
                                [False, True,  True,  False],
                                [False, True,  False, False],
                                [True,  True,  False, False],
                                [True,  False, False, False],
                                [True,  False, False, True]]
        self.mode = mode
        self.steps_per_revolution = steps_per_revolution

        if self.mode == Mode.EightStep:
            self.step_size = 1
        elif self.mode == Mode.FourStep:
            self.step_size = 2
        else:
            raise Exception('Unexpected mode in Stepper ctor')

        self.current_step = 1

    def __enter__(self):
        """
        Initialize GIOP as specified in c-tor
        """
        GPIO.setup(self.out_pins, GPIO.OUT, initial=GPIO.LOW)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleanup all used GPIO pins
        """
        GPIO.cleanup(self.out_pins)


    def delay_time_from_rps(self, rps):
        """
        Returns delay time between output pin changes (in seconds) needed to
        attain the given rps (revolutions per second).
        """
        period = 1.0/rps # Period of one revolution, in seconds
        if self.mode == Mode.EightStep:
            return period/self.steps_per_revolution
        elif self.mode == Mode.FourStep:
            return period/self.steps_per_revolution*2
        else:
            raise Exception('Unexpected mode in Stepper.delay_time_from_rpm()')

    def revolutions_from_steps(self, steps):
        """
        Returns the number of revolutions attained from a given number of steps.
        """
        if self.mode == Mode.EightStep:
            return steps/self.steps_per_revolution
        elif self.mode == Mode.FourStep:
            return steps/self.steps_per_revolution*2
        else:
            raise Exception('Unexpected mode in Stepper.revolutions_from_steps()')

    def run(self, rps, revolutions, direction):
        """
        Runs motor at a given revolutions-per-second, for a given amount of
        revolutions, going at a given direction.
        Assumes first revolution starts immediately after function first
        is called, which may not be true.
        """

        if direction == Direction.Clockwise:
            step_offset = -self.step_size
        elif direction == Direction.CounterClockwise:
            step_offset = self.step_size
        else:
            raise ValueError('Unexpected direction in Stepper.run()')

        delay_time = self.delay_time_from_rps(rps)

        num_steps = 0
        while True:
            # Time the loop to keep everything accurate
            start_time = time.perf_counter()

            # Enable GPIO pins in current step configuration
            GPIO.output(self.out_pins, self.out_sequence[self.current_step])
            # Advance counter to next step
            self.current_step = (self.current_step+step_offset) % len(self.out_sequence)
            # Calculate current revolutions
            num_steps += 1
            revolutions_so_far = self.revolutions_from_steps(num_steps)
            if revolutions_so_far >= revolutions:
                break

            # Wait for next step
            elapsed_time = time.perf_counter() - start_time
            time.sleep(max(delay_time - elapsed_time, 0))
