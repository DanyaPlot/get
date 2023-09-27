import RPi.GPIO as GPIO
import time
import sys
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
def perev(value,n):
    return [int(element) for element in bin(value)[2:].zfill(8)] 
try:
    while True:
        T = input()
        if not T.isdigit():
            print('Write a number')
        t = T/256/2
        for i in range (256):
            GPIO.output (dac, perev(i, 8))
            sleep(5)
        for i in range(255, -1, -1):
            GPIO.output (dac, perev(i, 8))
            sleep(5)








finally:
    GPIO.output(dac, 1)
    GPIO.cleanup()