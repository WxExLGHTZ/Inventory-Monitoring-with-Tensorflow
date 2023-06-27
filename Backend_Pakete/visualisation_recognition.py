import io
import tarfile
import cv2
import uuid
import os
import time

import numpy
import wget
from git import Repo
import shutil
import object_detection
import numpy as np
import matplotlib.pyplot as plt
import os.path
from datetime import datetime

from Backend_Pakete.variables import *
from Backend_Pakete.database import *



class Visualisation:

    def __init__(self):
        print("Visualisation start")

    # number in stock-array represents a color
    def set_color(self, color_num):
        if color_num == 1:
            return "blue"
        elif color_num == 3:
            return "black"
        elif color_num == 0:
            return "red"

    # visualize stock-array
    
    def visualize_from_object(self, lagerbestand, transfer_object, timestamp):



        circle_size = 0.3
        cross_size =1800

        # coordinates of each compartment of the stock in the output graphics

        a3 = ""
        pos_0_2_x = 2.5
        pos_0_2_y = 0.5

        a2 = ""
        pos_0_1_x = 1.5
        pos_0_1_y = 0.5

        a1 = ""
        pos_0_0_x = 0.5
        pos_0_0_y = 0.5

        b3 = ""
        pos_1_2_x = 2.5
        pos_1_2_y = 1.5

        b2 = ""
        pos_1_1_x = 1.5
        pos_1_1_y = 1.5

        b1 = ""
        pos_1_0_x = 0.5
        pos_1_0_y = 1.5

        c3 = ""
        pos_2_2_x = 2.5
        pos_2_2_y = 2.5

        c2 = ""
        pos_2_1_x = 1.5
        pos_2_1_y = 2.5

        c1 = ""
        pos_2_0_x = 0.5
        pos_2_0_y = 2.5

        fig, ax = plt.subplots()

        # Axes of the output graphics
        ax.set(xlim=(0, 3), ylim=(0, 3))

        horizontal_line = plt.axhline(1)
        vertical_line = plt.axvline(1)
        horizontal_line2 = plt.axhline(2)
        vertical_line2 = plt.axvline(2)

        circle = None
        cross = None

        # for each position in stock-array add correct object with correct color to correct position in output graphics
        for i in range(3):

            for j in range(3):

                if i == 0 and j == 0:
                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_0_2_x, pos_0_2_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            a3 = "RED"
                        else:
                            a3 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_0_2_x, pos_0_2_y),
                                            circle_size, color='black', fill=False)

                        a3 = "WHITE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_0_2_x, pos_0_2_y, c='black', s=cross_size, marker='x')

                        a3 ="EMPTY"

                        ax.add_artist(cross)

                if i == 0 and j == 1:
                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_0_1_x, pos_0_1_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))
                        if (lagerbestand[i][j] == 0):
                            a2 = "RED"
                        else:
                            a2 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_0_1_x, pos_0_1_y),
                                            circle_size, color='black', fill=False)

                        a2 = "WHITE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_0_1_x, pos_0_1_y, c='black', s=cross_size, marker='x')

                        a2 = "EMPTY"
                        ax.add_artist(cross)

                if i == 0 and j == 2:
                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_0_0_x, pos_0_0_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            a1 = "RED"
                        else:
                            a1 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_0_0_x, pos_0_0_y),
                                            circle_size, color='black', fill=False)

                        a1 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_0_0_x, pos_0_0_y, c='black', s=cross_size, marker='x')

                        a1 = "EMPTY"
                        ax.add_artist(cross)

                if i == 1 and j == 0:

                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_1_2_x, pos_1_2_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            b3 = "RED"
                        else:
                            b3 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_1_2_x, pos_1_2_y),
                                            circle_size, color='black', fill=False)

                        b3 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_1_2_x, pos_1_2_y, c='black', s=cross_size, marker='x')

                        b3 = "EMPTY"
                        ax.add_artist(cross)

                if i == 1 and j == 1:

                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_1_1_x, pos_1_1_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            b2 = "RED"
                        else:
                            b2 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_1_1_x, pos_1_1_y),
                                            circle_size, color='black', fill=False)

                        b2 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_1_1_x, pos_1_1_y, c='black', s=cross_size, marker='x')

                        b2 = "EMPTY"
                        ax.add_artist(cross)

                if i == 1 and j == 2:

                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_1_0_x, pos_1_0_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            b1 = "RED"
                        else:
                            b1 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_1_0_x, pos_1_0_y),
                                            circle_size,  color='black', fill=False)

                        b1 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_1_0_x, pos_1_0_y, c='black', s=cross_size, marker='x')

                        b1 = "EMPTY"
                        ax.add_artist(cross)

                if i == 2 and j == 0:

                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_2_2_x, pos_2_2_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            c3 = "RED"
                        else:
                            c3 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_2_2_x, pos_2_2_y),
                                            circle_size,  color='black', fill=False)

                        c3 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_2_2_x, pos_2_2_y, c='black', s=cross_size, marker='x')

                        c3 = "EMPTY"
                        ax.add_artist(cross)

                if i == 2 and j == 1:

                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_2_1_x, pos_2_1_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            c2 = "RED"
                        else:
                            c2 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_2_1_x, pos_2_1_y),
                                            circle_size, color='black', fill=False)

                        c2 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_2_1_x, pos_2_1_y, c='black', s=cross_size, marker='x')

                        c2 = "EMPTY"
                        ax.add_artist(cross)

                if i == 2 and j == 2:

                    if lagerbestand[i][j] == 0 or lagerbestand[i][j] == 1:
                        circle = plt.Circle((pos_2_0_x, pos_2_0_y),
                                            circle_size, color=self.set_color(lagerbestand[i][j]))

                        if (lagerbestand[i][j] == 0):
                            c1 = "RED"
                        else:
                            c1 = "BLUE"

                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 2:
                        circle = plt.Circle((pos_2_0_x, pos_2_0_y),
                                            circle_size, color='black', fill=False)

                        c1 = "WHITE"
                        ax.add_artist(circle)
                    elif lagerbestand[i][j] == 3:
                        cross = plt.scatter(pos_2_0_x, pos_2_0_y, c='black', s=cross_size, marker='x')

                        c1 = "EMPTY"
                        ax.add_artist(cross)





        plt.axis('off')

        # safe result
        # result_name = "Bild_" + transfer_object.image_suffix + "_Auswertung.png"
        # plt.savefig(os.path.join(paths['RESULT_PATH'], result_name))
        # Das erstellte Auswertungsbild, wird jetzt über das TransferObjekt an die MainForm zurückgegeben
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        transfer_object.set_tf_evaluated_image(img_buf)

        database_obj = Database()
        error = "Lagerbestandserkennung erfolgreich ausgeführt!"
        database_obj.insert_data(timestamp, error, a1, a2, a3, b1, b2, b3, c1, c2, c3)

