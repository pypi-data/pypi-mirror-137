"""

purpose: assorted function, which are a bit untested


Functions:
----------
importDataFromFolder - IF the user already has a data folder with certain
specifications
>> from supplychainmodelhelper import datahandling as dh
>> help(dh.importDataFromFolder)
this function may be used to create a hdf5 database without much effort

decBSList - if a list of strings or bytestrings are given, this function
returns a list of strings. No need to check if some string is one or the
other, just apply this to your list.

decBS - if a string or bytestring is given, this function returns a string.
No need to check if some string is one or the other, just apply this to your
list.
"""

import csv #1.0
import h5py # 2.10.0
import pandas as pd # 0.25.2
import os
import warnings
warnings.filterwarnings("ignore")



def decBSList(inputList: list) -> list:
    """
    purpose:convert list of bytestrings to list of strings
    if it is already a string, do nothing

    :param inputList: a list of strings to be converted
    (may be str or bytestring)

    :return: list of strings converted to str

    example:
    from supplychainmodelhelper import datahandling as dh
    blist = [b'test',b'another test',b'not another test']
    strlist = dh.decBSlist(blist)

    """
    definiteList = []
    for i in range(len(inputList)):  
        try:
            definiteList.append(inputList[i].decode())
        except (UnicodeDecodeError, AttributeError):
            definiteList.append(inputList[i])
   
    return definiteList


def decBS(inputString: str) -> str:
    """
    purpose: convert list of bytestrings to list of strings
    if it is already a string, do nothing

    :param inputString: a str or bytestring

    :return: string

    example:
    from supplychainmodelhelper import datahandling as dh
    blist = b'test'
    strlist = dh.decBSlist(blist)

    """
    try:
        definiteString = inputString.decode()
    except (UnicodeDecodeError, AttributeError):
        definiteString = inputString
   
    return definiteString


