import RPi.GPIO as GPIO

led = 18
botao = 16

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(botao, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while(1):
    if GPIO.input(botao) == GPIO.HIGH:
        GPIO.output(led, 1)
        print("Apertou")
    if GPIO.input(botao) == GPIO.LOW:
        GPIO.output(led, 0)
        print("Soltou")
        