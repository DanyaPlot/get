import RPi.GPIO as GPIO
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)] 
try:
    while True:
        print('Введи число от 0 до 255')
        value = input()
        if(value == 'q'):
            print(decimal2binary(value))
        elif (int(value) > 255 or int(value)<0):
            print ('Глаза разуй,пжшка')
            GPIO.output(dac, 0)
        else:
            GPIO.output(dac, decimal2binary(int(value)))
            print("{:.4f}".format(int(value)/255*3.3))


finally: 
    GPIO.output(dac, 0)
    GPIO.cleanup()

