from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#ENTRADAS

START=8 #Botão de inicio
SENBAIXO=10 #Sensor Peça baixa
SENALTO=12 #Sensor Peça Alta
SENMETAL=16 #Sensor Peça Metalica
EMERGENCIA=18 #Botão de Emergencia
SENPISTAO1=22 #Sensor Pistão 1
SENPISTAO2=24 #Sensor Pistão 2
SENPISTAO3=26 #Sensor Pistão 3
SENPISTAO4=32 #Sensor Pistão 4
SENFIMCURSO=36 #Sensor Fim de Curso



GPIO.setup(START,GPIO.IN)
GPIO.setup(EMERGENCIA,GPIO.IN)
GPIO.setup(SENBAIXO,GPIO.IN)
GPIO.setup(SENALTO,GPIO.IN)
GPIO.setup(SENMETAL,GPIO.IN)
GPIO.setup(SENPISTAO1,GPIO.IN)
GPIO.setup(SENPISTAO2,GPIO.IN)
GPIO.setup(SENPISTAO3,GPIO.IN)
GPIO.setup(SENPISTAO4,GPIO.IN)
GPIO.setup(SENFIMCURSO,GPIO.IN)

#SAIDAS

PISTAO1=11 #SAIDA PISTÃO 1
PISTAO2=13 #SAIDA PISTÃO 2
PISTAO3=15 #SAIDA PISTÃO 3
PISTAO4=19 #SAIDA PISTÃO 4
ESTEIRA1=21 #SAIDA ESTEIRA 1
ESTEIRA2=23 #SAIDA ESTEIRA 2

GPIO.setup(PISTAO1,GPIO.OUT)
GPIO.setup(PISTAO2,GPIO.OUT)
GPIO.setup(PISTAO3,GPIO.OUT)
GPIO.setup(PISTAO4,GPIO.OUT)
GPIO.setup(ESTEIRA1,GPIO.OUT)
GPIO.setup(ESTEIRA2,GPIO.OUT)

@app.route("/")


def main():
  

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
    GPIO.output(ESTEIRA2, GPIO.HIGH)
    ESTADOESTEIRA1 = "LIGADA"
    ESTADOESTEIRA2 = "LIGADA"

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
    ESTADOESTEIRA1="DESLIGADA"
    ESTADOESTEIRA2="DESLIGADA"

  if(GPIO.input(SENFIMCURSO)):
        
    GPIO.output(ESTEIRA1, GPIO.LOW)
    GPIO.output(ESTEIRA2, GPIO.LOW)
    time.sleep(3)
    GPIO.output(ESTEIRA1, GPIO.HIGH)
    GPIO.output(ESTEIRA2, GPIO.HIGH)
    
    
    if (PECA == "NAO METALICA BAIXA"):
      
      if(GPIO.input(SENPISTAO1)):
        GPIO.output(PISTAO1, GPIO.HIGH)
        PISTAO1="PISTAO ACIONADO"
        CON_NMETAL_BAIXA = CON_NMETAL_BAIXA + 1
        time.sleep(1)
        GPIO.output(PISTAO1, GPIO.LOW)
        PISTAO1="PISTAO DESACIONADO"
        
    elif (PECA == "NAO METALICA ALTA"):
      
      if(GPIO.input(SENPISTAO2)):
        GPIO.output(PISTAO2, GPIO.HIGH)
        PISTAO2="PISTAO ACIONADO"
        CON_NMETAL_ALTO = CON_NMETAL_ALTO + 1
        time.sleep(1)
        GPIO.output(PISTAO2, GPIO.LOW)
        PISTAO2="PISTAO DESACIONADO"
        
        
    elif (PECA == "METALICA BAIXA"):
      
      if(GPIO.input(SENPISTAO3)):
        GPIO.output(PISTAO3, GPIO.HIGH)
        PISTAO3="PISTAO ACIONADO"
        CON_METAL_BAIXA = CON_METAL_BAIXA + 1
        time.sleep(1)
        GPIO.output(PISTAO3, GPIO.LOW)
        PISTAO3="PISTAO DESACIONADO"

    elif (PECA == "METALICA ALTA"):
      
      if(GPIO.input(SENPISTAO4)):
        GPIO.output(PISTAO4, GPIO.HIGH)
        PISTAO4="PISTAO ACIONADO"
        CON_METAL_ALTO = CON_METAL_ALTO + 1
        time.sleep(1)
        GPIO.output(PISTAO4, GPIO.LOW)
        PISTAO4="PISTAO DESACIONADO"


  templateData = {
    'CON_TOTAL' : CON_TOTAL,
    'CON_NMETAL_BAIXA' : CON_NMETAL_BAIXA,
    'CON_NMETAL_ALTA' : CON_NMETAL_ALTA,
    'CON_METAL_BAIXA' : CON_METAL_BAIXA,
    'CON_METAL_ALTA' : CON_METAL_ALTA,
    #'PISTAO1' : PISTAO1,
    #'PISTAO2' : PISTAO2,
    #'PISTAO3' : PISTAO3,
    #'PISTAO4' : PISTAO4,
    'Peca' : PECA,
    'Esteira1' :ESTADOESTEIRA1,
    'Esteira2' :ESTADOESTEIRA2,
    #'mensagem' : mensagem,
    #'mensagem1' : mensagem1
  }
  
  return render_template('PaginaPrincipal.html',**templateData)
        

if __name__ == "__main__":

  app.run(host='0.0.0.0',port=80,debug=True)





