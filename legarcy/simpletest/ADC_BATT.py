from machine import Pin, ADC 
from time import sleep

analogue_value = machine.ADC(27)
VOLTAGE_DROP_FACTOR = 1 
 
while True:
    reading = analogue_value.read_u16()     
    voltage = reading * (4.5 / 65535) * VOLTAGE_DROP_FACTOR
    print(voltage)
    sleep(2)
