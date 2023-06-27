Lagerbestandserfassung mithilfe von Neuronalen Netzen

Teammitglieder:

Mert Karadeniz s0569367

Viktor Kruckow s0569025

William Eppel s0570986

Semester: WS21/22

Eine Software um ein Lagerbestand auszulesen mithilfe von Neuronalen Netzen

	-Achtung: Das Netz ist auf eine bestimmte Art von Lager und bestimmte Objekte trainiert.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Vorbereitung:
1. Installieren Sie PyCharm (entwickelt mit: PyCharm Community Edition) 

2. Installieren Sie Python 3.8.x 

	-Achtung: getestet mit Python 3.8.0 & Python 3.8.10

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Installation:
1. Klonen Sie sich das repository in ein Verzeichnis Ihrer Wahl

2. Legen Sie sich eine eigene virtuelle Umgebung an. So werden alle Bibliotheken in die virtuelle Umgebung runtergeladen und abgespeichert.

	1. Öffnen Sie die Kommandozeile als Administrator
	2. Navigieren Sie in das Verzeichnis, welches Sie im vorherigen Schritt gecloned haben
	3. geben Sie den folgenden Befehl zum erstellen einer virtuellen Umgebung ein:

			{path to python.exe} -m venv venv

		Achtung: das letzte venv steht für den Namen der virtuellen Umgebung, dieser ist frei wählbar, muss aber im folgenden Verlauf benutzt werden

		Achtung: {path to python.exe} => hier muss der komplette Pfad zu Ihrer python Installation angegeben werden (ohne Klammern)

		Achtung: falls Sie nur eine Python Version auf Ihrem System installiert haben können Sie stattdessen auch folgenden Befehl benutzen:

			python -m venv venv
	
3. Aktivieren Sie Ihre virtuelle Umgebung (# Windows)

		.\venv\Scripts\activate

	Achtung: Um eine virtuelle Umgebung zu schließen benutzen Sie 'deactivate'
 

4. Installieren Sie die folgenden dependencies:

	Achtung: geben Sie die Befehle nacheinander in die Kommandozeile ein

		1.python -m pip install --upgrade pip

		2.pip install opencv-python

		3.pip install wget

		4.pip install gitpython

		5.pip install pyrealsense2


5. Öffnen Sie den Projektordner in Pycharm


6. Wählen Sie den für dieses Projekt erstellten Python Interpreter

	Achtung: der Pfad zum Interpreter ist: /venv/Scripts/Python.exe

7. Wählen Sie den Eintiegspunkt der Run/Debug configuration aus

	Achtung: Wählen Sie main.py als Einstiegspunkt aus

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Die Software ist standardmäßig so eingestellt, dass zuerst das Setup ausgeführt wird. 


Ausführung der Software:

1. Drücken Sie auf Run'main'



Nach erfolgreichem Abschluss des Setups muss folgendes in der **main.py** getan werden:

	1. Kommentieren Sie from Backend_Pakete.setup import * aus
	2. Kommentieren Sie setup_obj = Setup() aus
	3. Kommentieren Sie setup_obj.setup_start() aus 

	4. Kommentieren Sie from Frontend_Pakete.real_sense_main import *  ein
	5. Kommentieren Sie app = QApplication(sys.argv) ein
	6. Kommentieren Sie main_window = MainWindow() ein
	7. Kommentieren Sie main_window.show() ein
	8. Kommentieren Sie sys.exit(app.exec_()) ein 


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Für das Testen der Erkennungsfunktion des neuronalen Netzes muss sich ein Testbild im folgenden Ordner befinden:

	\Testimage\test.png

	Achtung: standardmäßig befindet sich bereits ein Testbild im genannten Verzeichnis. 

	Achtung: in der HTW Cloud befinden sich zusätzliche Bilder, die für das Testen verwendet werden können.
			
			 https://cloud.htw-berlin.de/f/126370598  

	Achtung: Falls ein anderes Bild, statt dem standardmäßig ausgewähltem Bild, verwendet werden soll, muss dieses in test umbennant werden und die Dateinamenserweiterung .png besitzen.

	Achtung: alle Bilder in https://cloud.htw-berlin.de/f/126370598 werden korrekt erkannt.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



Möchten Sie NICHT das Testbild aus dem Testimage Ordner verwenden, sondern die RealSense Kamera bei der Erkennung des Lagerbestandes nutzen, muss folgendes getan werden:

	1. Öffnen sie Frontend_Pakete/real_sense_main.py


	2. Gehen Sie zu der Methode def control_timer(self):  (Zeile: 125)

	3. Kommentieren Sie self.cam = cv2.VideoCapture(0) aus  (Zeile: 134)
	4. Kommentieren Sie self.cam = cv2.VideoCapture(1) ein  (Zeile: 137)


	5. Gehen Sie zu der Methode def create_photo(self):  (Zeile: 169 )

	6. Kommentieren Sie self.cam = cv2.VideoCapture(0) aus  (Zeile: 177)
	7. Kommentieren Sie self.cam = cv2.VideoCapture(1) ein  (Zeile: 180)
	8. Kommentieren Sie t = threading.Thread(target=self.image_to_tensorflow, args=(image2, timestamp,)) aus  (Zeile: 207)
	9. Kommentieren Sie t = threading.Thread(target=self.image_to_tensorflow, args=(image, timestamp,)) ein  (Zeile: 210)




-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Tensorboard von Training

	-in cmd, im env, in Tensorflow/workspace/models/my_ssd_mobilenet/train
	-tensorboard --logdir=.
	

Tensorboard von Evaluation
	
	-in cmd, im env, in Tensorflow/workspace/models/my_ssd_mobilenet/eval
	-tensorboard --logdir=.
	

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Benutzung:

1) Drücke Sie auf "Kamera verbinden"

--> Das Programm startet die Web-cam, da standardmäßig keine Verbindung zu der RealSense Kamera besteht.

--> Nach dem Drücken von "Kamera verbinden" wird die Schaltfläche "Photo machen" aktiv 

2) Drücken Sie auf "Photo machen"
--> Das Program lädt standardmäßig das Testbild aus dem Ordner "/Testimage"

3) Das Ergebnis der Erkennung erscheint auf der Benutzeroberfläche und wird in "/ResultOfRecognition" gespeichert

4) Der erkannte Lagerbestand wird mit den dazugehörigen Logdaten in der Datenbank abgespeichert (Verbindung in: database.py)
