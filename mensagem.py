import RPi.GPIO as GPIO

def button_callback(channel):
	print("Botão pressionado")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(16,GPIO.RISING,callback=button_callback)

mensagem = input("Pressione ENTER para sair\n")

GPIO.cleanup
