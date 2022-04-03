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

import pygame
import RPi.GPIO as GPIO
import time



 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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
 
 
class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10
 
 
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
 
# Get ready to print
textPrint = TextPrint()



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
motorSpeed_A = 0
motorSpeed_B = 0
    
p1 = GPIO.PWM(pwmA, 50)
p2 = GPIO.PWM(pwmB, 50)

p1.start(motorSpeed_A)
p2.start(motorSpeed_B)


# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        
        #if event.type == pygame.JOYBUTTONDOWN:
         #   print("Ricky Bolzoni")
        #if event.type == pygame.JOYBUTTONUP:
         #   print("Cimeo")
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
 
    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
 
        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()
 
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))
 
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes))
        textPrint.indent()
 
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            if(i == 1 and axis == -1):
                print("UP")
            elif(i == 1 and axis > 0):
                print("DOWN")
            elif(i == 0 and axis == -1):
                print("LEFT")
                motorSpeed_A = 50
                motorSpeed_B = 100
                print('Motor spreed A: ' + str(motorSpeed_A))
                print('Motor spreed B: ' + str(motorSpeed_B))
            elif(i == 0 and axis > 0):
                print("RIGHT")
                motorSpeed_A = 100
                motorSpeed_B = 50
                print('Motor spreed A: ' + str(motorSpeed_A))
                print('Motor spreed B: ' + str(motorSpeed_B))
            elif(i == 0 and axis == 0):
                motorSpeed_A = 100
                motorSpeed_B = 100
                print('Motor spreed A: ' + str(motorSpeed_A))
                print('Motor spreed B: ' + str(motorSpeed_B))
        textPrint.unindent()
 
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
 
        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
            if(i == 0 and button == 1):
                print("Triangle")
            elif(i == 1 and button == 1):
                print('Circle')
            elif(i == 2):
                if(button == 1):
                   print("X")
                   # Set motor A forward
                   GPIO.output(in1A, GPIO.HIGH)
                   GPIO.output(in2A, GPIO.LOW)

                   # Set motor B forward
                   GPIO.output(in1B, GPIO.LOW)
                   GPIO.output(in2B, GPIO.HIGH)

                   p1.ChangeDutyCycle(motorSpeed_A)
                   p2.ChangeDutyCycle(motorSpeed_B)
                
                elif(button == 0):
                   
                   p1.ChangeDutyCycle(0)
                   p2.ChangeDutyCycle(0)

            elif(i == 3 and button == 1):
                   
                   print("Square")
                   # Set motor A forward
                   GPIO.output(in1A, GPIO.LOW)
                   GPIO.output(in2A, GPIO.HIGH)

                   # Set motor B forward
                   GPIO.output(in1B, GPIO.HIGH)
                   GPIO.output(in2B, GPIO.LOW)

                   p1.ChangeDutyCycle(motorSpeed_A)
                   p2.ChangeDutyCycle(motorSpeed_B)
                

            elif(i == 4 and button == 1):
                print("L2")
            elif(i == 5 and button == 1):
                print("R2")
            elif(i == 6 and button == 1):
                print("L1")
            elif(i == 7 and button == 1):
                print("R1")
            elif(i == 8 and button == 1):
                print("Select")
            elif(i == 9 and button == 1):
                print("Start")
            

        textPrint.unindent()
 
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats))
        textPrint.indent()
 
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()
 
        textPrint.unindent()
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
