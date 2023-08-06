"""
Download The Tensorflow model garden and create object Detect  model
"""

# Author: Lohit Sundaramaha lingam <lohit.cs19@bitsathy.ac>


from git import Repo
import os
import shutil
from zipfile import ZipFile
import git
from git import RemoteProgress
from tqdm import tqdm
import wget
import tarfile


class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def check_folder(dict_name):
    for i in dict_name:
        if (os.path.exists(dict_name[i])):
            sample = 10
        else:
            os.mkdir(dict_name[i])


class CreateModel:
    """
    BuildModel automatical create the with the class is called.BuildModel complete
    Generate the data file,Download the pretrained model,Create Pipeline file,
    export the model.


    Parameter:
    ---------
    number_of_class:int default:NO DEFAULT VALUE
        Number of training set


    pretrained_model_name:string default:ssd_mobilenet_v2_320x320_coco17_tpu
        Please copy name from the tensorflow model zoo






    modelUrl:string default:http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz
        Pretrained model is downloaded from here.Copy url from tensorflow model zoo





    batch_size_for_train:int default:8
        batch while training the model





    train_steps:int default:2000
        Training epochs

    """
    def __init__(self,number_of_class,pretrained_model_name="ssd_mobilenet_v2_320x320_coco17_tpu-8",modelUrl="http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz",
                 batch_size_for_train=8,train_steps=2000):
        self.pretrained_model_name = pretrained_model_name
        self.org_url = modelUrl
        self.number_of_class = number_of_class
        self.batch_size_for_train=batch_size_for_train
        self.train_steps=train_steps

        self.folder_outer = {
            'scripts': os.path.join("scripts"),
            'preprocessing': os.path.join("scripts", "preprocessing"),
            'workspace': os.path.join("workspace"),
            'training_demo': os.path.join("workspace", "training_demo"),
        }
        self.folder_inner = {
            'annotations': os.path.join(self.folder_outer['training_demo'], "annotations"),
            'images': os.path.join(self.folder_outer['training_demo'], "images"),
            'test_images': os.path.join(self.folder_outer['training_demo'], 'test'),
            'train_images': os.path.join(self.folder_outer['training_demo'], 'train'),
            'exported-models': os.path.join(self.folder_outer['training_demo'], "exported-models"),
            'models': os.path.join(self.folder_outer['training_demo'], "models"),
            'pre-trained-models': os.path.join(self.folder_outer['training_demo'], "pre-trained-models")
        }


    def model_setup(self):
        """
        Download the tensorflow model garden if it is not present.Also check whether the working
        directory is ready to train the model.Check the all packages are installed or not.If the
        not return the error
        """
        if (os.path.exists("models")):
            a = 10
        else:
            Repo.clone_from("https://github.com/tensorflow/models.git", "models", branch='master',
                            progress=CloneProgress())
            print("The Download is Complted successfully......")
        os.chdir(os.path.join("models", "research"))
        if (os.system("python object_detection/builders/model_builder_tf2_test.py")):
            print("Invalid setup.Please Run setup.py file")
            quit()
        else:
            a = 10
        os.chdir('..')
        os.chdir('..')

    def create_folder(self):
        """
        Create the require folder to build the model.
        """
        check_folder(self.folder_outer)
        check_folder(self.folder_inner)

    def image_data(self):
        """
            Generate the data file:.Also generate the label map from user input

        """
        print("Split the data into two parts Train and test\n")
        print("Paste the image train and test folder...")
        label_input = int(input("Enter the input.0 for create new Label map  and 1 leave it"))
        if (label_input == 1):
            pass
        elif (label_input == 0):
            if (os.path.exists(os.path.join(self.folder_inner['annotations'], 'label_map.pbtxt')) or os.path.exists(
                    os.path.join(self.folder_inner['annotations'], 'test.record')) or os.path.exists(
                    os.path.join(self.folder_inner['annotations'], 'train.record'))):
                if (os.path.exists(os.path.join(self.folder_inner['annotations'], 'label_map.pbtxt'))):
                    os.remove(os.path.join(self.folder_inner['annotations'], 'label_map.pbtxt'))

                if (os.path.exists(os.path.join(self.folder_inner['annotations'], 'test.record'))):
                    os.remove(os.path.join(self.folder_inner['annotations'], 'test.record'))

                if (os.path.exists(os.path.join(self.folder_inner['annotations'], 'train.record'))):
                    os.remove(os.path.join(self.folder_inner['annotations'], 'train.record'))

            labelMap = []
            limit=self.number_of_class
            for i in range(1, limit + 1):
                name_input = input("Name of the class:")
                mydict = {'name': name_input, 'id': i}
                labelMap.append(mydict)

            with open(os.path.join(self.folder_inner['annotations'], "label_map.pbtxt"), 'w') as f:
                for label in labelMap:
                    f.write('item { \n')
                    f.write('\tname:\'{}\'\n'.format(label['name']))
                    f.write('\tid:{}\n'.format(label['id']))
                    f.write('}\n')
                f.close()

        else:
            quit()

        # Tensorflow Records
        if (os.path.exists(os.path.join(self.folder_outer['scripts'], 'generate_tfrecord.py'))):
            pass

        else:
            os.chdir(self.folder_outer['scripts'])
            Repo.clone_from('https://github.com/lohitslohit/generate_tfrecord.git', 'scriptFile')
            shutil.move(os.path.join('scriptFile', 'generate_tfrecord.py'), os.path.join('generate_tfrecord.py'))
            os.chdir("..")


    def generate_file(self):
        """
        It generate .record file from the input image.It is used to train the model.  .record file is created for
        both train and test data

        """
        main_py_file = os.path.join(self.folder_outer['scripts'], 'generate_tfrecord.py')
        label_path = os.path.join(self.folder_inner['annotations'], 'label_map.pbtxt')

        train_im = self.folder_inner['train_images']
        record_train = os.path.join(self.folder_inner['annotations'], 'train.record')
        train_gen = f'python {main_py_file} -x {train_im} -l {label_path} -o {record_train}'
        os.system(train_gen)

        test_im = self.folder_inner['test_images']
        record_test = os.path.join(self.folder_inner['annotations'], 'test.record')
        test_gen = f'python {main_py_file} -x {test_im} -l {label_path} -o {record_test}'
        os.system(test_gen)


    def download_model(self):
        """
        Download the pretrained model:It download the model from the tensorflow model zoo.It is pretrained model.

        """
        os.chdir(self.folder_inner['pre-trained-models'])
        if (os.path.exists(os.path.join("ExtractedFolder", self.pretrained_model_name))):
            print("Model is exixts")
        else:
            print("Downloading ...")
            wget.download(self.org_url)
            file = tarfile.open(self.pretrained_model_name + '.tar.gz')
            exp_files = os.path.join("ExtractedFolder")
            file.extractall(exp_files)
            file.close()
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    def configure_pipeline(self):
        """
        Create Pipeline file:Pipeline file contains of the number of training steps,batch size,
            train and test folder path also the record file path etc.

        """
        exp_folder = os.path.join(self.folder_inner['pre-trained-models'], 'ExtractedFolder')
        model_name = self.pretrained_model_name
        if (not os.path.exists(os.path.join(self.folder_inner['models'], model_name))):
            os.mkdir(os.path.join(self.folder_inner['models'], model_name))

        shutil.copy(os.path.join(exp_folder, model_name, 'pipeline.config'),
                    os.path.join(self.folder_inner['models'], model_name))
        print("Pipe line file is moved successfully......")

        import tensorflow as tf
        from object_detection.utils import config_util
        from object_detection.protos import pipeline_pb2
        from google.protobuf import text_format

        pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()

        with tf.io.gfile.GFile(os.path.join(self.folder_inner['models'], model_name, 'pipeline.config'), "r") as f:
            proto_str = f.read()
            text_format.Merge(proto_str, pipeline_config)

        config_text = text_format.MessageToString(pipeline_config)
        with tf.io.gfile.GFile(os.path.join(self.folder_inner['models'], model_name, 'pipeline.config'), "wb") as f:
            f.write(config_text)

        pipeline_config.model.ssd.num_classes = self.number_of_class
        pipeline_config.train_config.batch_size = self.batch_size_for_train
        pipeline_config.train_config.fine_tune_checkpoint = os.path.join(self.folder_inner["pre-trained-models"],
                                                                         'ExtractedFolder', model_name, 'checkpoint','ckpt-0')
        pipeline_config.train_config.fine_tune_checkpoint_type = 'detection'
        pipeline_config.train_input_reader.label_map_path = os.path.join(self.folder_inner['annotations'],'label_map.pbtxt')
        pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [
            os.path.join(self.folder_inner['annotations'], 'train.record')]
        pipeline_config.eval_input_reader[0].label_map_path = os.path.join(self.folder_inner['annotations'],'label_map.pbtxt')
        pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [
            os.path.join(self.folder_inner['annotations'], 'test.record')]

        config_text = text_format.MessageToString(pipeline_config)
        with tf.io.gfile.GFile(os.path.join(self.folder_inner['models'], model_name, 'pipeline.config'), "wb") as f:
            f.write(config_text)

        shutil.copy(os.path.join("models", "research", "object_detection", "model_main_tf2.py"),
                    os.path.join(self.folder_outer['training_demo']))
        model_main_file = os.path.join(self.folder_outer['training_demo'], 'model_main_tf2.py')
        model_folder = os.path.join(self.folder_inner['models'], self.pretrained_model_name)
        model_config = os.path.join(model_folder, 'pipeline.config')
        final_run = f'python {model_main_file} --model_dir={model_folder} --pipeline_config_path={model_config} --num_train_steps={self.train_steps}'


        os.system(final_run)




    def export_model(self):
        """
        Export the model:Finally we need to export the model for future use.

        :return:
        """
        import uuid
        shutil.copy(os.path.join("models", "research", "object_detection", "exporter_main_v2.py"),
                    os.path.join(self.folder_outer['training_demo']))
        model_main_file = os.path.join(self.folder_outer['training_demo'], 'exporter_main_v2.py')
        model_folder = os.path.join(self.folder_inner['models'], self.pretrained_model_name)
        model_config = os.path.join(model_folder, 'pipeline.config')
        e=uuid.uuid1()
        os.chdir(os.path.join("workspace", "training_demo", "exported-models"))
        os.mkdir("ExportedModel"+str(e))
        folder_name="ExportedModel"+str(e)
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        dirExport = os.path.join("workspace", "training_demo", "exported-models",folder_name)
        final_run = f'python {model_main_file} - -input_type image_tensor - -pipeline_config_path {model_config} - -trained_checkpoint_dir {model_folder} --output_directory {dirExport}'
        os.system(final_run)

