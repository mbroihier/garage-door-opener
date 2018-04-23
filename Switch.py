'''
Created on Apr 23, 2018

@author: broihier
'''
import time
import RPi.GPIO as GPIO

class Switch(object):
    '''
    Class for making a switch controller
    '''

    def __init__(self, duration):
        '''
        Constructor
        '''
        self.state = "open"
        self.duration = duration
        self.pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.open()

    def open(self):
        '''
        Open the switch (off/false)
        '''
        GPIO.output(self.pin, False)

    def close(self):
        '''
        Close the switch (on/true)
        '''
        GPIO.output(self.pin, True)

    def press(self):
        '''
        Press the switch closed for duration seconds
        '''
        self.close()
        time.sleep(self.duration)
        self.open()