def importDataFromFolder(
        fileOutputName: str,
        fileInputPath: str,
        fileInMetadataName='folderMD.csv'
) -> bool:
    """
    purpose: import files from existing folder structure
    folder needs to consists of folderMD.csv:
        - minimum entries for headers of folderMD.csv:
            'Folder', 'ID', 'Title', 'Description' optional to enter more
            categories, will be automatically integrated into database
        - fill this csv file with naming the data containing folders,
            give unique IDs and proper title and description
        - every subfolder mentioned in folderMD.csv should contain another
            csv file named as the subfolder (e.g. subfolder is 'Test',
            so the csv file in 'Test' should be named 'TestMD.csv')
        - minimum entries for headers of 'subfolder'MD.csv:
            'Dataset',
            'Filename',
            'Format',
            'ID',
            'Title',
            'Rows',
            'Columns',
            'Encoding'
            ('Dataset' is the identifier you give when retrieving dataset
            from db)
        - put file with 'Filename' into this subfolder, this file will be
            added to database (with header!)

    TODO maybe an example folder?
    current implementation: 1D / 2D dataset only

    :param fileOutputPath:
    :param fileInputPath: the path of the folder 
    :param fileInMetadataName(optional): filename of folderMD.csv(default), maybe different filename
    
    :return: true if input file existed and consistent with all data in folder

    example: 
    from supplychainmodelhelper import datahandling as dh
    path2DataFolder = '../data/'#folder where your data set lies
    myfname = 'test.hdf5'

    didItWork4 = dh.importDataFromFolder(
        fileOutputName=myfname,
        fileInputPath=path2DataFolder
    )
    if didItWork4:
        print('yes!')
    else:
        print('no!')

    """
    done = []
    

    done.append(True) \
        if isinstance(fileInputPath, str) \
        else done.append(False)
    done.append(True) \
        if isinstance(fileInMetadataName, str) \
        else done.append(False)
    done.append(True) \
        if isinstance(fileOutputName, str) \
        else done.append(False)

    # start reading metadata structure
    folderMD = csv.DictReader(
        open(fileInputPath + fileInMetadataName),
        delimiter=';'
    )
    done.append(True) \
        if(os.path.exists(fileInputPath + fileInMetadataName)) \
        else done.append(False)
    
    listOfContent = []
    # writing the hdf5 structure
    with h5py.File(fileOutputName,'w') as db:
        ####################################################
        # creating the structure from meta data schema table
        ####################################################
        # getting the metadata from each metadata table in
        # each of the folders as described in fileFolderLoc
        for row in folderMD:
            listOfContent.append(row['Folder'])
            myAttrs = list(row.keys())        
            # creating the folders and look out for subfolders
            if not row['Subfolder']:
                db.create_group(row['Folder'])
                for run in myAttrs:
                    # attach all info to metadata schema
                    if run != 'Folder' and run != 'Subfolder':
                        db[row['Folder']].attrs[run] = row[run]

            # creating the subfolders(aka subgroups) inside hdf5 db
            # if existing in metadata file
            if row['Subfolder']:
                db[row['Folder']].create_group(row['Subfolder'])

                for run in myAttrs:
                    if run != 'Folder' and run != 'Subfolder':
                        db[
                            row['Folder'] +
                            '/' +
                            row['Subfolder']
                        ].attrs[run] = row[run]
        
    ####################################################
    # incorporating the datasets with corresponding metadata
    ####################################################
        for foldername in db:
    
            #print(foldername)
            # code assumes
            #   that meta datafile is located in file folder and
            #   last 2 letters of filename is "MD" and
            #   is in csv-format
            metaDataFile = csv.DictReader(
                open(
                    fileInputPath +
                    foldername +
                    "/" +
                    foldername +
                    "MD.csv"
                ),
                delimiter=';'
            )
            done.append(True) if(os.path.exists(
                fileInputPath +
                foldername +
                "/" +
                foldername +
                "MD.csv")
            ) else done.append(False)
            
            for row in metaDataFile:
            #     # read in the data set:
            #     NEEDS to have index and column header in csv file
            #     #print(row)
                dataSet = pd.read_csv(
                    fileInputPath + foldername + "/" + row['Filename'],
                    header=0,
                    sep=';',
                    index_col=0,
                    encoding=row['Encoding'],
                    dtype='str'
                )
                done.append(True) if(os.path.exists(
                    fileInputPath+foldername+"/"+row['Filename'])
                ) else done.append(False)
                dataSet = dataSet.fillna(value=0)

            #     # create the hdf5 dataset and store it in the hdf5-file
                dt = h5py.string_dtype(encoding='utf-8')
                d5 = db[foldername].create_dataset(
                    row['Dataset'],
                    data=dataSet,
                    dtype=dt
                )
                
                # attach metadata information to newly created data set
                myAttrs = list(row.keys())
                for run in myAttrs:
                    if run != 'Dataset':
                        db[
                            foldername+
                            '/'+
                            row['Dataset']
                        ].attrs[run] = row[run]
                

                # attach dimension scale from csv file,
                # ASSUMING it's always a 2d table...
                # TODO make it dynamical, so that the reader recognizes
                #  the format!
                # has a unique ID, given that in the MD-files
                # this ID is unique (filewise), as well!
                # TODO currently unique ID is given in filename
                #  --> make it internal UID!
                try:
                    dtIndex = 'i'
                    db[foldername].create_dataset(
                        "ScaleRowOfDataSet"+row['ID'],
                        data=dataSet.index.astype(int).values,
                        dtype=dtIndex
                    )
                except TypeError:
                    # this only works for py3!
                    dtIndex = h5py.string_dtype(encoding='utf-8')
                    db[foldername].create_dataset(
                        "ScaleRowOfDataSet"+row['ID'],
                        data=dataSet.index.values,
                        dtype=dtIndex
                    )
        
                # attach the header row and header columne of the
                # table as meta data info
                # TODO automatic recognition of header
                #  -> cell data type analysis (header = string, data=not string)
                d5.dims[0].label = row['Rows']
                d5.dims[0].attach_scale(
                    db[foldername +
                       "/ScaleRowOfDataSet" +
                       row['ID']
                    ]
                )
                

                try:
                    dtCol = 'i'
                    db[foldername].create_dataset(
                        "ScaleColOfDataSet" + row['ID'],
                        data=dataSet.columns.astype(int).values,
                        dtype=dtCol
                    )
                except TypeError:
                    # this only works for py3!
                    dtCol = h5py.string_dtype(encoding='utf-8')
                    db[foldername].create_dataset(
                        "ScaleColOfDataSet" + row['ID'],
                        data=dataSet.columns.values,
                        dtype=dtCol
                    )
                
                # encoding list of strings to list of b-strings (py3 necessity)
                d5.dims[1].label = row['Columns']
                d5.dims[1].attach_scale(
                    db[
                        foldername +
                        "/ScaleColOfDataSet" +
                        row['ID']
                    ]
                )

        # DATABASE IS WRITTEN AND FILE IS CLOSED!
    #done = True
    return all(done)