import time, os, datetime
import json, requests
import notificacao
import RPi.GPIO as GPIO

def button_callback(channel):
    criaNotificacao()

def criaNotificacao():
    resp = verificaNotificacao()
    if not resp:
        notificacao = {"status": "tocando"}
        post = requests.post("http://127.0.0.1:5000/notificacao", json=notificacao)
        if post.status_code != 201:
            print('POST /notificacao {}'.format(post.status_code))
        else:
            print('Notificacao criada. ID: {}'.format(post.json()["_id"]))


def verificaNotificacao():
    response = requests.get("http://127.0.0.1:5000/notificacao/{0}".format("tocando"))
    print(response.status_code)
    dados = json.loads(response.content)
    resp = 0
    if response.status_code == 206:
        print(response.status_code)
        print(dados[0]['message'])
        print(notificacao.status)
    else:
        notificacao.id = dados[0]['_id']
        notificacao.dataehora = dados[0]['dataehora']
        notificacao.status = dados[0]['status']
        print("Já existe uma notificacao com status tocando. ID: {}".format(notificacao.status))
        resp = 1
    return resp

notificacao = notificacao.Notificacao(0, datetime.datetime.now, 'aguardando')
botao = 16
led = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(botao,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

GPIO.add_event_detect(botao,GPIO.RISING,callback=button_callback)

continua = 1
while continua:
    resp = verificaNotificacao()
    print("Opções:")
    print("1 - Tocar Botão Campainha")
    print("2 - Abrir Trava Portão")
    print("3 - Sair")
    print("-------------------------")
    if not resp:
        print("Digite: ")
        resp = input()
        resp = int(resp)
        if resp == 1:
            criaNotificacao()
        elif resp == 2:
            GPIO.output(led, 1)
            print("Portão aberto")
            time.sleep(3)
            GPIO.output(led, 0)
        elif resp == 3:
            continua = 0
        else:
            print("Digite 1 ou 2")
    else:
        print("-------------------------")
    time.sleep(3)
    os.system("clear")

GPIO.cleanup