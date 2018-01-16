# About
This project provides easy-to-use Python classes for controlling stepper motors and ranged sensors from a Raspberry Pi.

The motor controller was written for a 28BYJ-48 stepper motor, and as such expects the motor position to be controlled by 4 inputs (with either a 4-step or 8-step driving sequence), and defaults steps per revolution to 4096, the (approximate) value for the that motor.

The range sensor controller was written for an HC-SR04 ultrasonic ranging sensor, which is controlled by trigger and echo pins. Since the 5V output from the echo pin is too much for the Raspberry Pi, a voltage divider is necessary to scale this to less that 3.3V.