"""
Download The Tensorflow model garden
"""

# Author: Lohit Sundaramaha lingam <lohit.cs19@bitsathy.ac>

from git import Repo
import os
from git import RemoteProgress
from tqdm import tqdm


# TODO:Download model and check whether the models is present or not

class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def start_download():
    """
    Download the Model Garden for tensorflow.Tensorflow model Garden is repository with
    many number of state-of-art models and modeling solutions.Checks whether the tensorflow
    model garden folder is present or not.If the folder is not present start_download() function
    just download from online.

    Parameter:
    ---------
    No Parameters to pass

    Return
    ------
    Download the models garden



    """
    if(os.path.exists("models")):
        pass
    else:
        Repo.clone_from("https://github.com/tensorflow/models.git","models",branch='master', progress=CloneProgress())

def check_model():
    """
    Checks the Models Garden for tensorflow present or not.

    Parameter:
    ---------
    No Parameters to pass

    :return:
    true if the models garden is present,
    false if the models garden is not present

    """
    if(os.path.exists("models")):
        return True
    else:
        return False