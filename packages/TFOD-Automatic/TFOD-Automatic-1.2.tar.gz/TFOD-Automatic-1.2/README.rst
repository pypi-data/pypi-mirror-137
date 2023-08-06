**TFOD-Automatic**

Tensorflow object detection automatically from user input.

TFOD-Automatic Setup

In this we going to setup requirements for object detection
automatically using TFOD-Automatic.setup.

.. code:: python

   from TFOD-Automatic import setup



**start_download()**


start_download is used to download the tensorflow model garden from the
github.If the model garden is present already in the working
directory.it automatically skip this process.

.. code:: python

   from TFOD-Automatic.setup import start_download
   start_download()



**check_model()**

check_model is used to check whether the model garden folder is present
or not.if the folder is present it return True and else it return False.

.. code:: python

   from TFOD-Automatic.setup import check_model
   check_model()



**protobuf_setup()**


protobuf_setup is used to setup the protobuf.Protobufs to configure
model and training parameters.The Protobuf version is 3.19.

Steps: - Protobuf is downloaded successfully and saved in folder
protobuf. - Now copy the folder protobuf folder and Go to C:/Program
File and paste it inside - Now copy the location of the file like
“C:/Program File /protobuf/bin” - Now open Edit envirnoment variable and
go to Enviroment Variable and paste the location inside Path and save. -
Finaly the open new Anaconda comment prompt and start project.

To Check whether the protobuf is set or not use check_protobuf() method.

.. code:: python

   from TFOD-Automatic.setup import protobuf_setup
   protobuf_setup()



**check_protobuf()**


check_protobuf is used to check whether the protobuf is setup is
completed or not.Returns true if the setup is correct and False if the
setup is incorrect.

.. code:: python

   from TFOD-Automatic.setup import check_protobuf
   check_protobuf()

Note: - Now the tensorflow object detection setup is completed.Next we
are going to install the require package automaticaly



TFOD-Automatic Install Package


In this we going to install the require package for tensorflow object
detection automatically using TFOD-Automatic.install.

.. code:: python

   from TFOD-Automatic import install

**install_packages()**


install_packages is used to install the required Packages like
cython,cocoapi,labelImg,pycocotools-windows.To install these package we
need visual studio c++ build support.If the visual studio c++ build
support is not install then first install it then only we can install
the package. All require package get installed.

.. code:: python

   from TFOD-Automatic.install import install_packages
   install_packages()

**check_installed()**


Check the all packages are installed or not.If the require package is
not install it show the error.

.. code:: python

   from TFOD-Automatic.install import check_installed
   check_installed()

**install_all()**


install_packages is used to install the required Packages like
cython,cocoapi,labelImg,pycocotools-windows.To install these package we
need visual studio c++ build support.If the visual studio c++ build
support is not install then first install it then only we can install
the package. All require package get installed and check all the
packages are installed.

.. code:: python

   from TFOD-Automatic.install import install_all
   install_all()

Note:


-  Now the tensorflow object detection setup is completed and every
   package is installed.Now we are going to create the object detection
   model.

To create the tensorflow object detection model there are two method in TFOD-Automatic they are CreateModel and BuildModel:


-  BuildModel: It is beginner-friendly.Example one command is used to
   create model and complete the training.
-  CreateModel: It is some advance method. It has many command to create
   ,train, export the model.

BuildModel:


Download The Tensorflow model garden and Build object Detect model
automaticaly.

.. code:: python

   from TFOD-Automatic import model

**ModelSetup()**:


ModelSetup class is used to automatically create the Folder setup in
working directory.And also check every package are installed and setup
is completed or not.

.. code:: python

   from TFOD-Automatic.model import ModelSetup
   model_setup=ModelSetup()


**BuildModel()**:


BuildModel is used to automatical create the model.BuildModel complete
Generate the data file,Download the pretrained model,Create Pipeline
file,export the model.

Generate the data file:


It generate record file from the input image.

Download the pretrained model:


It download the model from the tensorflow model zoo.It is pretrained
model.

Create Pipeline file:


Pipeline file contains of the number of training steps,batch size,train
and test folder path also the record file path etc.

Export the model:


Finally we need to export the model for future use.

Parameter:


-  number_of_class:int default:NO DEFAULT VALUE Number of training set
-  pretrained_model_name:string
   default:ssd_mobilenet_v2_320x320_coco17_tpu Please copy pretrained
   model name from the tensorflow model zoo
-  modelUrl:string
   default:http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz
   Pretrained model is downloaded from here.Copy url from tensorflow
   model zoo
-  batch_size_for_train:int default:8 batch while training the model
-  train_steps:int default:2000 Training epochs

.. code:: python

   from TFOD-Automatic.model import BuildModel
   build_model=BuildModel(number_of_class)

Notes


-  It creates the model with number_of_class with batch_size of 8 and
   train_step of 2000.
-  It takes some time. so be patient.
-  After the training is completed their will be the folder called
   ->workspace->training_demo->exported-models. You will find the
   exported model.It can used for future use.

CreateModel

-  number_of_class:int default:NO DEFAULT VALUE Number of training set
-  pretrained_model_name:string
   default:ssd_mobilenet_v2_320x320_coco17_tpu Please copy pretrained
   model name from the tensorflow model zoo
-  modelUrl:string
   default:http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz
   Pretrained model is downloaded from here.Copy url from tensorflow
   model zoo
-  batch_size_for_train:int default:8 batch while training the model
-  train_steps:int default:2000 Training epochs

.. code:: python

   from TFOD-Automatic.model import CreateModel
   # create the class instance
   createmodel=CreateModel()

   # model_setup() is used to check whether the package is installed and setup is correct completed.
   createmodel.model_setup()

   # create_folder() is used to create the require folder in the working directory
   createmodel.create_folder()

   # image_data() is used to generate the label map in .pbtxt format
   createmodel.image_data()

   # generate_file() is used to generate the .record file for the train and test image
   createmodel.generate_file()

   # download_model() is used to Download the pretrained model from tensorflow model zoo.
   createmodel.download_model()

   # configure_pipeline() used to create Pipeline file:Pipeline file contains of the number of training steps,batch size, train and test folder path also the record file path etc.
   createmodel.configure_pipeline()

   #export_model() is used to export the model.Finally we need to export the model for future use.
   createmodel.export_model()
