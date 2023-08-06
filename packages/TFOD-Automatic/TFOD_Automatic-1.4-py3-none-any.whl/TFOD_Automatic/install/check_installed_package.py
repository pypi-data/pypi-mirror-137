"""
Install Require packages
"""

# Author: Lohit Sundaramaha lingam <lohit.cs19@bitsathy.ac>

from ..setup import check_protobuf

import os
import shutil


# TODO Package setup

def install_packages():
    """
    Install The require Packages like cython,cocoapi,labelImg,pycocotools-windows.To
    install these package we need to visual studio c++ build support.


    :return:
    All require package get installed.
    """
    check_protobuf()
    os.chdir(os.path.join("models", "research"))
    os.system("pip install cython")
    os.system("pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI")
    os.system("pip install labelImg")
    os.system("pip install pycocotools-windows")
    shutil.copy(os.path.join("object_detection", "packages", "tf2", "setup.py"), os.path.join("setup.py"))
    if (os.system("python -m pip install --use-feature=2020-resolver .")):
        print("Download C++ build support")
    else:
        print("Setup completed")

    os.chdir("..")
    os.chdir("..")



def check_installed():
    """
    Check the all packages are installed or not.If the not return the error

    """
    os.chdir(os.path.join("models", "research"))
    if (os.system("python object_detection/builders/model_builder_tf2_test.py")):
        print("Invalid setup")
    else:
        print("Everything is Working")
    os.chdir("..")
    os.chdir("..")



def install_all():
    """
    Install The require Packages like cython,cocoapi,labelImg,pycocotools-windows.To
    install these package we need to visual studio c++ build support.Check the all
    packages are installed or not.If the not return the error
    :return:
    """
    install_packages()
    check_installed()
