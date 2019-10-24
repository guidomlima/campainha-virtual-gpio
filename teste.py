# Definindo da biblioteca GPIO
import RPi.GPIO as GPIO

# Aqui definimos que vamos usar o numero de ordem do pino, e não o numero que refere a porta
# Para usar o numero da porta, é preciso trocar a definição "GPIO.BOARD (ex. Pino 12)" para "GPIO.BCM (ex.GPIO 18)"
GPIO.setmode(GPIO.BOARD)
# Setando as portas de entrada e saída
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.IN)
# Loop principal (Laço indefinido)
while(True):
    if GPIO.input == False:
        GPIO.output(12, 1)
    if GPIO.output == True:
        GPIO.output(12, 0)
