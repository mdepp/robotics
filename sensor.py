from RPi import GPIO
import time

class Sensor:
    """
    Defines a distance sensor with given trigger and echo pins. Use __enter__
    and __exit__ to control GPIO resources.
    """
    def __init__(self, trigger_pin, echo_pin, timeout=1, sound_speed=343):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.timeout = timeout
        self.sound_speed = sound_speed

    def __enter__(self):
        """
        Initialize GPIO pins.
        """
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleanup all used GPIO pins.
        """
        GPIO.cleanup(self.trigger_pin)
        GPIO.cleanup(self.echo_pin)

    def sense_distance(self):
        """
        Sends and receives a sound pulse, then uses the delay to calculate
        and return distance (in meters). Maximum delay timeout is specified in
        constructor.
        """
        # Trigger sensor with 10 microsecond pulse
        self.send_pulse(self.trigger_pin, 10 / 10**6)
        # Receive input from the echo pin
        echo_duration = self.receive_pulse(self.echo_pin, self.timeout)
        # Calculate and return distance
        return 0.5 * self.sound_speed * echo_duration

    """
    Helper functions.
    """

    def send_pulse(self, pin, duration):
        """
        Sends a pulse of a specific (in seconds) to a specific pin. The pin is
        assumed to be LOW beforehand and is set to LOW after.
        """
        GPIO.output(pin, True)
        time.sleep(duration)
        GPIO.output(pin, False)

    def receive_pulse(self, pin, timeout):
        """
        Wait and receive a pulse from a specified pin. Returns the duration (in
        seconds) of the pulse. 'timeout' defines the maximum amount of time
        (in seconds) this function will block before it returns anyway. Assumes pin
        starts as LOW.
        """
        GPIO.wait_for_edge(pin, GPIO.RISING, timeout=timeout*500)
        time_start = time.time()
        GPIO.wait_for_edge(pin, GPIO.FALLING, timeout=timeout*500)
        time_end = time.time()
        return time_end - time_start
