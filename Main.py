from flask import *
import datetime
import json
import time
import RPi.GPIO as gpio
app = Flask(__name__)

gpio.setmode(gpio.BOARD)

## Biblioteca contendo as saidas ##
pins = {
  12 : {'name' : 'atuador1', 'state' : gpio.LOW} ,
  16 : {'name' : 'atuador2', 'state' : gpio.LOW} ,
  8  : {'name' : 'esteira', 'state' : gpio.LOW} ,
  10 : {'name' : 'esteira2', 'state' : gpio.LOW} ,
  18 : {'name' : 'atuador3', 'state' : gpio.LOW},
  22 : {'name' : 'atuador4', 'state' : gpio.LOW} ,
}

## Biblioteca das Entradas ##
data = {
  7  : { 'name' : 'sensorAlto', 'state' : 'desligado'},
  11 : { 'name' : 'sensorBaixo', 'state' : 'desligado'},
  23 : { 'name' : 'sensorMetalico', 'state' : 'desligado'},
  29 : { 'name' : 'sensorFim', 'state' : 'desligado'},
  13 : { 'name' : 'sensorAT1', 'state' : 'desligado'},
  15 : { 'name' : 'sensorAT2', 'state' : 'desligado'},
  19 : { 'name' : 'sensorAT3', 'state' : 'desligado'},
  21 : { 'name' : 'sensorAT4', 'state' : 'desligado'}
  }

for pin in pins:
  gpio.setup(pin, gpio.OUT)
  gpio.output(pin, gpio.LOW)

## Configuraçoes ##
gpio.setup(7, gpio.IN)
gpio.setup(11, gpio.IN)
gpio.setup(23, gpio.IN)
gpio.setup(29, gpio.IN)
gpio.setup(13, gpio.IN)
gpio.setup(15, gpio.IN)
gpio.setup(19, gpio.IN)
gpio.setup(21, gpio.IN)

sensorAlto=gpio.input(7)
sensorBaixo=gpio.input(11)
sensorMetalico=gpio.input(23)
sensorFim=gpio.input(29)
sensorAT1=gpio.input(13)
sensorAT2=gpio.input(15)
sensorAT3=gpio.input(19)
sensorAT4=gpio.input(21)
ESTADOESTEIRA1 = "DESLIGADA"
ESTADOESTEIRA2 = "DESLIGADA"
PECA = "NENHUMA PECA NA ESTEIRA"
CON_TOTAL = 0
CON_NMETAL_BAIXA = 0
CON_NMETAL_ALTO = 0
CON_METAL_BAIXA = 0
CON_METAL_ALTO = 0
AUXSTART = False
AUXSENALTO = False
AUXSENBAIXO = False
AUXSENMETAL = False
AUXFIM = False
auxpeca=0
result="nada"

