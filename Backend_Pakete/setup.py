import os
from git import Repo
import shutil
import wget
from Backend_Pakete.variables import *



class Setup:

    def __init__(self):
        print("Setup object created")


    def setup_start(self):

        print("Setup begin")

        #creating image path
        IMAGES_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'collectedimages')

        if not os.path.exists(IMAGES_PATH):
            os.makedirs(IMAGES_PATH)

        if not os.path.exists(paths['RESULT_PATH']):
            os.makedirs('ResultOfRecognition')


        #Setup labelimg
        os.system('cmd /c "pip install --upgrade pyqt5 lxml"')

        LABELIMG_PATH = os.path.join('Tensorflow', 'labelimg')

        if not os.path.exists(LABELIMG_PATH):
            os.makedirs(LABELIMG_PATH)

            Repo.clone_from("https://github.com/tzutalin/labelImg", LABELIMG_PATH)

            print("cloned")

        print("current directory: " + os.getcwd())

        os.chdir("Tensorflow\labelimg")

        print("current directory: " + os.getcwd())

        os.system('cmd /c "pyrcc5 -o libs/resources.py resources.qrc"')

        os.chdir("..")
        os.chdir("..")

        for path in paths.values():
            if not os.path.exists(path):
                os.makedirs(path)

        print("step_1_done")



        #Setup for training and testing

        #clone Tensorflow Model Garden repo for using of the Tensorflow object-detection-API

        if not os.path.exists(os.path.join(paths['APIMODEL_PATH'], 'research', 'object_detection')):
            Repo.clone_from("https://github.com/tensorflow/models", paths['APIMODEL_PATH'])

        print("step_2_done")




        # Setup Protoc (Protocol Buffers)

        url = "https://github.com/protocolbuffers/protobuf/releases/download/v3.15.6/protoc-3.15.6-win64.zip"
        wget.download(url)

        print("current directory: " + os.getcwd())
        print("step_3_done")

        os.system('cmd /c "move protoc-3.15.6-win64.zip Tensorflow/protoc"')

        print("step_4_done")

        os.chdir(paths["PROTOC_PATH"])

        os.listdir(os.getcwd())

        print("step_5_done")
        print("current directory: " + os.getcwd())

        os.system('cmd /c "tar -xf protoc-3.15.6-win64.zip"')

        print("step_6_done")

        os.chdir("..")
        os.chdir("..")

        print("current directory: " + os.getcwd())


        # add path to 'bin' of protoc to PATH (environment variable)
        os.environ['PATH'] += os.pathsep + os.path.abspath(os.path.join("Tensorflow/protoc", 'bin'))

        print(os.environ['PATH'])
        print("step_7_done")

        os.chdir("Tensorflow/models/research")

        print("current directory: " + os.getcwd())

        os.system('cmd /c "protoc object_detection/protos/*.proto --python_out=. "')

        print("step_8_done")
        print("current directory: " + os.getcwd())




        #Setup Tensorflow Object detection API

        shutil.copy('object_detection/packages/tf2/Setup.py', os.getcwd())

        print("step_9_done")

        os.system('cmd /c "pip uninstall pillow -y"')
        os.system('cmd /c "pip install pillow"')

        os.system('cmd /c "pip uninstall tf_slim -y"')
        os.system('cmd /c "pip install tf_slim"')

        os.system('cmd /c "pip uninstall scipy -y"')
        os.system('cmd /c "pip install scipy"')

        os.system('cmd /c "pip uninstall tensorflow-io -y"')
        os.system('cmd /c "pip install tensorflow-io"')

        os.system('cmd /c "pip uninstall tf-models-official -y"')
        os.system('cmd /c "pip install tf-models-official"')

        os.system('cmd /c "pip install absl-py"')
        os.system('cmd /c "pip install pyyaml"')

        os.system('cmd /c "pip install tensorflow --upgrade"')
        os.system('cmd /c "pip uninstall protobuf matplotlib -y"')
        os.system('cmd /c "pip install protobuf matplotlib==3.2"')

        os.system('cmd /c "pip install pytz"')
        os.system("pip install gin-config==0.1.1")
        os.system("pip install tensorflow-addons")

        os.system("pip install pyodbc")

        os.system('cmd /c "pip list"')

        print("step_10_done")

        os.system('cmd /c "python Setup.py build"')

        print("step_11_done")

        print("current directory: " + os.getcwd())

        os.system('cmd /c "python Setup.py install"')

        print("step_12_done")

        print("current directory: " + os.getcwd())

        os.chdir("object_detection/builders")

        print("current directory: " + os.getcwd())



        # verificatin of proper insatllation of Tensorflow Object detection
        os.system('cmd /c python model_builder_tf2_test.py')


        # os.chdir("..")
        # os.chdir("..")
        # os.chdir("..")
        # os.chdir("..")
        # os.chdir("..")


        # os.system("pip install tensorflow==2.7.0 tensorflow-gpu==2.7.0") #optional if using GPU

        print("Setup successful")
