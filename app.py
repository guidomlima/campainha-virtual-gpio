import time, os, datetime
import json, requests
import notificacao
import RPi.GPIO as GPIO

def button_callback(channel):
    criaNotificacao()
    time.sleep(3)
    os.system("clear")
    exibirMenu()

def criaNotificacao():
    encontrou = verificaNotificacao()
    if not encontrou:
        notificacao = {"status": "tocando"}
        post = requests.post("http://127.0.0.1:5000/notificacao", json=notificacao)
        if post.status_code != 201:
            print('POST /notificacao {}'.format(post.status_code))
            
def verificaNotificacao():
    response = requests.get("http://127.0.0.1:5000/notificacao/{0}".format("tocando"))
    dados = json.loads(response.content)
    encontrou = 0
    if response.status_code == 206:
        print(response.status_code)
        print(dados[0]['message'])
        notificacao.status="aguardando"
    else:
        notificacao.id = dados[0]['_id']
        notificacao.dataehora = dados[0]['dataehora']
        notificacao.status = dados[0]['status']
        print("Já existe uma notificacao com status tocando")
        encontrou = 1
    return encontrou
    
def exibirMenu():
    print("Opções:")
    print("1 - Tocar Botão Campainha")
    print("2 - Abrir Trava Portão")
    print("3 - Sair")
    print("-------------------------")
    print("Digite: ")

notificacao = notificacao.Notificacao(0, datetime.datetime.now, 'aguardando')
botao = 16
led = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(botao,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

GPIO.add_event_detect(botao,GPIO.RISING,callback=button_callback)

continua = 1
while continua:
    exibirMenu()
    resp = input()
    nenhum = 1
    if resp.isnumeric():
        resp = int(resp)
        if resp == 1:
            criaNotificacao()
            nenhum = 0
        elif resp == 2:
            GPIO.output(led, 1)
            print("Portão aberto")
            time.sleep(3)
            GPIO.output(led, 0)
            nenhum = 0
        elif resp == 3:
            continua = 0
            nenhum = 0
    if nenhum:
        print("Digite 1 ou 2")
        print("-------------------------")
    time.sleep(3)
    os.system("clear")

GPIO.cleanup
