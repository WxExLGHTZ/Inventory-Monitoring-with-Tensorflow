#from Backend_Pakete.labelImg import *
#from Backend_Pakete.training_net import *
#from Backend_Pakete.database import *






# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# # ---------------------------------------------------------------------------------------------
# #  nur der folgende Code ist relevant für den Benutzer
# #---------------------------------------------------------------------------------------------




from Backend_Pakete.setup import *
#from Frontend_Pakete.real_sense_main import *


setup_obj = Setup()
setup_obj.setup_start()


# app = QApplication(sys.argv)
# main_window = MainWindow()
# main_window.show()
# sys.exit(app.exec_())



# #-------------------------------------------------------------------------------------------
# # der unten stehende Code ist für den Benutzer nicht notwendig
# #-------------------------------------------------------------------------------------------


# #-----------------------------------------------------------------
# #initialize objects
# #-----------------------------------------------------------------



#setup_obj = Setup()
#labelIm_obj = LabelImg()
#training_net_obj = TNet()




# #------------------------------------------------------------------
# #general Setup
# #------------------------------------------------------------------


#setup_obj.setup_start()


# #-------------------------------------------------------------------
# # start LabelImg for labeling
# #-------------------------------------------------------------------


#labelIm_obj.start_labeling()


##--------------------------------------------------------------------
## training and evaluation
##---------------------------------------------------------------------

# # Setup for training
#training_net_obj.setup()

# # train
#training_net_obj.train()

# # evaluate training
#training_net_obj.eval()


# # Tensorboard metrics (Tensorflow log files)

# #training metrics:
# #in cmd go to Tensorflow/workspace/models/my_ssd_mobilenet/train)
# #command: tensorboard --logdir=.

# evaluation metrics:
# in cmd go to Tensorflow/workspace/models/my_ssd_mobilenet/eval)
# command: tensorboard --logdir=.



##------------------------------------------------------------------------
## database delete all function
##-----------------------------------------------------------------------

#database_obj = Database()
# database_obj.delete_all("WarehouseStock")
# database_obj.delete_all("ErrorLog")




