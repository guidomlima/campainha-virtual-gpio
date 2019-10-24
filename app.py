import time, os
import json, requests
import gpio

botao = gpio.Gpio(0,90,0)
trava = gpio.Gpio(0,24,0)

while True:
    response = requests.get("http://127.0.0.1:5000/gpio/{0}".format(botao.pin))
    print(response.status_code)
    dados = json.loads(response.content)
    recebido = gpio.Gpio(dados[0]['_id'],dados[0]['pin'],dados[0]['status'])

    resp = 0
    if recebido.status == 1:
        resp = 1
    print("Opções:")
    print("1 - Tocar Botão Campainha")
    print("2 - Abrir Trava Portão")
    print("-------------------------")
    if resp==0:
      print("Digite: ")
      resp = input()
    else:
      print("Recebeu 1")
    print("-------------------------")

    resp = int(resp)
    if resp == 1:
        print("Tocou campainha")
        botao.status=1
    elif resp == 2:
        print("Abriu portão")
        trava.status = 1
    else:
        print("Digite 1 ou 2")
    time.sleep(3)
    botao.status = 0
    trava.status = 0
    os.system("clear")
