import RPi.GPIO as GPIO
import time as Time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

LOW = GPIO.LOW
HIGH = GPIO.HIGH
OUTPUT = GPIO.OUT
INPUT = GPIO.IN

def delay(time: int):
    '''
    :param time: time in milli seconds
    :type time: int
    '''
    Time.sleep(time / 10**3)

def delayMicros(time: int):
    '''
    :param time: time in micro seconds
    :type time: int
    '''
    Time.sleep(time / 10**6)

def digitalWrite(PIN, SIGNAL):
    '''
    :param PIN: PIN number 
    :param SIGNAL: LOW / HIGH
    '''
    if SIGNAL == LOW:
        return GPIO.output(PIN, LOW)
    elif SIGNAL == HIGH:
        return GPIO.output(PIN, HIGH)
    else:
        raise ValueError("SIGNAL must be LOW or HIGH!")
    
def digitalRead(PIN):
    '''
    :param PIN: PIN number
    '''
    return GPIO.input(PIN)

def pinMode(PIN, TYPE):
    '''
    :param PIN: PIN number
    :param TYPE: INPUT / OUTPUT
    '''
    if TYPE == INPUT:
        GPIO.setup(PIN, INPUT)
    elif TYPE == OUTPUT:
        GPIO.setup(PIN, OUTPUT)
    else:
        raise ValueError("TYPE must be INPUT or OUTPUT")