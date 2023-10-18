import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

#Настройка GPIO на Raspberry Pi
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
levels = 2**len(dac)
max = 3.3
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

#Функция двоичного предстваления
def decimal2binary(a):
    return [int(elem) for elem in bin(a)[2:].zfill(8)]

#Функция 
def adc():
    value_res = 0
    temp_value = 0
    for i in range(8):
        pow = 2**(8-i-1)
        temp_value = value_res + pow 
        signal = decimal2binary(temp_value)
        GPIO.output(dac,signal)
        time.sleep(0.001)
        compvalue = GPIO.input(comp)
        if (compvalue == 0):
            value_res = value_res + pow
            return value_res

#Зарядка и Разрядка конденсатора
try:
    time_start = time.time()
    schet = 0
    data = []
    all_time = []
    voltage = 0
    GPIO.output(troyka, 1)
    print('Идет зарядка конденсатора')
    while voltage <= 206 :
        voltage = adc()
        print(voltage)
        data.append(voltage/256*3.3)
        time.sleep(0)
        schet +=1
        GPIO.output (led, decimal2binary(voltage))
        all_time.append(time.time()-time_start)
    while voltage >= 177:
        voltage = adc()
        print(voltage)
        data.append(voltage/256*3.3)
        time.sleep(0)
        schet +=1
        GPIO.output (led, decimal2binary(voltage))
        all_time.append(time.time()-time_start)

    time_end = time.time()
    time_total = time_end - time_start
    print('График')
#График
    plt.plot(all_time, data)
    plt.xlabel('Секунды')
    plt.ylabel('Напряжение')
    print('Запись')

    with open ('data.txt', 'w') as f:
        for i in data:
            f.write(str(i) + '\n')
    with open ('settings.txt', 'w') as f:
            f.write('Частота дискретизации' + str(1/time_total * schet) + 'Гц' + '\n')
            f.write('Шаг квантования = 0.0129 В')
    
    print('Частота дискретизации, Гц :', schet/time_total)
    print('Продолжительность,С :', time_total)
    print('Шаг квантования, В: ', max/256)
    print('Завершение программы')
        
#Сброс
finally:
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.cleanup()
    plt.show()