#!/usr/bin/env python

# Copyright (c) 2019-2020, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import RPi.GPIO as GPIO
import time


output_pins = {
    'JETSON_XAVIER': 18,
    'JETSON_NANO': 33,
    'JETSON_NX': 33,
    'CLARA_AGX_XAVIER': 18,
    'JETSON_TX2_NX': 32,
}
output_pin = output_pins.get(GPIO.model, None)

# Motor A (left side)
pwmA = 32
in1A = 16
in2A = 18

# Motor B (right side)
pwmB = 33
in1B = 24
in2B = 26




if output_pin is None:
    raise Exception('PWM not supported on this board')


def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of LOW
    
    # pwmA
    GPIO.setup(pwmA, GPIO.OUT, initial=GPIO.LOW)
    # in1A
    GPIO.setup(in1A, GPIO.OUT, initial=GPIO.LOW)
    # in2A
    GPIO.setup(in2A, GPIO.OUT, initial=GPIO.LOW)
    # pwmB
    GPIO.setup(pwmB, GPIO.OUT, initial=GPIO.LOW)
    # in1B
    GPIO.setup(in1B, GPIO.OUT, initial=GPIO.LOW)
    # in2B
    GPIO.setup(in2B, GPIO.OUT, initial=GPIO.LOW)



    # Motor speed (max speed is 100)
    motorSpeed_A = 100
    motorSpeed_B = 100
    
    p1 = GPIO.PWM(pwmA, 50)
    p2 = GPIO.PWM(pwmB, 50)

    p1.start(motorSpeed_A)
    p2.start(motorSpeed_B)



    print("Core running. Press CTRL+C to exit.")
    while True: 
        # Set motor A forward
        GPIO.output(in1A, GPIO.HIGH)
        GPIO.output(in2A, GPIO.LOW)

        # Set motor B forward
        GPIO.output(in1B, GPIO.LOW)
        GPIO.output(in2B, GPIO.HIGH)

        p1.ChangeDutyCycle(motorSpeed_A)
        p2.ChangeDutyCycle(motorSpeed_B)


    
        

if __name__ == '__main__':
    main()
