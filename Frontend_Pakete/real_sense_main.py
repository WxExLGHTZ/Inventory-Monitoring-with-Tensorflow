"""
Letzte Aenderung 20.01.2022
"""
# import system Modul
import sys
import threading
# import PyQt5 Modul
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QTextCursor
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
# import Opencv Modul
import cv2
# import von realsense2
import pyrealsense2 as rs

# import von MainUI-File real_sense_main_form.py
from Frontend_Pakete.real_sense_main_form import *

# import von Pillow fürs allg. arbeiten mit Bildern.
from PIL import Image
from PIL.ImageQt import ImageQt
# import von datetime
from datetime import datetime
# import von logging
import logging
# import von Tensorflow internen Projekt
from Backend_Pakete.recognition_coordinates_net import *


def get_device_infos():
    print("get_device_infos begin")
    pipeline_wrapper = rs.pipeline_wrapper(rs.pipeline())
    pipeline_profile = rs.config().resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    print("device_product_line: ", str(device.get_info(rs.camera_info.product_line)))
    print("device_name: ", str(device.get_info(rs.camera_info.name)))
    print("device_firmware_version: ", str(device.get_info(rs.camera_info.firmware_version)))
    print("device_firmware_update_id: ", str(device.get_info(rs.camera_info.firmware_update_id)))
    print("device_product_id: ", str(device.get_info(rs.camera_info.product_id)))
    print("device_serial_number: ", str(device.get_info(rs.camera_info.serial_number)))
    print("device_physical_port: ", str(device.get_info(rs.camera_info.physical_port)))


