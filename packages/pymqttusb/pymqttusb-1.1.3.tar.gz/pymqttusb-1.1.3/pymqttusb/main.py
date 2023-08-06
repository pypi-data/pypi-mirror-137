import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl
import base64
import random, string
import math
import json
import time
import sys
import serial
import threading
import getpass

if (len(sys.argv)>2):# la vitesse de communication peut-être donnée en 2ème argument
    baudRate = str(sys.argv[2])
    portSerie = str(sys.argv[1])
elif (len(sys.argv)== 2):
    portSerie = str(sys.argv[1])
    baudRate = 9600
else: 
    baudRate = 9600
    portSerie = "/dev/bus/usb/001/002"
  
# Opening JSON file 
try:
    file = open('arduino_mqtt_data.json',"r") 
except OSError:
    print('Le fichier de configuration \'arduino_mqtt_data.json\' n\'est pas présent dans votre répertoire !')
    exit()

# returns JSON object as a dictionary 
jsonconf = json.load(file) 
 
urlMqtt = jsonconf["broker_url"]  # url mqtt
portMqtt = jsonconf["broker_port"]   # port mqtt

salle = jsonconf["salle"]
KEY = jsonconf["KEY"]
broker_protocol = jsonconf["broker_protocol_mqtt_mqtts_ws_wss"]

#transport='websockets'    transport="tcp" pour ssl)
if (broker_protocol == "wss"):
    protocol = "websockets"
else:
    protocol = "tcp"

Username = input('Entrez votre identifiant MQTT : ') 
pwd = getpass.getpass('Entrez votre mot de passe MQTT :')

auth = {
    'username':Username,
    'password':pwd
}

#initialisation du port série
ser = serial.Serial()
ser.port = portSerie # le port de l'Arduino
ser.baudrate = baudRate
ser.timeout = 1 # attente pour lecture du port série avec readline()
ser.open() # ouverture du port
time.sleep(1)# temporisation nécessaire le temps que le port soit ouvert

if ser.is_open==True:
    print("\n Le port série \"",ser.port,"\" est ouvert !\n")
    print("Vitesse de communication : ",baudRate," bauds\n")
    #print(ser, "\n") # affiche la configuration du port série 

def serialEvent():
    while True:
        try:
            data = ser.readline().decode('utf-8').strip('\r\n')
            if ((client.connected_flag) and (data != "")):
                print("envoi : "+salle+"/"+KEY+"/out/ "+data)
                client.publish(salle+"/"+KEY+"/out/",payload=data,qos=0)
            #time.sleep(0.21)
        except serial.SerialTimeoutException:
            print('-- SerialTimeoutException in serialEvent main.py --- ', data)
            #break
        except:
            #pass
            print("en attente des données....")

# fonction qui retourne une chaine aléatoire
def randomword(length):
    lettresEtChiffres = string.ascii_letters + string.digits
    chaineAleatoire = ''.join((random.choice(lettresEtChiffres) for i in range(length)))
    return chaineAleatoire

tls = {
  #'ca_certs':"",
  'tls_version':ssl.PROTOCOL_TLSv1_2
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  if (rc ==0):
      client.connected_flag=True #set flag
      print("connexion MQTT effectuée.\n")
      client.subscribe(salle+"/"+KEY+"/in/")
      # à faire envoyer un signal à mqtt : client.publish(salle+"/"+KEY+"/out/",payload="{/"pymqttusb/":/"connexion établie/"}",qos=0)
  else :
      print("Problème de connexion, code : "+str(rc))
      client.connected_flag=False #set flag
  #print("flags "+str(flags))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = str(msg.payload.decode("utf-8"))
    print("réception : "+salle+"/"+KEY+"/in/ "+data)
    ser.write((data+"\n").encode())
    print(data.encode())
    #ser.write("{\"led1\":\"B\"}\n".encode())

client = mqtt.Client(
    client_id= randomword(8),
    clean_session=True,
    protocol=mqtt.MQTTv311,
    transport=protocol)    # transport="tcp" pour ssl transport='websockets' pour wss 
client.connected_flag=False
client.username_pw_set(username=auth["username"],password=auth["password"])
client.tls_set(tls_version=tls["tls_version"])
client.on_connect = on_connect
client.on_message = on_message
client.reconnect_delay_set(min_delay=3, max_delay=120) # reconnection après 3 s puis si échec après 6 s jusqu'à 120 s
client.connect(urlMqtt, portMqtt, 60)

t = threading.Thread(target=serialEvent)# lecture du port serie dans un thread
t.start()

client.loop_forever()
