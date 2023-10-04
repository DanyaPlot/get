import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
GPIO.setwarnings(False)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)] 

def bin_leds(a):
    for i in range(8,0,-1):
        if i*32 - 1 <= a:
            return decimal2binary(2**i - 1)
    return decimal2binary(0)        
def adc(troyka):
    a = 0
    for i in range (7, -1, -1):
        GPIO.output(dac,decimal2binary(a+2**i))
        sleep(0.007)
        if GPIO.input(comp)==0:
            a +=2**i
    return a        

try:
    while True:
            GPIO.output(led, bin_leds(adc(troyka)))
            
        
     
finally:
    GPIO.output(dac, [0]+8)
    GPIO.cleanup()