### programaçao da maquina ###
def rodar():
  sensorAlto=gpio.input(7)
  sensorBaixo=gpio.input(11)
  sensorMetalico=gpio.input(23)
  sensorFim=gpio.input(29)
  sensorAT1=gpio.input(13)
  sensorAT2=gpio.input(15)
  sensorAT3=gpio.input(19)
  sensorAT4=gpio.input(21)
  global START
  global EMERGENCIA
  global PECA
  global CON_NMETAL_BAIXA
  global CON_NMETAL_ALTO
  global CON_METAL_ALTO
  global CON_METAL_BAIXA
  global AUXSENALTO
  global AUXSENBAIXO
  global AUXSENMETAL
  global auxpeca
  global AUXFIM
  ## inicio ##
  if (START==True):

    gpio.output(8,gpio.HIGH)
    gpio.output(10,gpio.HIGH)
    ## Sensor de peça alta ##
    if (sensorAlto==True):
      AUXSENALTO=True

    ## Sensor de peça baixa ##
    if (sensorBaixo==True):
      AUXSENBAIXO=True

    ## Sensor metalico ##
    if (sensorMetalico==True):
      AUXSENMETAL=True


    if ((AUXSENBAIXO==True) and (AUXSENALTO==False) and (AUXSENMETAL==False)):
      PECA = "NAO METALICA BAIXA"
      auxpeca=1

    if ((AUXSENALTO==True) and (AUXSENMETAL==False)):
      PECA = "NAO METALICA ALTA"
      auxpeca=2

    if ((AUXSENALTO==False) and (AUXSENBAIXO==True) and (AUXSENMETAL==True)):
      PECA = "METALICA BAIXA"
      auxpeca=3

    if ((AUXSENALTO==True) and (AUXSENMETAL==True)):
      PECA = "METALICA ALTA"
      auxpeca=4


  if (START==False):

    gpio.output(8, gpio.LOW)
    gpio.output(10, gpio.LOW)
    AUXFIM=0
    auxpeca=0
    PECA = "NENHUMA PECA NA ESTEIRA"
    AUXSENALTO=False
    AUXSENBAIXO=False
    AUXSENMETAL=False
   ## Sensor fim de esteira ##
  if(sensorFim==True):

    gpio.output(8, gpio.LOW)
    gpio.output(10, gpio.LOW)
    time.sleep(3)
    gpio.output(10, gpio.HIGH)
    gpio.output(8, gpio.HIGH)
    AUXFIM=True

  if (AUXFIM==True):
    global CON_NMETAL_BAIXA
    global CON_NMETAL_ALTO
    global CON_METAL_ALTO
    global CON_METAL_BAIXA


    if (auxpeca==1):
      ## Sensor do atuador 1 ##
      if(sensorAT1==True):
        gpio.output(12, gpio.HIGH)
        CON_NMETAL_BAIXA = CON_NMETAL_BAIXA + 1
        time.sleep(1)
        gpio.output(12, gpio.LOW)

        auxpeca=0
        PECA = "NENHUMA PECA NA ESTEIRA"
        AUXFIM=0
        AUXSENALTO=False
        AUXSENBAIXO=False
        AUXSENMETAL=False

    elif (auxpeca==2):
      ## Sensor do atuador 2 ##
      if(sensorAT2==True):
        gpio.output(16, gpio.HIGH)
        CON_NMETAL_ALTO = CON_NMETAL_ALTO + 1
        time.sleep(1)
        gpio.output(16, gpio.LOW)

        auxpeca=0
        PECA = "NENHUMA PECA NA ESTEIRA"
        AUXFIM=0
        AUXSENALTO=False
        AUXSENBAIXO=False
        AUXSENMETAL=False


    elif (auxpeca==3):
      ## Sensor do atuador 3 ##
      if(sensorAT3==True):
        gpio.output(18, gpio.HIGH)
        CON_METAL_BAIXA = CON_METAL_BAIXA + 1
        time.sleep(1)
        gpio.output(18, gpio.LOW)

        auxpeca=0
        PECA = "NENHUMA PECA NA ESTEIRA"
        AUXFIM=0
        AUXSENALTO=False
        AUXSENBAIXO=False
        AUXSENMETAL=False

    elif (auxpeca==4):
      ## Sensor do atuador 4 ##
      if(sensorAT4==True):
        gpio.output(22, gpio.HIGH)
        CON_METAL_ALTO = CON_METAL_ALTO + 1
        time.sleep(1)
        gpio.output(22, gpio.LOW)

        auxpeca=0
        PECA = "NENHUMA PECA NA ESTEIRA"
        AUXFIM=0
        AUXSENALTO=False
        AUXSENBAIXO=False
        AUXSENMETAL=False


### Pagina inicial ###
@app.route('/')
def main():
  return render_template('PaginaPrincipal.html')

### Pagina de modo de Escolha ###
@app.route('/ModoDeEscolha')
def modo():
  for pin in pins:
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, gpio.LOW)


  return render_template('ModoDeEscolha.html')

### Pagina que efetua a leitura as entradas ###
@app.route("/switch")
def switch():
  def read_switch():
    while True:
      sensorAlto=gpio.input(7)
      sensorBaixo=gpio.input(11)
      sensorMetalico=gpio.input(23)
      sensorFim=gpio.input(29)
      sensorAT1=gpio.input(13)
      sensorAT2=gpio.input(15)
      sensorAT3=gpio.input(19)
      sensorAT4=gpio.input(21)

      yield 'data: {0}\n'.format(sensorAlto)
      yield 'data: {0}\n'.format(sensorBaixo)
      yield 'data: {0}\n'.format(sensorMetalico)
      yield 'data: {0}\n'.format(sensorFim)
      yield 'data: {0}\n'.format(sensorAT1)
      yield 'data: {0}\n'.format(sensorAT2)
      yield 'data: {0}\n'.format(sensorAT3)
      yield 'data: {0}\n\n'.format(sensorAT4)


      time.sleep(0.5)
  return Response(read_switch(), mimetype='text/event-stream')




### Pagina Manual ###
@app.route('/Manual')
def manual():

  for pin in pins:
    pins[pin]['state'] = gpio.input(pin)
  templateData = {
    'pins' : pins


    }

  return render_template('Manual.html', **templateData)


