from Backend_Pakete.variables import *


class LabelImg:
    def __init__(self):
        print("LabelImg object created")

    def start_labeling(self):
        # start LabelImg
        os.system('cmd /c "python Tensorflow\labelimg\labelImg.py"')

