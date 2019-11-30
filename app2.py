#requests com jwt
import time, os, datetime
import json, requests
import notificacao, gpio
import RPi.GPIO as GPIO
from threading import Thread

notificacao = notificacao.Notificacao(0, datetime.datetime.now, 'aguardando')
gpio = gpio.Gpio(0,0,0)
botao = 16
led = 18

def button_callback(channel):
    criaNotificacao()
    time.sleep(3)
    os.system("clear")
    exibirMenu()
    
def abrirPortao():
    GPIO.output(led, 1)
    print("Portão aberto")
    time.sleep(3)
    GPIO.output(led, 0)

def criaNotificacao():
    encontrou = verificaNotificacao()
    if not encontrou:
        jNotificacao = {"status": "tocando"}
        put = requests.put("http://127.0.0.1:5000/notificacao/{0}".format("encerrada"), json=jNotificacao)
        if put.status_code != 201:
            print('PUT /notificacao {}'.format(put.status_code))
            
def verificaNotificacao():
    response = requests.get("http://127.0.0.1:5000/notificacao/{0}".format("tocando"))
    dados = json.loads(response.content)
    encontrou = 0
    if response.status_code == 206:
        print(response.status_code)
        print(dados[0]['message'])
        notificacao.status="aguardando"
    else:
        notificacao.idNotificacao = dados[0]['_id']
        notificacao.dataehora = dados[0]['dataehora']
        notificacao.status = dados[0]['status']
        print("Já existe uma notificacao com status tocando")
        encontrou = 1
    return encontrou

def atualizaGpio():
    if verificaGpio() and gpio.status:
        abrirPortao()               
        gpio.status = 0
        jGpio = {"pin": gpio.pin, "status": gpio.status}
        put = requests.put("http://127.0.0.1:5000/gpio", json=jGpio)
        if put.status_code != 201:
            print('POST /gpio {}'.format(put.status_code))
        os.system("clear")
        exibirMenu()

def verificaGpio():
    response = requests.get("http://127.0.0.1:5000/gpio/{0}".format(led))
    dados = json.loads(response.content)
    encontrou = 0
    if response.status_code == 206:
        print(response.status_code)
        print(dados[0]['message'])
        gpio.status="0"
    else:
        gpio.idGpio = dados[0]['_id']
        gpio.pin = dados[0]['pin']
        gpio.status = dados[0]['status']
        encontrou = 1
    return encontrou

def exibirMenu():
    print("Opções:")
    print("1 - Tocar Botão Campainha")
    print("2 - Abrir Trava Portão")
    print("3 - Sair")
    print("-------------------------")
    print("Digite: ")

def appinput(continua):
    while continua[0]:
        exibirMenu()
        resp = input()
        nenhum = 1
        if resp.isnumeric():
            resp = int(resp)
            if resp == 1:
                criaNotificacao()
                nenhum = 0
            elif resp == 2:
                abrirPortao()
                nenhum = 0
            elif resp == 3:
                continua[0] = 0
                nenhum = 0
        if nenhum:
            print("Digite 1 ou 2")
            print("-------------------------")
        time.sleep(3)
        os.system("clear")
    
    GPIO.cleanup

def handler(continua):
    while continua[0]:
        atualizaGpio()
        time.sleep(1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(botao,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

GPIO.add_event_detect(botao,GPIO.RISING,callback=button_callback)

def main():
    continua = [1]
    ai = Thread(target=appinput,args=[continua])
    h = Thread(target=handler,args=[continua])
    
    ai.start()
    h.start()
    
main()
