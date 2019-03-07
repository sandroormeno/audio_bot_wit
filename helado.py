# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import alsaaudio, wave, numpy
import os , time, datetime
#import speech_recognition as sr
from wit import Wit 
from os import path
import sys
#import json
reload(sys)
sys.setdefaultencoding("utf-8")


access_token = ""
client = Wit(access_token = access_token)

# Pins definitions
btn_pin = 4
#led_pin = 12

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(27, GPIO.OUT) # el led
GPIO.output(27, False)

helado = {"sabor" : None , "cantidad" : None}


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def wit_responde(mensaje, diccionario):
	entities = resp['entities']

	# actualiza los datos:
	if helado.get("sabor") == None:
		helado["sabor"] = first_entity_value(entities, 'sabor')
	if helado.get("cantidad") == None:
		helado["cantidad"] = first_entity_value(entities, 'cantidad')
		

	#helado["sabor"] = first_entity_value(entities, 'sabor')
	#helado["cantidad"] = first_entity_value(entities, 'cantidad')
	intent = first_entity_value(entities, 'intent')
	sabor = first_entity_value(entities, 'sabor')
	cantidad = first_entity_value(entities, 'cantidad')

	#print "--- " + str(resp['_text'])

	# pregunta por lo que falta

	if helado.get("sabor") == None:
		print "\n"
		print "Qué sabor quieres? \n"
		os.system("mpg123 -q sabor.mp3")
		print "----------------------------"
		print " Cuál sabor : " + str(helado.get("sabor"))
		print " Cuánto : " + str(helado.get("cantidad"))
		print "----------------------------"

	elif helado.get("cantidad") == None:
		print "\n"
		print "Cuantas bolas quieres? \n"
		os.system("mpg123 -q bolas.mp3")
		print "----------------------------"
		print " Cuál sabor : " + str(helado.get("sabor"))
		print " Cuánto : " + str(helado.get("cantidad"))
		print "----------------------------"
	else:
		print "\n"
		#print "Aquí tiene su helado de " +  str(helado.get("sabor")) +", que los drisfrute \n"
		responde = "Aquí tiene su helado de " +  str(helado.get("sabor")) +", que lo disfrute!"
		
		f = open("test.txt","w")
		f.write(" "+ str(responde))
		f.close()
		print "Aquí tiene su helado de " +  str(helado.get("sabor")) +", que lo disfrute! \n"
		#buscar_respuesta(responder)
		salida = "sudo python3 pyvona_lee_esto.py " 
		os.system(salida)
		helado["sabor"] = None
		helado["cantidad"] = None
		print "fin\n"

	#print " Qué quiere : " + str(intent)


activo = 0
prev_input = 0
try:
	while True:
		input = GPIO.input(4)
		if ((not prev_input) and input) and activo == 0:	
			inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
			inp.setchannels(1)
			inp.setrate(44100)
			#inp.setrate(8000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
			inp.setperiodsize(1024)
			w = wave.open('temp.wav', 'w')
			w.setnchannels(1)
			w.setsampwidth(2)
			w.setframerate(44100)
			#w.setframerate(8000)
			os.system("aplay --device=plughw:1,0 beep.wav -q")
			activo = 1
			print "...Grabando ..."
		if (GPIO.input(4) == True) and activo == 1:
			l, data = inp.read()
			w.writeframes(data)
		if (prev_input and not input):
			activo = 0
			time.sleep(1) #este delay impide error al enviar datos
			os.system("aplay --device=plughw:1,0 beep.wav -q") # -q permite ocultar la imformación de archivo
			print "...Enviando datos a Wit..."
			inp.close()
			w.close()
			AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp.wav")
			resp = None
			with open('temp.wav', 'rb') as f:
  				resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
	  		#responder = r.recognize_wit(audio, key=WIT_AI_KEY)
			#print "..."+ str(responder) + "...")
			wit_responde(resp, helado)
			#f = open("temp.txt","w")
			#f.write(" "+ str(responder))
			#f.close()
			#buscar_respuesta(responder)
			
			

			#os.system("sudo python3 habla.py")
			os.system("aplay --device=plughw:1,0 beep.wav -q") 

		prev_input = input	

# When you press ctrl+c, this will be called


except KeyboardInterrupt:
	GPIO.cleanup()