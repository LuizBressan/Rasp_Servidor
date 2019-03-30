from flask import Flask, render_template, jsonify, json
import datetime
import time
import RPi.GPIO as gpio
app = Flask(__name__)

gpio.setmode(gpio.BOARD)

pins = {
  12 : {'name' : 'atuador1', 'state' : gpio.LOW} ,
  16 : {'name' : 'atuador2', 'state' : gpio.LOW} ,
  8  : {'name' : 'esteira', 'state' : gpio.LOW} ,
  10 : {'name' : 'esteira2', 'state' : gpio.LOW} ,
  18 : {'name' : 'atuador3', 'state' : gpio.LOW},
  22 : {'name' : 'atuador4', 'state' : gpio.LOW} ,
}
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
  print('Passou')
  if (START==True):
    print ("START")
    gpio.output(8,gpio.HIGH)
    gpio.output(10,gpio.HIGH)

    if (sensorAlto==True):
      AUXSENALTO=True
      print ("Alto")

    if (sensorBaixo==True):
      AUXSENBAIXO=True
      print ("Baixo")

    if (sensorMetalico==True):
      AUXSENMETAL=True
      print ("Metal")

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
    print(PECA)
      
  if (START==False):
      
    gpio.output(8, gpio.LOW)
    gpio.output(10, gpio.LOW)
    AUXFIM=0
    auxpeca=0
    PECA = "NENHUMA PECA NA ESTEIRA"
    AUXSENALTO=False
    AUXSENBAIXO=False
    AUXSENMETAL=False

  if(sensorFim==True):
    print ("Fim")
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
  


@app.route('/')
def main():
  return render_template('PaginaPrincipal.html')


@app.route('/ModoDeEscolha')
def modo():
  return render_template('ModoDeEscolha.html')

@app.route('/Manual')
def manual():
  sensorAlto=gpio.input(7)
  sensorBaixo=gpio.input(11)
  sensorMetalico=gpio.input(23)
  sensorFim=gpio.input(29)
  sensorAltoNaoMetalico=gpio.input(13)
  sensorAltoMetalico=gpio.input(15)
  sensorBaixoNaoMetalico=gpio.input(19)
  sensorBaixoMetalico=gpio.input(21)


  #teste Alto
  if sensorAlto==True :
    sA="alto"
  else:
    sA="desligado"

   #teste baixo
  if sensorBaixo==True :
    sB="baixo"
  else:
    sB="desligado"

    #teste metalico
  if sensorMetalico==True :
    sM="metal"
  else:
    sM="desligado"

    #teste fim
  if sensorFim==True :
    sF="fim"
  else:
    sF="desligado"

#teste Alto nao metalico
  if sensorAltoNaoMetalico==True :
    sAN="altoNaoMetalico"

  else:
    sAN="desligado"
#teste baixo n metalico
  if sensorBaixoNaoMetalico==True :
    sBN="baixoNaoMetalico"

  else:
    sBN="desligado"

    #teste Alto metalico
  if sensorAltoMetalico==True :
    sAM="altoMetalico"

  else:
    sAM="desligado"

#teste baixo metalico
  if sensorBaixoMetalico==True :
    sBM="baixoMetalico"

  else:
    sBM="desligado"

  for pin in pins:
    pins[pin]['state'] = gpio.input(pin)
  templateData = {
    'pins' : pins,
    'sB': sB,
    'sA' : sA,
    'sM' : sM,
    'sF' : sF,
    'sBM': sBM,
    'sAM' : sAM,
    'sBN': sBN,
    'sAN' : sAN
    
  
    }
    
  return render_template('Manual.html', **templateData)

@app.route("/Manual/<changePin>/<action>")
def action(changePin, action):
  sensorAlto=gpio.input(7)
  sensorBaixo=gpio.input(11)
  sensorMetalico=gpio.input(23)
  sensorFim=gpio.input(29)
  sensorAltoNaoMetalico=gpio.input(13)
  sensorAltoMetalico=gpio.input(15)
  sensorBaixoNaoMetalico=gpio.input(19)
  sensorBaixoMetalico=gpio.input(21)
  changePin = int(changePin)
  if action == "on":
    gpio.output(changePin,gpio.HIGH)

  if action == "off":
    gpio.output(changePin,gpio.LOW)
  

  if action == "toggle":
    gpio.output(changePin,not gpio.input(changePin))
    

  for pin in pins:
    pins[pin]['state'] = gpio.input(pin)

  if sensorAlto==True :
    sA="alto"

  else:
    sA="desligado"
  if sensorBaixo==True :
    sB="baixo"
  else:
    sB="desligado"
  if sensorMetalico==True :
    sM="metal"
  else:
    sM="desligado"
  if sensorFim==True :
    sF="fim"
  else:
    sF="desligado"
 #teste Alto nao metalico
  if sensorAltoNaoMetalico==True :
    sAN="altoNaoMetalico"

  else:
    sAN="desligado"
#teste baixo n metalico
  if sensorBaixoNaoMetalico==True :
    sBN="baixoNaoMetalico"

  else:
    sBN="desligado"

    #teste Alto metalico
  if sensorAltoMetalico==True :
    sAM="altoMetalico"

  else:
    sAM="desligado"

#teste baixo metalico
  if sensorBaixoMetalico==True :
    sBM="baixoMetalico"

  else:
    sBM="desligado"

  

  templateData = {
  'pins': pins,
  'sB': sB,
  'sA' : sA,
  'sM' : sM,
  'sF' : sF,
  'sBM': sBM,
  'sAM' : sAM,
  'sBN': sBN,
  'sAN' : sAN
  }

  return render_template('Manual.html', **templateData)

@app.route('/Automatico')
def auto():
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

  

  CON_TOTAL = CON_NMETAL_BAIXA + CON_NMETAL_ALTO + CON_METAL_BAIXA + CON_METAL_ALTO
  
  templateData = {
    'CON_TOTAL' : CON_TOTAL,
    'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
    'CON_NMETAL_ALTO' : CON_NMETAL_ALTO,
    'CON_METAL_BAIXA' : CON_METAL_BAIXA,
    'CON_METAL_ALTO' : CON_METAL_ALTO
    
  }
  return render_template('Automatico.html',**templateData)
@app.route('/Automatico/<algo>')
def autom(algo):
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

  if (algo=="inicio"):
    START=True
    rodar()

  if (algo=="emerg"):
    START=False
    rodar()



  CON_TOTAL = CON_NMETAL_BAIXA + CON_NMETAL_ALTO + CON_METAL_BAIXA + CON_METAL_ALTO
  
  templateData = {
    'CON_TOTAL' : CON_TOTAL,
    'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
    'CON_NMETAL_ALTO' : CON_NMETAL_ALTO,
    'CON_METAL_BAIXA' : CON_METAL_BAIXA,
    'CON_METAL_ALTO' : CON_METAL_ALTO,
    'sensorAT1': sensorAT1,
    'sensorAT2': sensorAT2,
    'sensorAT3': sensorAT3,
    'sensorAT4': sensorAT4
    
  }
  return render_template('Automatico.html',**templateData)

  
  



  
if __name__=="__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
