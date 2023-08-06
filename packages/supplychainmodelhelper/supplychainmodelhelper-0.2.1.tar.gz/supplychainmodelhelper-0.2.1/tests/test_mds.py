from supplychainmodelhelper import mds


import csv
import pandas as pd # 0.25.2
import os.path

import unittest
  
#testDF = {'col1': [1,2], 'col2':[3,4]}
# # Testing mds
class Mymds(unittest.TestCase):
    
    # testing if 2 folders with the same name can exist
    def test_addFolder2ExistingDB(self):
        # TODO check if this works correctly!
        # TODO how to check if this is written corecctly?!
        myfname = './testDCa.hdf5'
        testDCA = mds.Datacube(myfname,'new')
        testDCA.addFolder2ExistingDB(['thisFolder','ss','s','Descripcvdxction'])
        with self.assertRaises(Exception):
            testDCA.addFolder2ExistingDB(['thisFolder','ID','Title','Description'])
            testDCA.addFolder2ExistingDB(['this Folder','ID','Title','Description'])
        #with warnings.catch_warnings(record=True) as w:
        with self.assertWarns(Warning):
            testDCA.addFolder2ExistingDB(['new Folder','ID','Title','Description'])
        
        myDF = testDCA.getMDFromDB()
        assert 'thisFolder' in list(myDF['Folder'])
        assert 'newFolder' in list(myDF['Folder'])

    # testing datacube initialisation
    def test_Datainit(self):
        myfname = './testDCb.hdf5'
        testDCB = mds.Datacube(myfname,'new')
        assert os.path.isfile(myfname)
        assert testDCB.h5Filename == myfname

    # testing if the csv file stored is reproducably equal to the md schema
    def test_exportTemplateMDSchemaofDB2CSV(self):
        myfname = './testDCc.hdf5'
        testDCC = mds.Datacube(myfname,'new')
        testcsv = './dbschematest.csv'
        testDCC.exportTemplateMDSchemaofDB2CSV(testcsv)
        with open(testcsv, newline='') as csvfile:
            testDF = csv.reader(csvfile, delimiter = ';')
            myLine = list(testDF)[0]
        assert testDCC.listOfTemplateMDofDB == myLine

    # test adding data set to folder in db
    # TODO test id checker
    def test_addDataSet2ExistingFolder(self):
        import os
        myfname = './testDCd.hdf5'
        testDCD = mds.Datacube(myfname,'new')
        testDCD.addFolder2ExistingDB(testDCD.listOfTemplateMDofDB)
        testDF = pd.DataFrame(data={'col1': [1,2], 'col2':[3,4]},index=['1','2'])

        # test if wrong md schema raises exception
        with self.assertRaises(Exception):
            testDCD.addDataSet2ExistingFolder(testDCD.listOfTemplateMDofDB[0],['mytest'],testDF)
        
        # test if non existing folder raises exception
        with self.assertRaises(Exception):
            testDCD.addDataSet2ExistingFolder('nonexistingfolder',\
                                              testDCD.listOfTemplateMDofDataset,testDF)

        # test if database entry dumps other errors that have nothing to do with this function
        testDCD.addDataSet2ExistingFolder(testDCD.listOfTemplateMDofDB[0],\
            testDCD.listOfTemplateMDofDataset,testDF)

        # test if existing dataset raises exception
        with self.assertRaises(Exception):
            testDCD.addDataSet2ExistingFolder(testDC.listOfTemplateMDofDB[0],\
                testDCD.listOfTemplateMDofDataset,testDF)

        # test if spaces are removed and warning to user is issued
        myTest = testDCD.listOfTemplateMDofDataset[:]
        myTest[0] = "my stupid test"
        myTest[3] = "10"
        with self.assertWarns(Warning):
            testDCD.addDataSet2ExistingFolder(testDCD.listOfTemplateMDofDB[0],\
                myTest,testDF)
        
        os.remove(myfname)

            


    # load dataset and see if is equal to original
    def test_getDataFrameFromFolder(self):
        myfname = './testDCe.hdf5'
        testDCE = mds.Datacube(myfname,'new')
        testDF = pd.DataFrame(data={'col1': [1,2], 'col2':[3,4]},index=['test1','test2'])
        myfolderMD = ['Folderteste','IDteste','Titleteste','Descriptione']
        mydatasetMD = ['DatasetE','FilenameE','FormatE','IDE','TitleE','RowsE','ColumnsE','EncodingE']
        testDCE.addFolder2ExistingDB(myfolderMD)
        testDCE.addDataSet2ExistingFolder('Folderteste',\
            mydatasetMD,testDF)
        myDF = testDCE.getDataFrameFromFolder(myfolderMD[0],\
            mydatasetMD[0])
        assert all((myDF==testDF).values.flatten())

    # test if md schema is stored consistently in dataset
    def test_getMDFromDataSet(self):
        myfname = './testDCf.hdf5'
        testDCF = mds.Datacube(myfname,'new')
        
        myFolderList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDCF.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut)

        loc = ['BER','SXF','TXL']
        myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        myDF = pd.DataFrame(myData,index=loc)


        myDataList2FillOut = ['distancematrix', 'distmatrix.csv', 'csv', '1', \
            'Distance matrix', str(len(list(myDF.index))), str(len(list(myDF.columns))), 'utf-8']
        testDCF.addDataSet2ExistingFolder(folderName='newfolder', \
            listOfDataEntries=myDataList2FillOut, datasetDF=myDF)
        
        myMD = testDCF.getMDFromDataSet(folderName='newfolder',\
            nameOfDataSet='distancematrix')
        
        assert all([x for x in myDataList2FillOut if x in myMD])


    # test if md schema is stored consistently in folder
    def test_getMDFromFolder(self):
        myfname = './testDCg.hdf5'
        testDCG = mds.Datacube(myfname,'new')
        
        myFolderList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDCG.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut)
                
        assert all([x for x in myFolderList2FillOut \
            if x in testDCG.getMDFromFolder(folderName='newfolder')])

    # test if md schema is stored consistently in database
    def test_getMDFromDB(self):
        myfname = './testDCh.hdf5'
        testDCH = mds.Datacube(myfname,'new')
        
        myFolderList2FillOut1 = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDCH.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut1)

        myFolderList2FillOut2 = ['thishere', '2', 'This is a new test', \
            'weird type of description text to describe the reason for the existence of this folder']
        testDCH.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut2)

        myFolderList2FillOut3 = ['rightnow', '3', 'This is a new test', \
            'some type of description text to describe the reason for the existence of this folder']
        testDCH.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut3)

        myFolderList2FillOut4 = ['topdown', '4', 'This is a really new test', \
            'another kind of description text to describe the reason for the existence of this folder']
        testDCH.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut4)


        myMD = myFolderList2FillOut1+myFolderList2FillOut2+\
            myFolderList2FillOut3+myFolderList2FillOut4
        assert all([x for x in myMD \
            if x in testDCH.getMDFromDB().values.flatten()])

    def test_importMDDataofDBfromCSV(self):
        myfname = './testDCi.hdf5'
        testDCI = mds.Datacube(myfname,'new')
        testdfFileName = './templates/testImportFunction.csv'
        testDCI.importMDDataofDBfromCSV(testdfFileName)
        dbRead = testDCI.getMDFromDB()
        myRead = pd.read_csv(testdfFileName,delimiter=';')
        for el in testDCI.listOfTemplateMDofDB:
            assert(all([True if myRead[el][row]==dbRead[el][row] else False for row in myRead.index]))

    def test_importMDDataofDatasetFromCSV(self):
        myfname = './testDC2j.hdf5'
        testDCJ = mds.Datacube(myfname,'new')

        myFolderList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDCJ.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut)
        myFolderList2FillOut = ['anewtest', '2', 'This is a new test', \
            'some kind of description text to describe the reason for the living of this folder']
        testDCJ.addFolder2ExistingDB(listOfEntries=myFolderList2FillOut)

        testDCJ.importMDDataofDatasetFromCSV('newfolder','./templates/myTemplate.csv')

    def test_add2TemplateMDofDB(self):
        myfname = './testDCK.hdf5'
        testDCK = mds.Datacube(myfname, 'new')
        myNewCats = ['new cat1', 'new cat2', 'new cat3']
        testDCK.add2TemplateMDofDB(myNewCats)
        myFolderMD = ['thisFolder', '1', 's', 'Descripcvdxction','1','2','3']
        assert len(testDCK.listOfTemplateMDofDB) == len(myFolderMD)

        testDCK.addFolder2ExistingDB(myFolderMD)

        with self.assertWarns(Warning):
            testDCK.removeFromTemplateMDofDB(myNewCats)
            # test that nothing happend if sure == False
            assert len(testDCK.listOfTemplateMDofDB) == len(myFolderMD)

        testDCK.removeFromTemplateMDofDB(myNewCats,sure=True)
        assert len(testDCK.listOfTemplateMDofDB) == (len(myFolderMD)-len(myNewCats))

        testDCK.addFolder2ExistingDB(['thisnewFolder', '2', 's', 'Descripcvdxction'])
        testDCK.addFolder2ExistingDB(['thisoldFolder', '3', 's', 'Descripcvdxction'])

        with self.assertWarns(Warning):
            testDCK.add2TemplateMDofDB(myNewCats)
            # test that nothing happend if sure == False
            assert len(testDCK.listOfTemplateMDofDB) == (len(myFolderMD)-len(myNewCats))
        testDCK.add2TemplateMDofDB(myNewCats,sure=True)
        assert len(list(testDCK.getMDFromDB().columns))==len(myFolderMD)
        testDCK.removeFromTemplateMDofDB(myNewCats, sure=True)

    def test_add2TemplateMDofDataset(self):
        myfname = './testDCL.hdf5'
        testDCL = mds.Datacube(myfname, 'new')
        assert len(testDCL.listOfTemplateMDofDataset)==8
        newCats = ['data category 1','data category 2','data category 3']

        #testing change of class variable
        testDCL.add2TemplateMDofDataset(newCats)
        assert len(testDCL.listOfTemplateMDofDataset) == (8+len(newCats))
        assert all([True if i in testDCL.listOfTemplateMDofDataset else False for i in newCats])
        testDCL.removeElementTemplateDataSetMD(newCats)
        assert len(testDCL.listOfTemplateMDofDataset) == 8

        #testing sync with db
        # by adding folder and dataset to db
        # then changing md schema
        # then checking if md schema was changed in db as class variables
        testDF = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]}, index=['1', '2'])
        testMD = ['someTable','Filename','Format','ID','Title','Rows','Columns','Encoding']
        testDCL.addFolder2ExistingDB(['thisnewFolder', '2', 's', 'Descripcvdxction'])
        testDCL.addDataSet2ExistingFolder('thisnewFolder',testMD,testDF)
        with self.assertWarns(Warning):
            testDCL.add2TemplateMDofDataset(newCats)
            assert len(testDCL.listOfTemplateMDofDataset) == 8
            assert len(list(testDCL.getMDFromDataSet('thisnewFolder', 'someTable')['MD Names'])) == 10
        testDCL.add2TemplateMDofDataset(newCats,sure=True)
        assert len(testDCL.listOfTemplateMDofDataset) == (8+len(newCats))
        assert len(list(testDCL.getMDFromDataSet('thisnewFolder', 'someTable')['MD Names'])) == 13
        testDCL.removeElementTemplateDataSetMD(newCats)
        assert len(testDCL.listOfTemplateMDofDataset) == (8 + len(newCats))
        testDCL.removeElementTemplateDataSetMD(newCats,sure=True)
        assert len(testDCL.listOfTemplateMDofDataset) == 8
        assert len(list(testDCL.getMDFromDataSet('thisnewFolder','someTable')['MD Names']))==10
    # test sync function of

    def test_editMDofDB(self):
        myfname = './testDCM.hdf5'
        testDCM = mds.Datacube(myfname, 'new')

        # add 3 folders
        folder1 = ['test', '1', 'a title', 'a description']
        folder2 = ['anothertest', '2', 'another title', 'a new description']
        folder3 = ['yetanothertest', '3', 'yet another title', 'also new description']
        testDCM.addFolder2ExistingDB(folder1)
        testDCM.addFolder2ExistingDB(folder2)
        testDCM.addFolder2ExistingDB(folder3)

        newCats = ['source', 'year', 'help']
        testDCM.add2TemplateMDofDB(newCats,sure=True)

        # edit new entries as list
        folderNames = [folder1[0], folder2[0], folder3[0]]
        myContent = ['Astronomische Nachrichten', 'Zentralblatt Mathematik', 'FMJ']
        testDCM.editMDofDB(folder=folderNames, category='source', content=myContent)
        entered = list(testDCM.getMDFromDB()['source'])
        assert all([True if i in entered else False for i in myContent])
        myContent = ['2009', '2021', '2017']
        testDCM.editMDofDB(folder=folderNames, category='year', content=myContent)
        entered = list(testDCM.getMDFromDB()['year'])
        assert all([True if i in entered else False for i in myContent])
        notEntered = list(testDCM.getMDFromDB()['help'])
        assert notEntered == (['no entry yet']*len(newCats))

        # edit new entries as str
        testDCM.editMDofDB(folder=folder1[0], category='help', content='myContent')
        enteredContent = list(testDCM.getMDFromDB()['help'])
        enteredFolderIndex = list(testDCM.getMDFromDB()['Folder']).index(folder1[0])
        assert enteredContent[enteredFolderIndex] == 'myContent'


        testDCM.removeFromTemplateMDofDB(['source', 'year', 'help'], sure=True)

    #   editMDofDataset
    def test_editMDofDataset(self):
        myfname = './testDCN.hdf5'
        testDCN = mds.Datacube(myfname, 'new')

        # add 3 folders
        folder1 = ['test', '1', 'a title', 'a description']
        testDCN.addFolder2ExistingDB(folder1)

        # adding dataset to folder
        loc = ['BER', 'TXL', 'SXF']
        myData = {loc[0]: [1, 2, 50], loc[1]: [2, 1, 49], loc[2]: [50, 49, 1]}
        myDF = pd.DataFrame(myData, index=loc)
        dataMD = ['distanceMatrix', 'no filename', 'pandas df', '1', 'distance matrix', '3', '3', 'utf-8']
        testDCN.addDataSet2ExistingFolder(folder1[0], dataMD, myDF)

        # adding new md schema to dataset, being sure
        testDCN.add2TemplateMDofDataset(['Creator', 'time of creation'], sure=True)
        assert len(list(testDCN.getMDFromDataSet(folder1[0], dataMD[0])['MD Names']))==12
        testDCN.editMDofDataset(folder1[0],dataMD[0],'Creator','mememe')
        catInd = list(testDCN.getMDFromDataSet(folder1[0], dataMD[0])['MD Names']).index('Creator')
        assert testDCN.getMDFromDataSet(folder1[0], dataMD[0])['Content'][catInd] == 'mememe'
        testDCN.removeElementTemplateDataSetMD(['Creator', 'time of creation'], sure=True)

    def test_removeFolder(self):
        myfname = './testDCO.hdf5'
        testDCO = mds.Datacube(myfname, 'new')

        # add a folder
        folder1 = ['test', '1', 'a title', 'a description']
        folder2 = ['test2', '2', 'another title', 'another description']
        testDCO.addFolder2ExistingDB(folder1)
        testDCO.addFolder2ExistingDB(folder2)
        assert list(testDCO.getMDFromDB()['Folder']) == ['test','test2']
        testDCO.removeFolder(folder1[0])
        assert list(testDCO.getMDFromDB()['Folder']) == ['test2']
        testDCO.removeFolder(folder2[0])
        assert list(testDCO.getMDFromDB()['Folder']) == []

    #   removeDatasetFromFolder
    def test_removeDatasetFromFolder(self):
        myfname = './testDCP.hdf5'
        testDCP = mds.Datacube(myfname, 'new')

        # add a folder
        folder1 = ['newfolder', '1', 'a title', 'a description']
        testDCP.addFolder2ExistingDB(folder1)

        # add a dataset
        loc = ['BER', 'SXF', 'TXL']
        myData = {loc[0]: [1, 2, 50], loc[1]: [2, 1, 49], loc[2]: [50, 49, 1]}
        myDF = pd.DataFrame(myData, index=loc)
        myList2FillOut = ['distancematrix', 'distmatrix.csv', 'csv', '1', 'Distance matrix', \
                str(len(list(myDF.index))), str(len(list(myDF.columns))), 'utf-8']
        testDCP.addDataSet2ExistingFolder(folderName='newfolder', \
                                          listOfDataEntries=myList2FillOut, \
                                          datasetDF=myDF)
        testDCP.removeDatasetFromFolder('newfolder', 'distancematrix')
        dsInd = list(testDCP.getMDFromFolder('newfolder')['MD Names']).index('Dataset')
        assert list(testDCP.getMDFromFolder('newfolder')['Content'][dsInd]) == []







if __name__ == '__main__': 
    unittest.main()








