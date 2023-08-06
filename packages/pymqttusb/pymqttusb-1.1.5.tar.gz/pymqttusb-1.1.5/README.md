#pymqttusb

Permet la connexion d'un microprocesseur branché sur un port usb vers un serveur MQTT.<br />

Un fichier json de configuration "arduino_mqtt_data.json" doit être présent dans le répertoire.<br />
Contenu du fichier "arduino_mqtt_data.json" :<br />

{<br />
  "broker_url":"url_de_votre_broker_mqtt",<br />
  "broker_protocol_mqtt_mqtts_ws_wss":"wss",<br />
  "broker_port":443,<br />
  "salle":"maSalle",<br />
  "KEY":"bureau/lumiere1"<br />
}<br />
<br />
-----------<br />

Le topic de réception sera : salle/KEY/out<br />

Le topic d'envoi sera : salle/KEY/in<br />

Les protocoles possibles sont "wss" websockets sécurisés avec login et mot de passe ( pas de certificat)
ou "tcp" pour ssl avec login et mot de passe ( pas de certificats client) <br />

Lancement du programme :<br />

	En indiquant le nom du port usb (vitesse par défaut 9600 bauds)
	py -m pymqttusb.main com8 <br />

	En modifiant la vitesse de communication par défaut du port série :
	py -m pymqttusb.main com8 57600<br />
<br />

