import enum
import numpy as np

"""
RsTfObject soll als Transferklasse dazu dienen, das gemachte Bild in dieses Transferobjekt zu packen und das 
gesamte Transferobjekt an Tensorflow (recognition) zu übergeben, damit das Ergebnisbild (bisher result.png) als 
tfResultImage in diesem Transferobjekt abgelegt werden kann.
Ebenso kann die Auswertung (als Bild) in tfEvaluatedImage 
oder als 3x3 Matrix in storageRack abgelegt werden.
Noch zu prüfen: Bei der 3x3 Matrix dann EnumColor mit verwenden.
"""


class RsTfObject:
    def __init__(self, rs_image: object, timestamp: object) -> object:
        print("RsTfObject Konstruktor")
        # Foto der Kamera
        self.rs_image = rs_image
        # Suffix (Zeitstempel), der beim Speichern von Bildern ins Filesystem, an den Namen angehängt wird
        self.image_suffix = timestamp.strftime('%Y%m%d_%H%M%S')
        # Bild, das von Tensorflow gelabelt wird,
        # wird zurzeit nicht benutzt.
        self.tf_result_image = None
        # Bild, mit der Auswertung von Tensorflow
        # wird zurzeit nicht benutzt.
        self.tf_evaluated_image = None
        # 3x3 Matrix, um das Auswertungsergebnis von Tensorflow als Array zu übermitteln
        # wird gefüllt aber zurzeit nicht benutzt.
        self.storage_rack = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=np.int32)
        # Variable, um mögliche Fehlermeldung von Tensorflow weiterzugeben
        self.error_message = None
        # Zeiterfassung für die Analyse
        self.timestamp_start = timestamp

        self.timestamp_finish = None

    # Setter in recognition_net
    def set_tf_result_image(self, image):
        self.tf_result_image = image

    # Setter
    def set_tf_evaluated_image(self, image):
        self.tf_evaluated_image = image

    # Setter
    # def setErrorMessage(self, msg):
    #    self.errorMessage = msg