class MainWindow(QWidget):
    # Konstruktor
    def __init__(self):
        # Aufruf des QWidget Konstruktors.
        super().__init__()
        # Lokale Variable für die GUI aus real_sense_main_form.py
        self.ui = Ui_RealSenseMainForm()
        # Methodenaufruf aus UI-Klasse.
        self.ui.setupUi(self)

        # Initialisieren des Control Timers.
        self.ctrlTimer = QTimer()
        # Läuft der Timer in der Methode control_timer los, wird Methode view_cam_start aufgerufen.
        self.ctrlTimer.timeout.connect(self.view_cam_start)
        # Variable nimmt Klick auf Button 'Kamera verbinden' entgegen. Aufrufen der Methode control_timer.
        self.ui.ctrl_camera_bt.clicked.connect(self.control_timer)

        # Initialisieren des Automatic Timers.
        self.automTimer = QTimer()
        # Läuft der Timer in der Methode automatic_timer los, wird Methode create_photo aufgerufen.
        self.automTimer.timeout.connect(self.create_photo)
        # Variable nimmt Klick auf Button 'Automatik starten' entgegen. Aufrufen der Methode automatic_timer.
        self.ui.ctrl_automatic_bt.clicked.connect(self.automatic_timer)

        # Klick auf Button 'Foto'
        self.ui.photo_bt.clicked.connect(self.create_photo)

        # Button sind anfangs deaktiviert.
        # self.ui.photo_bt.setEnabled(False)
        # self.ui.ctrl_automatic_bt.setEnabled(False)
        self.cam = None
        self.image = None
        # self.imageCount = 0
        self.automaticIsRunning = False

        self.ui.storage_rack_box.setVisible(False)
        self.ui.image_label.setVisible(True)
        self.ui.image_label.setScaledContents(True)

        # Entferne Label Beschriftung
        self.ui.video_label.clear()
        self.ui.image_label.clear()
        self.ui.wait_image_label.clear()
        self.ui.label_last_update.clear()
        self.ui.label_status_storacke_rack.clear()

        # animiertes Wait-Icon laden
        movie = QtGui.QMovie('Frontend_Pakete/loading2.gif')
        self.ui.wait_image_label.setMovie(movie)
        movie.start()
        # Wait-Icon-Label anfangs nicht sichtbar
        self.ui.wait_image_label.setVisible(False)
        # self.ui.wait_image_label.setGeometry(29, 500, 601, 71)

        # Setze Button -Bezeichnung und -Tooltips
        self.ui.ctrl_camera_bt.setText("Kamera verbinden")
        self.ui.ctrl_camera_bt.setToolTip("Startet die Verbindung zur angeschlossenen Kamera")
        self.ui.ctrl_automatic_bt.setText("Automatik starten")
        self.ui.ctrl_automatic_bt.setToolTip("Startet die Automatik, die in regelmäßigen Abstände Fotos macht")
        self.ui.photo_bt.setText("Foto machen")
        self.ui.photo_bt.setToolTip("Erstelle ein Foto, dass ausgewertet wird")

    # view_cam_start liest aus der gestarteten Kamera die Bilder aus und zeigt diese
    # auf der Oberfläche an.
    def view_cam_start(self):
        # Lesen der Kamera im BGR Format.
        ret, image = self.cam.read()
        # Konvertierung ind RGB Format, wird für die Anzeige auf der Oberflaeche benötigt.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Bestimmen der Metadaten des Images, erforderlich für die Umwandlung in ein qImage.
        height, width, channel = image.shape
        step = channel * width
        # Erstellen eines qImage aus der Variable 'image'.
        q_img = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # Zeige das erstellte qImg im VideoLabel auf der Oberfläche.
        # Umwandlung in qImage ist zur Ausgabe auf der Oberfläche im Label erforderlich.
        self.ui.video_label.setPixmap(QPixmap.fromImage(q_img))

    # Start und Stop der Kamera.
    def control_timer(self):
        # Der Timer wird beim Klicken auf den Button in der Oberfläche aktiviert und läuft los.
        if not self.ctrlTimer.isActive():
            print("control_timer not active. Start now")
            print("view_cam_start begin")
            # Herstellen der Kameraverbindung.
            if not self.cam:

                # verwenden wenn RealSense Kamera nicht verbunden --> Verwendung der WebCam
                self.cam = cv2.VideoCapture(0)

                # verwenden wenn RealSense Kamera angeschlossen
                #self.cam = cv2.VideoCapture(1)

            # Startet den Timer für Bildabfrage.
            self.ctrlTimer.start(20)
            # Aktivieren/Deaktivieren von Buttons.
            # self.ui.ctrl_automatic_bt.setEnabled(True)
            # self.ui.photo_bt.setEnabled(True)
            self.ui.ctrl_camera_bt.setText("Kamera trennen")
            self.ui.ctrl_camera_bt.setToolTip("Stoppt die Verbindung zur angeschlossenen Kamera")
        # Wenn diese Methode ein zweites Mal aufgerufen wird und der ctrlTimer aktiv ist und läuft,
        # wird direkt in des else - Zweig gesprungen und der Timer wird gestoppt.
        # Die Verbindung zu Kamera wird getrennt.
        else:
            # Stop des Timers
            print("control_timer is active. Stop now")
            self.ctrlTimer.stop()
            self.view_cam_stop()

    # Wenn view_cam_stop aufgerufen wird, wird die Verbindung der Kamera unterbrochen und Buttons deaktiviert.
    def view_cam_stop(self):
        print("view_cam_stop begin")
        self.cam.release()
        self.cam = None
        # self.ui.ctrl_automatic_bt.setEnabled(False)
        # self.ui.photo_bt.setEnabled(False)
        self.ui.ctrl_camera_bt.setText("Kamera verbinden")
        self.ui.ctrl_camera_bt.setToolTip("Startet die Verbindung zur angeschlossenen Kamera")
        self.ui.image_label.clear()
        self.ui.video_label.clear()
        self.ui.log_ausgabe.clear()

    # Speichern und Ausgabe des aufgenommenen Bildes.
    def create_photo(self):
        print("create_photo begin")
        # Suffix um Fotos mit untersch. Dateinamen zu speichern.
        timestamp = datetime.now()
        cam_should_closed = False
        if not self.cam:

            # verwenden wenn RealSense Kamera nicht verbunden --> Verwendung der WebCam
            self.cam = cv2.VideoCapture(0)

            # verwenden wenn RealSense Kamera angeschlossen
            #self.cam = cv2.VideoCapture(1)

            cam_should_closed = True
            print("create_photo open Cam")

        global TIMESTAMP
        TIMESTAMP = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Camera auslesen für ein Foto.
        return_value, image = self.cam.read()

        if cam_should_closed:
            self.cam.release()
            self.cam = None
            print("create_photo release Cam")

        # In der Logausgabe wird der Start einer neuen Erkennung dokumentiert. Vorher wird die Logausgabe geleert
        self.ui.log_ausgabe.clear()
        self.ui.log_ausgabe.append(datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ": Neue Erkennung gestartet")

        # In der Entwicklungsphase wird das Foto durch ein Testbild ersetzt, um eine Auswertung durch Tensorflow
        # zu ermöglichen
        image2 = cv2.imread("Testimage/test.png")
        print("call image_to_tensorflow:" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # self.image_to_tensorflow(image2, timestamp)

        # Parameter "image2" benutzen für lokal abgespeicherte Bilder
        t = threading.Thread(target=self.image_to_tensorflow, args=(image2, timestamp,))

        # Parameter "image" benutzen bei Verwendung von Bildern der RealSense kamera
        #t = threading.Thread(target=self.image_to_tensorflow, args=(image, timestamp,))

        t.start()

    # Ausgabe des gespeicherten Testbildes
    def load_picture_from_filesystem(self, path):
        print("load_picture_from_filesystem begin")

        if path == "" or not path:
            path = "Testimage/result.png"
        img = Image.open(path)
        qt_image = ImageQt(img)
        self.ui.image_label.setPixmap(QPixmap.fromImage(qt_image))

    # Start und Stop der Automatik.
    def automatic_timer(self):
        # Der Timer wird beim Klicken auf den Button in der Oberfläche aktiviert und läuft los.
        if not self.automTimer.isActive():
            print("automatic_timer not active. Start now")
            # Startet den Timer für automatische Bildabfrage.
            self.automaticIsRunning = True
            self.ui.photo_bt.setEnabled(False)
            # Erstes Foto direkt machen, dann Timer starten
            self.create_photo()
            # 2 Minuten = 120000 Millisekunden
            self.automTimer.start(120000)
            self.ui.ctrl_automatic_bt.setText("Automatik stoppen")
            self.ui.ctrl_automatic_bt.setToolTip("Stoppt die Automatik, die in regelmäßigen Abstände Photos macht")
        # Wenn diese Methode ein zweites Mal aufgerufen wird und der ctrlTimer aktiv ist und läuft,
        # wird direkt in des else - Zweig gesprungen und der Timer wird gestoppt.
        # Die Verbindung zu Kamera wird getrennt.
        else:
            # Stop des Timers
            print("automatic_timer is active. Stop now")
            self.automTimer.stop()
            self.automaticIsRunning = False
            self.ui.photo_bt.setEnabled(True)
            self.ui.ctrl_automatic_bt.setText("Automatik starten")
            self.ui.ctrl_automatic_bt.setToolTip("Startet die Automatik, die in regelmäßigen Abstände Photos macht")

# Bild an Tensorflow übergeben und auswerten lassen (Wird im extra Thread ausgeführt
    def image_to_tensorflow(self, image, timestamp):
        from Frontend_Pakete.rs_tf_object import RsTfObject

        print("image_to_tensorflow start:"+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.ui.wait_image_label.setVisible(True)
        transfer_obj = RsTfObject(image, timestamp)

        # Laden der RCoordinatesNet Klasse (Analyseklasse) von Tensorflow
        tf_recognition_coordinates_obj = RCoordinatesNet()

        try:
            # Aufruf der Auswertungsmethode der Analyseklasse, mit Übergabe des Transferobjektes
            tf_recognition_coordinates_obj.recognition_from_object(transfer_obj,TIMESTAMP)

            # Bilder aus dem Transferobjekt vorerst im Filesystem speichern
            # Bild zum auswerten
            if transfer_obj.rs_image is not None:
                cv2.imwrite("ResultOfRecognition/Bild_" + transfer_obj.image_suffix +
                            ".png", transfer_obj.rs_image)
            # gelabelten Ergebnisbild
            if transfer_obj.tf_result_image is not None:
                cv2.imwrite("ResultOfRecognition/Bild_" + transfer_obj.image_suffix +
                            "_Result.png", transfer_obj.tf_result_image)
            # generiertes Auswertungsbild
            if transfer_obj.tf_evaluated_image is not None:
                img_evaluated = Image.open(transfer_obj.tf_evaluated_image)
                img_evaluated.save("ResultOfRecognition/Bild_" + transfer_obj.image_suffix +
                                   "_Auswertung.png", format="png")
                qt_image = ImageQt(img_evaluated)
                self.ui.image_label.setPixmap(QPixmap.fromImage(qt_image))

            print("image_to_tensorflow done:" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # self.load_picture_from_filesystem(
            #    "ResultOfRecognition/Bild_" + transfer_obj.image_suffix + "_Auswertung.png")
            # self.showTfEvaluatedImage(transfer_obj.tfEvaluatedImage)
            transfer_obj.timestamp_finish = datetime.now()

            self.get_storage_rack_status(transfer_obj.storage_rack)
            #self.fill_storage_rackbox(transfer_obj.storage_rack)
            self.set_log_message("Lagerbestandserkennung erfolgreich ausgeführt!", False)
            #self.ui.label_last_update.setText("Zuletzt aktualisiert: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
            self.ui.label_last_update.setText("Zuletzt aktualisiert: " + TIMESTAMP)

        except RecognitonError:

            database_obj = Database()
            error = "ERROR: Erkennung fehlgeschlagen"
            database_obj.insert_data(TIMESTAMP, error)


            self.set_log_message(error, False)
            self.ui.image_label.clear()


        except SaveError:

            database_obj = Database()
            error = "ERROR: Kein Speicherort vorhanden"
            database_obj.insert_data(TIMESTAMP, error)

            self.set_log_message(error,False)
            self.ui.image_label.clear()



        except ValueOfBoxesTooLow:

            database_obj = Database()
            error = "ERROR: Lagerbestände nicht eindeutig erkennbar"
            database_obj.insert_data(TIMESTAMP, error)

            self.set_log_message(error,False)
            self.ui.image_label.clear()

        except DatabaseError:
            error = "ERROR: Verbindung zur Datenbank fehlgeschlagen"

            self.set_log_message(error,False)
            self.set_log_message("Lagerbestandserkennung erfolgreich ausgeführt!",False)

            if transfer_obj.rs_image is not None:
                cv2.imwrite("ResultOfRecognition/Bild_" + transfer_obj.image_suffix +
                            ".png", transfer_obj.rs_image)
                # gelabelten Ergebnisbild
            if transfer_obj.tf_result_image is not None:
                cv2.imwrite("ResultOfRecognition/Bild_" + transfer_obj.image_suffix +
                            "_Result.png", transfer_obj.tf_result_image)
                # generiertes Auswertungsbild
            if transfer_obj.tf_evaluated_image is not None:
                img_evaluated = Image.open(transfer_obj.tf_evaluated_image)
                img_evaluated.save("ResultOfRecognition/Bild_" + transfer_obj.image_suffix +
                                   "_Auswertung.png", format="png")
                qt_image = ImageQt(img_evaluated)
                self.ui.image_label.setPixmap(QPixmap.fromImage(qt_image))




        finally:
            self.ui.wait_image_label.setVisible(False)



    # Der übergebene Text wird im Log_Ausgabe_Label angehängt.
    # Image_Label wird entsprechend dem Übergabeparameter geleert.
    def set_log_message(self, msg, clean_imagelabel):
        message = datetime.now().strftime('%d-%m-%Y %H:%M:%S')+": "+msg
        print(message)
        self.ui.log_ausgabe.append(message)
        if clean_imagelabel:
            self.ui.image_label.clear()

    def get_storage_rack_status(self, stock_rack):
        cnt_blue = 0
        cnt_red = 0
        cnt_white = 0
        cnt_black = 0
        for i in range(len(stock_rack)):
            for j in range(len(stock_rack[i])):
                rack_value = stock_rack[i][j]
                if rack_value == 0:
                    cnt_red += 1

                if rack_value == 1:
                    cnt_blue += 1

                if rack_value == 2:
                    cnt_white += 1

                if rack_value == 3:
                    cnt_black += 1

        status = "Lagerbestand: "
        if cnt_red > 0:
            status += "rot:" + str(cnt_red) + " "

        if cnt_blue > 0:
            status += "blau:" + str(cnt_blue) + " "

        if cnt_white > 0:
            status += "weiss:" + str(cnt_white) + " "

        if cnt_black > 0:
            status += "leer:" + str(cnt_black)

        self.ui.label_status_storacke_rack.setText(status)
