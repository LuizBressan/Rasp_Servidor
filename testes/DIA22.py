from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
  12 : {'name' : 'atuador1', 'state' : GPIO.LOW} ,
  16 : {'name' : 'atuador2', 'state' : GPIO.LOW} ,
  8 : {'name' : 'esteira', 'state' : GPIO.LOW},
  10 : {'name' : 'esteira1', 'state' : GPIO.LOW} ,
  18 : {'name' : 'atuador3', 'state' : GPIO.LOW},
  22 : {'name' : 'atuador4', 'state' : GPIO.LOW} ,
}

for pin in pins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin,GPIO.LOW)
  GPIO.setwarnings(False)

GPIO.setwarnings(False)

###############ENTRADAS###############

SENBAIXO=11 #Sensor Peça baixa
SENALTO=23 #Sensor Peça Alta
SENMETAL=5 #Sensor Peça Metalica
SENPISTAO1=13 #Sensor Pistão 1
SENPISTAO2=15 #Sensor Pistão 2
SENPISTAO3=19 #Sensor Pistão 3
SENPISTAO4=21 #Sensor Pistão 4
SENFIMCURSO=29 #Sensor Fim de Curso

GPIO.setup(SENBAIXO,GPIO.IN)
GPIO.setup(SENALTO,GPIO.IN)
GPIO.setup(SENMETAL,GPIO.IN)
GPIO.setup(SENPISTAO1,GPIO.IN)
GPIO.setup(SENPISTAO2,GPIO.IN)
GPIO.setup(SENPISTAO3,GPIO.IN)
GPIO.setup(SENPISTAO4,GPIO.IN)
GPIO.setup(SENFIMCURSO,GPIO.IN)

################SAIDAS###############

PISTAO1=12 #SAIDA PISTÃO 1
PISTAO2=16 #SAIDA PISTÃO 2
PISTAO3=18 #SAIDA PISTÃO 3
PISTAO4=22 #SAIDA PISTÃO 4
ESTEIRA1=8 #SAIDA ESTEIRA 1
ESTEIRA2=10 #SAIDA ESTEIRA 2

GPIO.setup(PISTAO1,GPIO.OUT)
GPIO.setup(PISTAO2,GPIO.OUT)
GPIO.setup(PISTAO3,GPIO.OUT)
GPIO.setup(PISTAO4,GPIO.OUT)
GPIO.setup(ESTEIRA1,GPIO.OUT)
GPIO.setup(ESTEIRA2,GPIO.OUT)

app = Flask(__name__)


@app.route('/main')

def main():
       
  return render_template('PaginaPrincipal.html')


@app.route('/ModoDeEscolha')

def modo():
  
  return render_template('ModoDeEscolha.html')

@app.route('/Manual')

def manual():
  
  for pin in pins:
    pins[pin]['state'] = GPIO.input(pin)
  templateData = {
    'pins' : pins
    }
  return render_template('Manual.html', **templateData)

@app.route("/Manual/<changePin>/<action>")

def action(changePin, action):
  changePin = int(changePin)
  deviceName = pins[changePin]['name']
  
  if (action == "on"):
    GPIO.output(changePin,GPIO.HIGH)

  if (action == "off"):
    GPIO.output(changePin,GPIO.LOW)

  for pin in pins:
    pins[pin]['state'] = GPIO.input(pin)

  templateData = {
   # 'PISTAO1' : PISTAO1,
   # 'PISTAO2' : PISTAO2,
   # 'PISTAO3' : PISTAO3,
   # 'PISTAO4' : PISTAO4,
   # 'Peca' : PECA,
   # 'Esteira1' :ESTADOESTEIRA1,
    'pins' : pins
  }
    
  return render_template('Manual.html', **templateData)

@app.route('/Automatico')

