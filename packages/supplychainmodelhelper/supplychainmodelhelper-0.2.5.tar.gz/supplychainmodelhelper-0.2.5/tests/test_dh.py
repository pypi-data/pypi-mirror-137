from supplychainmodelhelper import datahandling as dh
import h5py # 2.10.0
import csv
import pandas as pd # 0.25.2
import os.path
import unittest as ut


def test_decBSList():
    assert dh.decBSList([b'string1',b'string2']) == ["string1","string2"]
    assert dh.decBSList(['string1','string2']) == ["string1","string2"]

def test_decBS():
    assert dh.decBS(b'string1') == "string1"
    assert dh.decBS('string1') == "string1"



# Testing datahandling
#def test_importDataFromFolder():
#    assert dh.importDataFromFolder("./data/metadata/","folderMD.csv","./data/rawData.hdf5") == True

