"""
Protobuf Installation/Compilation

"""

# Author: Lohit Sundaramaha lingam <lohit.cs19@bitsathy.ac>


from git import Repo
import os
import wget
import shutil
from zipfile import ZipFile
from git import RemoteProgress
from tqdm import tqdm


from ._cloneModel import start_download


# TODO Download and setup the Protobuf
class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def protobuf_setup():
    """
    Download and setup Protobuf.Protobuf is used to configure the model and training parameter.
    The Protobuf version is 3.19.

    :return:
    Downlaoded the Protobuf.


    """
    start_download()
    os.chdir(os.path.join("models", "research"))
    # Protobuf setup
    if(os.system("protoc object_detection/protos/*.proto --python_out=.")):
        os.chdir("..")
        os.chdir("..")
        if (os.path.exists(os.path.join("protoc-3.19.0-win64.zip"))):
            print("")
        else:
            url = "https://github.com/protocolbuffers/protobuf/releases/download/v3.19.0/protoc-3.19.0-win64.zip"
            wget.download(url)

        if (os.path.exists(os.path.join("protobuf", "bin"))):
            print("")
        else:
            if (os.path.exists(os.path.join("protobuf"))):
                print("")
            else:
                os.mkdir('protobuf')
            shutil.copy(os.path.join("protoc-3.19.0-win64.zip"), os.path.join("protobuf"))
        os.chdir("protobuf")
        zip = ZipFile('protoc-3.19.0-win64.zip')
        zip.extractall()

        print('''
1.Protobuf is downloaded successfully and saved in folder protobuf
2.Now copy the folder protobuf folder and Go to C:/Program File and paste it inside
3.Now copy the location of the file like "C:/Program File /protobuf/bin"
4.Now open Edit envirnoment variable and go to Enviroment Variable and paste the location inside Path and save.
5.Finaly the open new Anaconda comment prompt and start project.
                ''')
        print(os.chdir(".."))
        print(os.getcwd())
        exit(0)
    else:
        os.chdir("..")
        os.chdir("..")
        print("SetUp already Present")

def check_protobuf():
    """
    Check the Protobuf setup is complete or not.

    :return:
    True if the setup is correct and False if the setup is incorrect.
    """
    start_download()
    os.chdir(os.path.join("models", "research"))
    # Protobuf setup
    if(os.system("protoc object_detection/protos/*.proto --python_out=.")):
        os.chdir("..")
        os.chdir("..")
        return False
    else:
        os.chdir("..")
        os.chdir("..")
        return True