def auto():

  ESTADOESTEIRA1 = "DESLIGADA"
  ESTADOESTEIRA2 = "DESLIGADA"
  PECA = "NENHUMA PECA NA ESTEIRA"
  CON_TOTAL = 0
  CON_NMETAL_BAIXA = 0
  CON_NMETAL_ALTA = 0
  CON_METAL_BAIXA = 0
  CON_METAL_ALTA = 0
  AUXSTART = False
  AUXSENALTO = False
  AUXSENBAIXO = False
  AUXSENMETAL = False
  
  CON_TOTAL = CON_NMETAL_BAIXA + CON_NMETAL_ALTA + CON_METAL_BAIXA + CON_METAL_ALTA
  
  if (GPIO.input(START)):
    AUXSTART=True
    
  if (GPIO.input(EMERGENCIA)):
    AUXSTART=False

  if (AUXSTART):
    
    GPIO.output(ESTEIRA1, GPIO.HIGH)

    if (GPIO.input(SENALTO)):
      AUXSENALTO=True

    if (GPIO.input(SENBAIXO)):
      AUXSENBAIXO=True

    if (GPIO.input(SENMETAL)):
      AUXSENMETAL=True

    if ((AUXSENBAIXO) and not(AUXSENALTO)and not(AUXSENMETAL)):
      PECA = "NAO METALICA BAIXA"

    elif ((AUXSENALTO) and not(AUXSENBAIXO) and not(AUXSENMETAL)):
      PECA = "NAO METALICA ALTA"

    elif (not(AUXSENALTO) and (AUXSENBAIXO) and (AUXSENMETAL)):
      PECA = "METALICA BAIXA"

    elif ((AUXSENALTO) and not (AUXSENBAIXO) and (AUXSENMETAL)):
      PECA = "METALICA ALTA"
      
  elif (not(AUXSTART)):

    AUXSTART=False      
    GPIO.output(ESTEIRA1, GPIO.LOW)
    GPIO.output(ESTEIRA2, GPIO.LOW)

  if(GPIO.input(SENFIMCURSO)):
        
    GPIO.output(ESTEIRA1, GPIO.LOW)
    time.sleep(3)
    GPIO.output(ESTEIRA2, GPIO.HIGH)
    
    
    if (PECA == "NAO METALICA BAIXA"):
      
      if(GPIO.input(SENPISTAO1)):
        GPIO.output(PISTAO1, GPIO.HIGH)
        CON_NMETAL_BAIXA = CON_NMETAL_BAIXA + 1
        time.sleep(1)
        GPIO.output(PISTAO1, GPIO.LOW)
        GPIO.output(ESTEIRA2, GPIO.LOW)
        
    elif (PECA == "NAO METALICA ALTA"):
      
      if(GPIO.input(SENPISTAO2)):
        GPIO.output(PISTAO2, GPIO.HIGH)
        CON_NMETAL_ALTO = CON_NMETAL_ALTO + 1
        time.sleep(1)
        GPIO.output(PISTAO2, GPIO.LOW)
        GPIO.output(ESTEIRA2, GPIO.LOW)
        
        
    elif (PECA == "METALICA BAIXA"):
      
      if(GPIO.input(SENPISTAO3)):
        GPIO.output(PISTAO3, GPIO.HIGH)
        CON_METAL_BAIXA = CON_METAL_BAIXA + 1
        time.sleep(1)
        GPIO.output(PISTAO3, GPIO.LOW)
        GPIO.output(ESTEIRA2, GPIO.LOW)

    elif (PECA == "METALICA ALTA"):
      
      if(GPIO.input(SENPISTAO4)):
        GPIO.output(PISTAO4, GPIO.HIGH)
        CON_METAL_ALTO = CON_METAL_ALTO + 1
        time.sleep(1)
        GPIO.output(PISTAO4, GPIO.LOW)
        GPIO.output(ESTEIRA2, GPIO.LOW)

  templateData = {
    'CON_TOTAL' : CON_TOTAL,
    'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
    'CON_NMETAL_ALTA' : CON_NMETAL_ALTA,
    'CON_METAL_BAIXA' : CON_METAL_BAIXA,
    'CON_METAL_ALTA' : CON_METAL_ALTA,
  }
    

  return render_template('Automatico.html',**templateData)



if __name__=="__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