### Pagina manual que aciona as saidas ###
@app.route("/Manual/<changePin>/<action>")
def action(changePin, action):
  changePin = int(changePin)
  if ((changePin==8) and (action=="on")):
    gpio.output(8,gpio.HIGH)
    gpio.output(10,gpio.HIGH)
  elif ((changePin==8) and (action=="off")):
    gpio.output(8,gpio.LOW)
    gpio.output(10,gpio.LOW)

  else:


    if action == "on":
      gpio.output(changePin,gpio.HIGH)

    if action == "off":
      gpio.output(changePin,gpio.LOW)


    if action == "toggle":
      gpio.output(changePin,not gpio.input(changePin))


  for pin in pins:
    pins[pin]['state'] = gpio.input(pin)




  templateData = {
  'pins': pins
  }

  return render_template('Manual.html', **templateData)


### Pagina que efetua a leitura do estado da maquina ###
@app.route('/inicio')
def inicio():
    def auto_test():
        while True:


            global START
            global EMERGENCIA
            global PECA
            global CON_NMETAL_BAIXA
            global CON_NMETAL_ALTO
            global CON_METAL_ALTO
            global CON_METAL_BAIXA
            global AUXSENALTO
            global AUXSENBAIXO
            global AUXSENMETAL
            global result

            if (result=="inicio"):
                START=True
                rodar()

            if (result=="emerg"):
                START=False
                rodar()



            CON_TOTAL = CON_NMETAL_BAIXA + CON_NMETAL_ALTO + CON_METAL_BAIXA + CON_METAL_ALTO
            templateData = {
            'sensorAT1':gpio.input(13),
            'sensorAT2':gpio.input(15),
            'sensorAT3':gpio.input(19),
            'sensorAT4':gpio.input(21),
            'CON_TOTAL' : CON_TOTAL,
            'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
            'CON_NMETAL_ALTO' : CON_NMETAL_ALTO,
            'CON_METAL_BAIXA' : CON_METAL_BAIXA,
            'CON_METAL_ALTO' : CON_METAL_ALTO
            }





            yield 'data: {0}\n\n'.format(json.dumps(templateData))
            time.sleep(1.0)



    return Response(auto_test(),mimetype='text/event-stream')

### Pagina automatica em metodo Post ###
@app.route('/Automatico/<vonpar>', methods=['POST'])
def auto(vonpar):
  global START
  global EMERGENCIA
  global PECA
  global CON_NMETAL_BAIXA
  global CON_NMETAL_ALTO
  global CON_METAL_ALTO
  global CON_METAL_BAIXA
  global AUXSENALTO
  global AUXSENBAIXO
  global AUXSENMETAL
  global result

  if(vonpar=="inicio"):
      result="inicio"
  if(vonpar=="emerg"):
      result="emerg"
  if(vonpar=="zerar"):
    ESTADOESTEIRA1 = "DESLIGADA"
    ESTADOESTEIRA2 = "DESLIGADA"
    PECA = "NENHUMA PECA NA ESTEIRA"
    CON_TOTAL = 0
    CON_NMETAL_BAIXA = 0
    CON_NMETAL_ALTO = 0
    CON_METAL_BAIXA = 0
    CON_METAL_ALTO = 0
    AUXSTART = False
    AUXSENALTO = False
    AUXSENBAIXO = False
    AUXSENMETAL = False
    AUXFIM = False
    auxpeca=0
    result="nada"


  CON_TOTAL = CON_NMETAL_BAIXA + CON_NMETAL_ALTO + CON_METAL_BAIXA + CON_METAL_ALTO

  templateData = {
    'CON_TOTAL' : CON_TOTAL,
    'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
    'CON_NMETAL_ALTO' : CON_NMETAL_ALTO,
    'CON_METAL_BAIXA' : CON_METAL_BAIXA,
    'CON_METAL_ALTO' : CON_METAL_ALTO

  }
  return render_template('Automatico.html',**templateData)

### Pagina Automatico ###
@app.route('/Automatico')
def automatico():
  global START
  global EMERGENCIA
  global PECA
  global CON_NMETAL_BAIXA
  global CON_NMETAL_ALTO
  global CON_METAL_ALTO
  global CON_METAL_BAIXA
  global AUXSENALTO
  global AUXSENBAIXO
  global AUXSENMETAL
  global result

  CON_TOTAL = CON_NMETAL_BAIXA + CON_NMETAL_ALTO + CON_METAL_BAIXA + CON_METAL_ALTO

  templateData = {
    'CON_TOTAL' : CON_TOTAL,
    'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
    'CON_NMETAL_ALTO' : CON_NMETAL_ALTO,
    'CON_METAL_BAIXA' : CON_METAL_BAIXA,
    'CON_METAL_ALTO' : CON_METAL_ALTO

  }
  return render_template('Automatico.html',**templateData)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
