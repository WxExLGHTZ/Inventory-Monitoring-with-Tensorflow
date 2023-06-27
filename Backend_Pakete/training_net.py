import tarfile
import cv2
import uuid
import os
import time
import wget
from git import Repo
import shutil
import object_detection
from Backend_Pakete.variables import *


import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format


class TNet:

    def __init__(self):
        print("training_net object creaed")

    def setup(self):

        print("tarining_net Setup begin")

        # download pre traind model
        wget.download(PRETRAINED_MODEL_URL)  # download des models

        print("current directory: " + os.getcwd())

        os.system(
            'cmd /c "move ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8.tar.gz Tensorflow/workspace/pre-trained-models"')

        os.chdir("Tensorflow/workspace/pre-trained-models")

        os.system('cmd /c "tar -zxvf ssd_mobilenet_v1_fpn_640x640_coco17_tpu-8.tar.gz"')

        os.chdir("..")
        os.chdir("..")
        os.chdir("..")


        # create label map
        labels = [{'name': 'rot', 'id': 1}, {'name': 'blau', 'id': 2}, {'name': 'weiss', 'id': 3},
                  {'name': 'schwarz', 'id': 4}]

        with open(files['LABELMAP'], 'w') as f:
            for label in labels:
                f.write('item { \n')
                f.write('\tname:\'{}\'\n'.format(label['name']))
                f.write('\tid:{}\n'.format(label['id']))
                f.write('}\n')


        # create TF records
        if not os.path.exists(files['TF_RECORD_SCRIPT']):
            Repo.clone_from("https://github.com/nicknochnack/GenerateTFRecord", paths['SCRIPTS_PATH'])

        print("current directory: " + os.getcwd())

        os.system(
            "python " + "Tensorflow/scripts/generate_tfrecord.py " + "-x " + os.path.join('Tensorflow/workspace/images',
                                                                                          'train') + " -l " + "Tensorflow/workspace/annotations/label_map.pbtxt" + " -o " + os.path.join(
                'Tensorflow/workspace/annotations', 'train.record'))

        os.system(
            "python " + "Tensorflow/scripts/generate_tfrecord.py " + "-x " + os.path.join('Tensorflow/workspace/images',
                                                                                          'test') + " -l " + "Tensorflow/workspace/annotations/label_map.pbtxt" + " -o " + os.path.join(
                'Tensorflow/workspace/annotations', 'test.record'))



        # copy model config to training folder
        shutil.copy(os.path.join(paths['PRETRAINED_MODEL_PATH'], PRETRAINED_MODEL_NAME, 'pipeline.config'),
                    os.path.join(paths['CHECKPOINT_PATH']))


        # update config
        config = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])


        pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
        with tf.io.gfile.GFile(files['PIPELINE_CONFIG'], "r") as f:
            proto_str = f.read()
            text_format.Merge(proto_str, pipeline_config)

        pipeline_config.model.ssd.num_classes = len(labels)
        pipeline_config.train_config.batch_size = 4
        pipeline_config.train_config.fine_tune_checkpoint = os.path.join(paths['PRETRAINED_MODEL_PATH'],
                                                                         PRETRAINED_MODEL_NAME, 'checkpoint', 'ckpt-0')
        pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
        pipeline_config.train_input_reader.label_map_path = files['LABELMAP']
        pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [
            os.path.join(paths['ANNOTATION_PATH'], 'train.record')]
        pipeline_config.eval_input_reader[0].label_map_path = files['LABELMAP']
        pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [
            os.path.join(paths['ANNOTATION_PATH'], 'test.record')]

        config_text = text_format.MessageToString(pipeline_config)
        with tf.io.gfile.GFile(files['PIPELINE_CONFIG'], "wb") as f:
            f.write(config_text)

        print("tarining_net Setup done")






    #Training

    def train(self):

        print("training begin")

        TRAINING_SCRIPT = os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection', 'model_main_tf2.py')

        command = "python {} --model_dir={} --pipeline_config_path={} --num_train_steps=2000".format(TRAINING_SCRIPT,
                                                                                                     paths[
                                                                                                         'CHECKPOINT_PATH'],
                                                                                                     files[
                                                                                                         'PIPELINE_CONFIG'])

        #print(command)

        os.system(command)

        print("training done")



    # Evaluation of training

    def eval(self):

        print("evaluation begin")
        command_evaluate = "python {} --model_dir={} --pipeline_config_path={} --checkpoint_dir={}".format(TRAINING_SCRIPT,
                                                                                                           paths[
                                                                                                               'CHECKPOINT_PATH'],
                                                                                                           files[
                                                                                                               'PIPELINE_CONFIG'],
                                                                                                           paths[
                                                                                                               'CHECKPOINT_PATH'])

        #print(command_evaluate)
        os.system(command_evaluate)

        print("evaluation done")