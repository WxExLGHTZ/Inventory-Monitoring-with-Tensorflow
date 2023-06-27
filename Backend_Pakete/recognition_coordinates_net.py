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
from matplotlib import pyplot as plt

import os.path
from Backend_Pakete.variables import *
from Backend_Pakete.visualisation_recognition import *
from Backend_Pakete.errormanager import *

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import sys


class RCoordinatesNet:
    def __init__(self):
        print("RCoordinatesNet object created")

    # recognize from Image and preprocess for vizualization
    def recognition_from_object(self, transfer_object, timestamp):

        #ts = timestamp

        if not os.path.exists(paths['RESULT_PATH']):
            raise SaveError

        print("recognition from transfer_object begin")

        # array that contains the color of detected objects at the correct position (3x3)
        lagerbestand = np.full((3, 3), 7, np.int32)
        y = 0
        x = 1

        # load pipeline config and build a detection model
        configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
        detection_model = model_builder.build(model_config=configs['model'], is_training=False)

        # restore checkpoint
        ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
        ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'],
                                  'ckpt-11')).expect_partial()  # last checkpoint: my_ssd_mobilenet

        # detection
        @tf.function
        def detect_fn(image):
            image, shapes = detection_model.preprocess(image)
            prediction_dict = detection_model.predict(image, shapes)
            tmp_detections = detection_model.postprocess(prediction_dict, shapes)
            return tmp_detections

        # detect from image
        image_np = np.array(transfer_object.rs_image)

        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

        try:
            detections = detect_fn(input_tensor)
        except:
            raise RecognitonError()

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        boxes = detections['detection_boxes']

        max_boxes_to_draw = boxes.shape[0]

        scores = detections['detection_scores']

        min_score_thresh = .8

        boxscore = 0

        # for loop through all coordinates for checking result of detection
        for i in range(min(max_boxes_to_draw, boxes.shape[0])):

            if scores is None or scores[i] > min_score_thresh:
                # detection_classes --> id (color) of Box
                # class_name = category_index[detections['detection_classes'][i]]['name']
                print("This box is gonna get used", boxes[i], detections['detection_classes'][i])
                # [ymin, xmin, ymax, xmax]
                boxscore += 1

        if boxscore != 9:
            raise ValueOfBoxesTooLow

        # lagerbestand [1],[1]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if i == 0:
                    x1y1 = boxes[i]
                if boxes[i][y] + 0.10 <= x1y1[y] and boxes[i][x] + 0.05 <= x1y1[x] \
                        or boxes[i][y] - 0.10 <= x1y1[y] and boxes[i][x] + 0.05 <= x1y1[x] \
                        or boxes[i][y] + 0.10 <= x1y1[y] and boxes[i][x] - 0.05 <= x1y1[x]\
                        or boxes[i][y] - 0.10 <= x1y1[y] and boxes[i][x] - 0.05 <= x1y1[x]:
                    lagerbestand[0][0] = detections['detection_classes'][i]
                    x1y1 = boxes[i]
                    lagerbestand1x1 = boxes[i]
                else:
                    if lagerbestand[0][0] == 7:
                        lagerbestand[0][0] = detections['detection_classes'][0]
                        lagerbestand1x1 = boxes[i]

        # lagerbestand [1],[3]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if i == 0:
                    x1y1 = boxes[i]
                if boxes[i][y] + 0.010 <= x1y1[y] and boxes[i][x] + 0.05 > x1y1[x]\
                        or boxes[i][y] - 0.010 <= x1y1[y] and boxes[i][x] + 0.05 > x1y1[x] \
                        or boxes[i][y] + 0.010 <= x1y1[y] and boxes[i][x] - 0.05 > x1y1[x] \
                        or boxes[i][y] - 0.010 <= x1y1[y] and boxes[i][x] - 0.05 > x1y1[x]:
                    lagerbestand[0][2] = detections['detection_classes'][i]
                    x1y1 = boxes[i]
                    lagerbestand1x3 = boxes[i]

                else:
                    if lagerbestand[0][2] == 7:
                        lagerbestand[0][2] = detections['detection_classes'][0]
                        lagerbestand1x3 = boxes[i]

        # lagerbestand [3],[1]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if i == 0:
                    x1y1 = boxes[i]
                if boxes[i][y] + 0.010 >= x1y1[y] and boxes[i][x] + 0.05 <= x1y1[x] \
                        or boxes[i][y] - 0.010 >= x1y1[y] and boxes[i][x] + 0.05 <= x1y1[x]\
                        or boxes[i][y] + 0.010 >= x1y1[y] and boxes[i][x] - 0.05 <= x1y1[x] \
                        or boxes[i][y] - 0.010 >= x1y1[y] and boxes[i][x] - 0.05 <= x1y1[x]:
                    lagerbestand[2][0] = detections['detection_classes'][i]
                    x1y1 = boxes[i]
                    lagerbestand3x1 = boxes[i]

                else:
                    if lagerbestand[2][0] == 7:
                        lagerbestand[2][0] = detections['detection_classes'][0]
                        lagerbestand3x1 = boxes[i]

        # lagerbestand [3],[3]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if i == 0:
                    x1y1 = boxes[i]
                if boxes[i][y] + 0.010 >= x1y1[y] and boxes[i][x] + 0.05 > x1y1[x] \
                        or boxes[i][y] - 0.010 >= x1y1[y] and boxes[i][x] + 0.05 > x1y1[x] \
                        or boxes[i][y] + 0.010 >= x1y1[y] and boxes[i][x] - 0.05 > x1y1[x] \
                        or boxes[i][y] - 0.010 >= x1y1[y] and boxes[i][x] - 0.05 > x1y1[x]:
                    lagerbestand[2][2] = detections['detection_classes'][i]
                    x1y1 = boxes[i]
                    lagerbestand3x3 = boxes[i]
                else:
                    if lagerbestand[2][2] == 7:
                        lagerbestand[2][2] = detections['detection_classes'][0]
                        lagerbestand3x3 = boxes[i]

        # lagerbestand [1],[2]
        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:

                if boxes[i][y] + 0.010 <= lagerbestand1x1[y] and boxes[i][x] > lagerbestand1x1[x] \
                        and boxes[i][x] < lagerbestand1x3[x] \
                        or boxes[i][y] - 0.010 <= lagerbestand1x1[y] and boxes[i][x] > lagerbestand1x1[x] \
                        and boxes[i][x] < lagerbestand1x3[x]:
                    lagerbestand[0][1] = detections['detection_classes'][i]
                    lagerbestand1x2 = boxes[i]

                else:
                    if lagerbestand[0][1] == 7:
                        lagerbestand[0][1] = detections['detection_classes'][0]
                        lagerbestand1x2 = boxes[i]

        # lagerbestand [3], [2]
        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if boxes[i][y] + 0.010 >= lagerbestand3x1[y] and boxes[i][x] > lagerbestand3x1[x] \
                        and boxes[i][x] < lagerbestand3x3[x] or boxes[i][y] - 0.010 >= lagerbestand3x1[y] \
                        and boxes[i][x] > lagerbestand3x1[x] and boxes[i][x] < lagerbestand3x3[x]:
                    lagerbestand[2][1] = detections['detection_classes'][i]
                    lagerbestand3x2 = boxes[i]
                else:
                    if lagerbestand[2][1] == 7:
                        lagerbestand[2][1] = detections['detection_classes'][0]
                        lagerbestand3x2 = boxes[i]

        # lagerbestand [2],[1]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if boxes[i][x] + 0.050 <= lagerbestand3x1[x] and boxes[i][y] > lagerbestand1x1[y] \
                        and boxes[i][y] < lagerbestand3x3[y] and boxes[i][y] != lagerbestand1x1[y] \
                        and boxes[i][y] != lagerbestand3x1[y] or boxes[i][x] - 0.050 <= lagerbestand3x1[x] \
                        and boxes[i][y] > lagerbestand1x1[y] and boxes[i][y] < lagerbestand3x3[y] \
                        and boxes[i][y] != lagerbestand1x1[y] and boxes[i][y] != lagerbestand3x1[y]:
                    lagerbestand[1][0] = detections['detection_classes'][i]
                    lagerbestand2x1 = boxes[i]

                else:
                    if lagerbestand[1][0] == 7:
                        lagerbestand[1][0] = detections['detection_classes'][0]
                        lagerbestand2x1 = boxes[i]

        # lagerbestand [2],[3]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if x1y1[x] < boxes[i][x] and boxes[i][x] + 0.050 >= lagerbestand3x3[x] \
                        and boxes[i][y] > lagerbestand1x3[y] and boxes[i][y] < lagerbestand3x3[y] \
                        and boxes[i][y] != lagerbestand1x3[y] and boxes[i][y] != lagerbestand3x3[y] \
                        or x1y1[x] < boxes[i][x] and boxes[i][x] - 0.050 >= lagerbestand3x1[x] \
                        and boxes[i][y] > lagerbestand1x1[y] and boxes[i][y] < lagerbestand3x3[y] \
                        and boxes[i][y] != lagerbestand1x3[y] and boxes[i][y] != lagerbestand3x3[y]:
                    lagerbestand[1][2] = detections['detection_classes'][i]
                    x1y1 = boxes[i]
                    lagerbestand2x3 = boxes[i]

                else:
                    if lagerbestand[1][2] == 7:
                        lagerbestand[1][2] = detections['detection_classes'][0]
                        lagerbestand2x3 = boxes[i]

        # lagerbestand [2],[2]

        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if boxes[i][y] < lagerbestand3x2[y] and boxes[i][y] > lagerbestand1x2[y] \
                        and boxes[i][x] > lagerbestand2x1[x] and boxes[i][x] < lagerbestand2x3[x] \
                        and boxes[i][x] != lagerbestand1x2[x] and boxes[i][x] != lagerbestand3x2[x]\
                        and boxes[i][x] != lagerbestand1x1[x] and boxes[i][x] != lagerbestand3x1[x] \
                        and boxes[i][x] != lagerbestand1x3[x] and boxes[i][x] != lagerbestand3x3[x]:
                    lagerbestand[1][1] = detections['detection_classes'][i]
                    lagerbestand2x2 = boxes[i]

                else:
                    if lagerbestand[1][1] == 7:
                        lagerbestand[1][1] = detections['detection_classes'][0]
                        lagerbestand2x2 = boxes[i]

        print("1/1: ", lagerbestand1x1)
        print("1/2: ", lagerbestand1x2)
        print("1/3: ", lagerbestand1x3)
        print("2/1: ", lagerbestand2x1)
        print("2/2: ", lagerbestand2x2)
        print("2/3: ", lagerbestand2x3)
        print("3/1: ", lagerbestand3x1)
        print("3/2: ", lagerbestand3x2)
        print("3/3: ", lagerbestand3x3)

        transfer_object.storage_rack = np.copy(lagerbestand)
        # Flip stock-array because the y-axis in the picture goes from top to bottom, but we want it from bottom to top
        lagerbestand = numpy.flip(lagerbestand)
        x = lagerbestand
        #print(x[0,0]) oben links
        #print(x[2,2]) unten links
        print(x)

        # Stock-array is filled and ready for visualization
        visualisation_obj = Visualisation()
        visualisation_obj.visualize_from_object(lagerbestand, transfer_object, timestamp)
