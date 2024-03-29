import RPi.GPIO as GPIO
import time

led = 18
botao = 16

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(botao, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

espera = 1
while(espera):
    if GPIO.input(botao) == GPIO.HIGH:
        GPIO.output(led, 1)
        print("Apertou")
        espera = 0
    if GPIO.input(botao) == GPIO.LOW:
        GPIO.output(led, 0)
        print("Esperando")
time.sleep(3)
GPIO.cleanup()       
