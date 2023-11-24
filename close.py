#!/usr/bin/env python

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
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
import os
#import commands

# Pin Definitons:

out_pin = 7


def main():
    #prev_value = None

    # Pin Setup:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(out_pin, GPIO.OUT)  # LED pin set as output
    #print("Starting demo now! Press CTRL+C to exit")
    #curr_value = 1
    GPIO.output(out_pin, 0)
    #try:
        #while True:
            #print("output_value:{}".format(curr_value))
            #GPIO.output(out_pin, curr_value)
            #time.sleep(15)
            #curr_value = curr_value + 1
            #curr_value = curr_value % 2
    #finally:
        #GPIO.cleanup()  # cleanup all GPIO
        #cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
