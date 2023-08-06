# import csv #1.0
import h5py  # 2.10.0
import pandas as pd  # 0.25.2
import os.path
# import sys
# sys.path.append('../')
from supplychainmodelhelper.datahandling import decBSList
import warnings


# warnings.filterwarnings("ignore")

class Datacube:
    '''
    purpose: easy editing of hdf5 database for supply chain modelling
    consists of basic meta data schema for database itself, all 
    folders and datasets.
    basic structure
    database
        - metadata information of all containing folders
        - folder
            - metadata information about folder
            - dataset
                - metadata information about dataset
                - data of dataset
                - axis of dataset

    Possible actions:
    - initialise database: a new hdf5 file created or an existing accessed
    (see __init__)

    - extend the existing basic metadata schema of the database
    Please NOTE that only 1 schema exists at a time for the
    database in question. This schema exists to get easy
    access to existing folders and scan through the database rather
    quickly.
    At this point there is no plan to add multiple md schemas
    to 1 database.
    (add2TemplateMDofDB)

    - extend the existing basic metadata schema of an existing dataset
    Please NOTE that only 1 schema exists at a time for the
    dataset in question. This schema exists to get easy
    access to existing datasets and scan through the database rather
    quickly.
    At this point there is no plan to add multiple md schemas
    to 1 database.
    Further note that folders have a similar md schema as the dataset
    itself. The difference is that in any folder the md schema for
    ALL datasets inside the folder is summarized. See getMDFromFolder
    and getMDFromDataSet.
    (add2TemplateMDofDataset)

    - store the current metadata schema of the database as a
    template csv file, for later import (createTemplate_MD_Schema_DB_CSV)

    - store the current metadata schema of a folder as a
    template csv file, for later import (createTemplate_MD_Schema_Folder_CSV)

    - import csv file with current metadata schema of folder
    and filled out metadata information about containing datasets
    (importFromCSV_MD_DataForFolder)

    -  import csv file with current metadata schema of database
    and filled out metadata information about containing datasets
    (importFromCSV_MD_DataForDB)

    - add/remove a folder to the database, incl. a list of metadata information
    based on the current metadataschema (addFolder2ExistingDB, removeFolder)

    - add/remove a dataset to an existing folder, incl. a list of metadata
    information based on the current metadataschema
    (addDataSet2ExistingFolder, removeDatasetFromFolder)

    - get an existing dataset from a specific folder in the database
    (getDataFrameFromFolder)

    - get metadata information about an existing dataset in the database
    (getMDFromDataSet)

    - get metadata information about an existing folder in the database
    (getMDFromFolder)

    - get metadata information about the database
    (getMDfrom_db)

    - change metadata information of dataset, folder, database
    (editMDofDB,editMDofDataset)

    - remove meta data categories from md schema
    (removeFolderMD,removeDatasetMD)

    '''
    # basic template for mandatory entries for metadata schema
    # if needed add entries in these lists
    # with add2TemplateMDofDB or add2TemplateMDofDataset
    h5file_name = 'defaultDB.hdf5'
    listOfTemplateMDofDB = [
        'Folder',
        'ID',
        'Title',
        'Description'
    ]
    list_template_md_dataset = [
        'Dataset',
        'Filename',
        'Format',
        'ID',
        'Title',
        'Rows',
        'Columns',
        'Encoding'
    ]

    # TODO test in combination with other functions
    def __init__(
            self,
            h5file_name,
            rights='add'
    ):
        """
        purpose: initialise the data object

        input:
        :param h5file_name(optional): path to the hdf5 file. If not existing, a
        new file will be created. default file_name is 'defaultDB.hdf5'
        :param rights(optional): user rights to access this database.
        'add'(default) user may read/write, if no file by this name exists, the
        file will be created.
        'new' will overwrite any existing databases (good for testing the
        database, less good for working with it).
        Also on initialisation of this data object the given hdf5 database
        will be accessed and the md schema from the db overwrites the
        default md schema

        :return: none

        example:
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        #if needed the file_name is attached to this data object
        print(myNewDB.h5file_name)



        ======================================================================


        """

        self.overwritefile_name(h5file_name)
        if rights == 'add':
            with h5py.File(h5file_name, 'a') as db:
                # check md schema of existing db
                if len(list(db.keys())) > 0:
                    check_current_md_schema = list(self.getMDfrom_db().columns)
                    all_categories = [
                        True if i in self.listOfTemplateMDofDB
                        else False
                        for i in check_current_md_schema
                    ]
                    # check if more categories exist in db than in basic md
                    # schema
                    if not all(all_categories):
                        # get index of new categories
                        add_cat = [
                            f for f, x in enumerate(all_categories)
                            if not x
                        ]
                        self.listOfTemplateMDofDB += list(
                            map(
                                check_current_md_schema.__getitem__,
                                add_cat
                            )
                        )
                    new_categories = []
                    for folder in db.keys():
                        for dataset in db[folder].keys():
                            check_current_md_schema = list(
                                self.getMDFromDataSet(
                                    folder,
                                    dataset
                                ).columns
                            )
                            all_categories = [
                                True if i in self.listOfTemplateMDofDB
                                else False
                                for i in check_current_md_schema
                            ]
                            if not all(all_categories):
                                add_cat = [
                                    f for f, x in enumerate(all_categories)
                                    if not x
                                ]
                                new_cat_this_time = list(
                                    map(
                                        check_current_md_schema.__getitem__,
                                        add_cat
                                    )
                                )
                                new_categories = new_categories + \
                                                 new_cat_this_time
                    if new_categories != new_cat_this_time:
                        warnings.warn(
                            'Please be advised: different meta data schemas '
                            'for different datasets is untested!'
                        )
                    self.list_template_md_dataset += new_categories
        elif rights == 'new':
            with h5py.File(self.h5file_name, 'w'):
                print('new file created...' + self.h5file_name)
        else:
            raise Exception('please choose either \'add\' or \'new\'!')

    @classmethod
    def overwritefile_name(
            cls,
            file_name
    ):
        """
        TODO: hide from view
        internal function: not be applied by user
        """
        cls.h5file_name = file_name

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    @classmethod
    def add2TemplateMDofDB(
            cls,
            list_additional_categories,
            sure=False
    ):
        """

        if folder/dataset in db exists, add this new element to all existing
        give user warning that missing entries need to be added to dataset by
        other function
        purpose: adding a list of metadata categories to the overall metadata
        structure of the database

        input:
        :param list_additional_categories: a list of new categories
        :param sure(optional) only asked for if database named in
        initialisation, already contains folders.
        New categories in db will have the note 'no entry yet'


        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDofDB)

        # extend the metadata schema for database
        testDC.add2TemplateMDofDB(['db category 1','db category 2',
        'db category 3'])

        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDB)



        =======================================================================
        """
        # new md schema is built
        new_md_schema = cls.listOfTemplateMDofDB[:] + \
                        list_additional_categories[:]

        # check if existing folders need update
        new_cat = [
            i for i in new_md_schema
            if i not in cls.listOfTemplateMDofDB
        ]

        # check with db
        with h5py.File(cls.h5file_name, 'a') as db:
            # do folders exist? if so, check if element exists and
            # if not -> update it
            if not sure:
                if len(list(db.keys())) > 0:
                    warnings.warn(
                        'Please be advised. '
                        '\nYou are about to change the md schema '
                        'on existing db. \nRepeat this command '
                        'with the flag sure=True, '
                        'if you\'re really sure about this'
                    )
                else:
                    # counting doubles
                    if len(new_md_schema) == len(set(new_md_schema)):
                        cls.listOfTemplateMDofDB = new_md_schema[:]
                    else:
                        warnings.warn(
                            'At least one element was already '
                            'in the md schema. '
                            '\nRemoving the redundancy!'
                        )
                        cls.listOfTemplateMDofDB = list(set(new_md_schema[:]))
            # user is sure about what he/she is doing
            if sure:
                if len(list(db.keys())) > 0:
                    # go through every folder
                    for run in new_cat:
                        # for each folder 1 entry exists
                        # if this is the first entry
                        if not db.attrs.__contains__(run):
                            db.attrs[run] = ['no entry yet'] * len(new_cat)
                    # counting doubles
                    if len(new_md_schema) == len(set(new_md_schema)):
                        cls.listOfTemplateMDofDB = new_md_schema[:]
                    else:
                        warnings.warn(
                            'Warning: At least one element was already'
                            ' in the md schema, removing the redundancy.'
                        )
                        cls.listOfTemplateMDofDB = list(set(new_md_schema[:]))
                else:
                    warnings.warn(
                        'Warning: You set the flag \'sure\'=True, '
                        'but no entries are to be find in database! '
                        'Nothing done.'
                    )

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    @classmethod
    def add2TemplateMDofDataset(
            cls,
            list_additional_categories,
            sure=False
    ):
        """
        purpose: adding a list of metadata categories to the folder meta data

        input:
        :param list_additional_categories: a list of new categories
        :param sure(optional) only asked for if an hdf5 contains folder or
        dataset and the needs to be updated afterwards. New categories in db
        will have the note 'no entry yet'

        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname, 'new')

        # basic md template on creation
        print(testDC.list_template_md_dataset)

        # extend the metadata schema for database
        testDC.add2TemplateMDofDataset(['data category 1', 'data category 2',
                                        'data category 3'])

        # check out the CURRENT metadata schema of the database
        print(testDC.list_template_md_dataset)

        # if dataset are added, the flag 'sure' needs to be set to 'True'
        # otherwise change requests are ignored
        testDC.addFolder2ExistingDB(
            [
                'thisnewFolder',
                '2',
                's',
                'Descripcvdxction'
            ]
        )

        =======================================================================

        """
        new_md_schema = cls.list_template_md_dataset + \
                      list_additional_categories

        # check if existing folders need update
        new_cat = [
            i for i in new_md_schema
            if i not in cls.list_template_md_dataset
        ]

        # check with db
        with h5py.File(cls.h5file_name, 'a') as db:
            # do folders exist? if so, check if element exists and
            # if not -> update it
            if not sure:
                if len(list(db.keys())) > 0:
                    warnings.warn(
                        'Please be advised. You are about to '
                        'change the md schema on existing db.'
                        '\nRepeat this command with the flag '
                        'sure=True, if you\'re really sure about '
                        'this'
                    )
                else:
                    # counting doubles
                    if len(new_md_schema) == len(set(new_md_schema)):
                        cls.list_template_md_dataset = new_md_schema
                    else:
                        warnings.warn(
                            'at least one element was already in the md '
                            'schema, removing the redundancy.'
                        )
                        cls.list_template_md_dataset = list(set(new_md_schema))

            # user is sure about what he/she is doing
            if sure:
                if len(list(db.keys())) > 0:
                    # go through every folder
                    for folder in db.keys():
                        for run in new_cat:
                            # for each folder 1 entry exists
                            # if this is the first entry
                            if not db[folder].attrs.__contains__(run):
                                db[folder].attrs[run] = 'no entry yet'
                        for ds in db[folder].keys():
                            for run in new_cat:
                                if not db[
                                    folder + '/' + ds
                                ].attrs.__contains__(run):
                                    db[
                                        folder + '/' + ds
                                    ].attrs[run] = 'no entry yet'
                    # counting doubles
                    if len(new_md_schema) == len(set(new_md_schema)):
                        cls.list_template_md_dataset = new_md_schema
                    else:
                        warnings.warn(
                            'at least one element was already in the '
                            'md schema. '
                            '\nRemoving the redundancy.'
                        )
                        cls.list_template_md_dataset = list(set(new_md_schema))
                else:
                    warnings.warn(
                        'Warning: You set the flag \'sure\'=True, but no '
                        'entries are to be find in database! Nothing done.'
                    )

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    # TODO some elements (name, id) cant be removed
    @classmethod
    def removeFromTemplateMDofDB(
            cls,
            attr2remove,
            sure=False
    ):
        """
        purpose:
        If no folders are inserted yet to the database, the md schema
        wil be updated with no further warning. This can be undone
        by the function add2TemplateMDofDB.
        If at least 1 folder in db exists, remove this category from all
        existing folders in db. The user gets a warning if the flag 'sure'
        is NOT set to true.

        input:
        :param attr2remove: can be a list or a str
        :param sure: (optional) set True, if database exists already and
        existing entries are to be removed

        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDofDB)

        # extend the metadata schema for database
        testDC.add2TemplateMDofDB(
            ['db category 1','db category 2','db category 3']
        )

        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDB)

        # extend the metadata schema for database
        # can be a list
        testDC.removeFromTemplateMDofDB(['db category 1','db category 2'])
        # or a string
        testDC.removeFromTemplateMDofDB('db category 3')

        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDB)


        =======================================================================
        """
        if not sure:
            with h5py.File(cls.h5file_name, 'r') as db:
                # do folders exist?
                # if so, check if element exists and if not update it
                if len(list(db.keys())) > 0:
                    # dont do anything if folders exists
                    # and the flag sure is not set
                    # -> probably user did something wrong
                    rem = False

                    if isinstance(attr2remove, str):
                        if db.attrs.__contains__(attr2remove):
                            warnings.warn(
                                'Please be advised. ' +
                                str(attr2remove) +
                                ' is already entered into the database.\n'
                                'Repeat this command with the flag sure=True,'
                                ' if you\'re really sure about this'
                            )
                        else:
                            warnings.warn(
                                'Attribute '
                                + str(attr2remove) +
                                ' not found in database. '
                                'Please check spelling!'
                            )
                    elif isinstance(attr2remove, list):
                        for el in attr2remove:
                            if db.attrs.__contains__(el):
                                warnings.warn(
                                    'Please be advised. ' +
                                    str(el) +
                                    ' is already entered into the database.\n'
                                    'Repeat this command with the flag '
                                    'sure=True, if you\'re really sure about '
                                    'this'
                                )
                            else:
                                warnings.warn(
                                    'Attribute ' +
                                    str(el) +
                                    ' not found in database. '
                                    'Please check spelling!'
                                )
                else:
                    # no folders exist and sure is not set to True
                    # by hand of user -> probably ok,
                    # but if not, user may undo this by add2TemplateMDofDB
                    rem = True
        if sure:
            with h5py.File(cls.h5file_name, 'a') as db:
                # user is sure about what he/she is doing
                if len(list(db.keys())) > 0:
                    # probably ok, so go ahead and update class variable
                    # with md schema
                    rem = True
                    if isinstance(attr2remove, str):
                        if db.attrs.__contains__(attr2remove):
                            del db.attrs[attr2remove]
                    elif isinstance(attr2remove, list):
                        for el in attr2remove:
                            if db.attrs.__contains__(el):
                                del db.attrs[el]
                else:
                    # probably the user did something wrong,
                    # so dont do anythind
                    rem = False
                    warnings.warn(
                        'You set the flag sure, even if no database could be '
                        'found. Either read documentation more carefully, or '
                        'something weird happened. For security, nothing '
                        'removed.'
                    )

        # rem is true if sure is False AND no existing entries are in db
        # -> entries removed
        # rem is false if sure is True AND no existing entries are in db
        # -> something weird happened or user didnt read the doc
        # rem is false if sure is False AND existing entries are in db
        # -> user tries to edit db without being sure
        # rem is true if sure is True AND existing entries are in db
        # -> entries removed and synced with db
        if rem:
            # check if input is a list or a str
            if isinstance(attr2remove, str):
                if attr2remove not in cls.listOfTemplateMDofDB:
                    raise Exception(
                        'Given string is not an element of '
                        'the current meta data schema!'
                    )
                else:
                    cls.listOfTemplateMDofDB.remove(attr2remove)
            elif isinstance(attr2remove, list):
                for a in attr2remove:
                    if a not in cls.listOfTemplateMDofDB:
                        raise Exception(
                            'Element ' +
                            str(a) +
                            ' is not an element of the '
                            'current meta data schema!'
                        )
                    cls.listOfTemplateMDofDB.remove(a)
            else:
                raise Exception(
                    'Input is neither list nor string! Nothing removed!'
                )

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    # TODO some elements (name, id) cant be removed
    @classmethod
    def removeElementTemplateDataSetMD(
            cls,
            attr2remove,
            sure=False
    ):
        """
        purpose: removing either 1 element as string or multiple elements of
        metadata categories from ALL datasets.
        There are no multiple schemas for different datasets.
        Might be added later, if pressure is high.

        input:
        :param attr2remove: a str or a list of existing categories
        :param sure: (Boolean) only set to true, if you're sure
        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.list_template_md_dataset)

        # extend the metadata schema for database
        testDC.add2TemplateMDofDataset(
            ['folder category 1','folder category 2','folder category 3']
        )

        # check out the CURRENT metadata schema of the database
        print(testDC.list_template_md_dataset)

        # removing 1 item
        testDC.removeElementTemplateDataSetMD('folder category 2')
        print(testDC.list_template_md_dataset)

        # removing more items
        testDC.removeElementTemplateDataSetMD(
            ['folder category 1','folder category 3']
        )
        print(testDC.list_template_md_dataset)


        =======================================================================

        """
        if not sure:
            with h5py.File(cls.h5file_name, 'r') as db:
                # do folders exist?
                # if so, check if element exists and if not update it
                if len(list(db.keys())) > 0:
                    # dont do anything
                    # if folders exists and the flag sure is not set
                    # -> probably user did something wrong
                    rem = False

                    for folder in db.keys():
                        if isinstance(attr2remove, str):
                            if db[folder].attrs.__contains__(attr2remove):
                                warnings.warn(
                                    'Please be advised. ' +
                                    str(attr2remove) +
                                    ' is already entered into the database.\n'
                                    'Repeat this command with the flag '
                                    'sure=True, if you\'re really sure '
                                    'about this')
                            else:
                                warnings.warn(
                                    'Attribute ' +
                                    str(attr2remove) +
                                    ' not found in database. '
                                    'Please check spelling!'
                                )
                        elif isinstance(attr2remove, list):
                            for el in attr2remove:
                                if db[folder].attrs.__contains__(el):
                                    warnings.warn(
                                        'Please be advised. ' +
                                        str(el) +
                                        ' is already entered into the '
                                        'database.\nRepeat this command with '
                                        'the flag sure=True, if you\'re '
                                        'really sure about this'
                                    )
                                else:
                                    warnings.warn(
                                        'Attribute ' +
                                        str(el) +
                                        ' not found in database. '
                                        'Please check spelling!'
                                    )
                else:
                    # no folders exist and sure
                    # is not set to True by hand of user
                    # -> probably ok, but if not,
                    # user may undo this by add2TemplateMDofDB
                    rem = True

        # optional flag default is False
        if sure:
            with h5py.File(cls.h5file_name, 'a') as db:
                # do folders exist?
                # if so, check if element exists and if not update it
                if len(list(db.keys())) > 0:
                    # probably ok, so go ahead and update class variable
                    # with md schema
                    rem = True

                    for folder in db.keys():
                        if isinstance(attr2remove, str):
                            if db[folder].attrs.__contains__(attr2remove):
                                del db[folder].attrs[attr2remove]
                                print(
                                    'attribute removed from folder: ' +
                                    folder
                                )
                            else:
                                warnings.warn(
                                    'Attribute ' +
                                    str(attr2remove) +
                                    ' not found in database. '
                                    'Please check spelling!'
                                )
                            for ds in db[folder].keys():
                                if db[folder + '/' + ds].attrs.__contains__(
                                        attr2remove
                                ):
                                    del db[
                                        folder + '/' + ds
                                        ].attrs[attr2remove]
                                    print(
                                        'attribute removed from dataset: ' +
                                        ds
                                    )
                        elif isinstance(attr2remove, list):
                            for el in attr2remove:
                                if db[folder].attrs.__contains__(el):
                                    del db[folder].attrs[el]
                                    print(
                                        'attribute removed from folder: ' +
                                        folder
                                    )
                                else:
                                    warnings.warn(
                                        'Attribute ' +
                                        str(el) +
                                        'in folder ' +
                                        folder +
                                        ' not found in database. '
                                        'Please check spelling!'
                                    )
                                for ds in db[folder].keys():
                                    if db[
                                        folder + '/' + ds].attrs.__contains__(
                                        el
                                    ):
                                        del db[folder + '/' + ds].attrs[el]
                                        print(
                                            'attribute removed '
                                            'from dataset: ' +
                                            ds
                                        )
                                    else:
                                        warnings.warn(
                                            'Attribute ' +
                                            str(el) +
                                            'in folder ' +
                                            folder +
                                            ' in dataset ' +
                                            ds +
                                            ' not found in database. '
                                            'Please check spelling!'
                                        )
                else:
                    # probably the user did something wrong,
                    # so dont do anythind
                    rem = False
                    warnings.warn(
                        'You set the flag sure, even if no database '
                        'could be found. Either read documentation more '
                        'carfully, or something weird happened.'
                    )

        # rem is true if sure is False AND no existing entries are in db
        # -> entries removed
        # rem is false if sure is True AND no existing entries are in db
        # -> something weird happened or user didnt read the doc
        # rem is false if sure is False AND existing entries are in db
        # -> user tries to edit db without being sure
        # rem is true if sure is True AND existing entries are in db
        # -> entries removed and synced with db
        if rem:
            if isinstance(attr2remove, str):
                if attr2remove not in cls.list_template_md_dataset:
                    raise Exception(
                        'Given string is not an element of the '
                        'current meta data schema!'
                    )
                else:
                    cls.list_template_md_dataset.remove(attr2remove)
            elif isinstance(attr2remove, list):
                for a in attr2remove:
                    if a not in cls.list_template_md_dataset:
                        raise Exception(
                            'Element ' +
                            str(a) +
                            ' is not an element of the '
                            'current meta data schema!'
                        )
                    cls.list_template_md_dataset.remove(a)
            else:
                raise Exception('input is neither list nor string')

    # TODO test
    # TODO write self test to test new db sync functionality
    # TODO check if ID is unique
    def editMDofDataset(
            self,
            folder_name: str,
            name_dataset: str,
            category: str,
            content: str
    ):
        """
        purpose:
        adding a new category to md schema of dataset is done by
        the function add2TemplateMDofDataset (see example).
        Using this function only editing of EXISTING md categories is
        supported.
        Adding a new category means an update to all datasets, while
        this function only edits (or adds) content to 1 dataset at a time.

        This function checks if all inputs (folder, dataset, category) exists
        before editing the field.

        NOTE that the folder md data is updated as well, since the folder md
        is just a summary of what is in the folder.

        TODO:
        Future updates may have the option of having the variable dataset as a
        list and content as a list, so that multiple entries may be done at
        the same time.

        TODO:
        Is a flag for overwriting existing content necessary?

        input:
        :param folder_name: existing folder in db (str) - assumed all datasets are
        in given folder
        :param name_dataset: existing dataset (str)
        :param category: existing category (str) for changing 1 category
        at a time
        :param content: corresponding content existing category for changing

        :return: none

        example:
         from supplychainmodelhelper import mds
        import pandas as pd
        myNewDB = mds.Datacube('test.hdf5', 'new')

        # adding folder_names to database
        newfolder_nameMD = [
            'newfolder_name',
            '1',
            'A new folder_name',
            'A very cool description'
        ]
        myNewDB.addFolder2ExistingDB(newfolder_nameMD)

        # adding dataset to folder_name
        loc = ['BER', 'TXL', 'SXF']
        my_data = {loc[0]: [1, 2, 50], loc[1]: [2, 1, 49], loc[2]: [50, 49, 1]}
        my_df = pd.DataFrame(my_data, index=loc)
        dataMD = [
            'distanceMatrix',
            'no file_name',
            'pandas df',
            '1',
            'distance matrix',
            '3',
            '3',
            'utf-8'
        ]
        myNewDB.addDataSet2ExistingFolder(newfolder_nameMD[0], dataMD, my_df)

        # adding new md schema to dataset (user gets error, because at least
        # 1 dataset is stored to database
        myNewDB.add2TemplateMDofDataset(['Creator', 'time of creation'])

        # adding new md schema to dataset, being sure
        myNewDB.add2TemplateMDofDataset(
            ['Creator', 'time of creation'],
            sure=True
        )

        # get md info about dataset
        print(
            myNewDB.getMDFromDataSet(
                folder_name='newfolder_name',
                name_dataset='distanceMatrix'
            )
        )

        # editing dataset
        myNewDB.editMDofDataset(
            folder_name='newfolder_name',
            name_dataset='distanceMatrix',
            category='Creator',
            content='Marcel'
        )
        myNewDB.editMDofDataset(
            folder_name='newfolder_name',
            name_dataset='distanceMatrix',
            category='time of creation',
            content='today'
        )


        =======================================================================

        """
        with h5py.File(self.h5file_name, 'a') as db:
            if len(list(db.keys())) > 0:
                if folder_name in db.keys():
                    if name_dataset in db[folder_name].keys():
                        if db[folder_name].attrs.__contains__(category):
                            if db[
                                folder_name +
                                '/' +
                                name_dataset
                            ].attrs.__contains__(category):
                                # edit folder md entry in list
                                where_it_belongs = list(
                                    db[folder_name].attrs['Dataset']
                                ).index(name_dataset)
                                db[folder_name].attrs[category] = \
                                    list(
                                        db[folder_name].attrs[category]
                                    )[where_it_belongs]
                                # edit dataset md
                                db[
                                    folder_name +
                                    '/' +
                                    name_dataset
                                    ].attrs[category] = content
                            else:
                                raise Exception(
                                    'category does not exist in dataset!'
                                )
                        else:
                            raise Exception(
                                'category does not exist in folder!'
                            )
                    else:
                        raise Exception('dataset does not exist!')
                else:
                    raise Exception('folder does not exist!')
            else:
                raise Exception('no folders yet!')

            if isinstance(category, str) and isinstance(content, str):
                if db.attrs.__contains__(category):
                    db.attrs[category] = content
            elif isinstance(category, list) and isinstance(content, list):
                for it, el in enumerate(category):
                    if db.attrs.__contains__(el):
                        db.attrs[el] = content[it]
            else:
                raise Exception(
                    'Both \'category\' and \'content\' must be either str OR '
                    'list. No mixing up please!'
                )

    # TODO test
    # TODO write self test to test new db sync functionality
    # TODO check if ID is unique
    # TODO name shouldnt be editable or sync with db
    # TODO:
    #   Future updates may have the option of having the variable dataset as a
    #   list and content as a list, so that multiple entries may be done at
    #   the same time.
    # TODO:
    #   Is a flag for overwriting existing content necessary?
    def editMDofDB(
            self,
            folder_name,
            category: str,
            content
    ):
        """
        purpose:
        Adding a new category to the MD schema of the database is done by
        the function add2TemplateMDofDB (see example).
        Using this function only editing of EXISTING md categories is
        supported.
        Adding a new category means an update to md data of database, while
        This function only edits (or adds) content to 1 entry of the database
        at a time.

        TODO:
        Future updates may have the option of having the variable dataset as
        a list and content as a list, so that multiple entries may be done
        at the same time.

        TODO:
        Is a flag for overwriting existing content necessary?


        input:
        :param folder_name: the folder for which the content is for (str or list)
        :param category: existing categories for changing (str) - 1 category
        at a time
        :param content: corresponding content existing category and
        (str or list of) folders for changing (str or list) - same dimension
        as folder

        :return:

        example:
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        # add 3 folders
        folder1 = ['test','1','a title','a description']
        folder2 = ['anothertest','2','another title','a new description']
        folder3 = [
            'yetanothertest',
            '3',
            'yet another title',
            'also new description'
        ]
        myNewDB.addFolder2ExistingDB(folder1)
        myNewDB.addFolder2ExistingDB(folder2)
        myNewDB.addFolder2ExistingDB(folder3)

        # add categories without being sure (gets an error, because user
        # wasnt sure)
        myNewDB.add2TemplateMDofDB(['source','year','help'])

        # add categories with being sure
        myNewDB.add2TemplateMDofDB(['source','year','help'],sure=True)

        # edit new entries
        folder_names = [folder1[0],folder2[0],folder3[0]]
        myContent = [
            'Astronomische Nachrichten',
            'Zentralblatt Mathematik',
            'FMJ'
        ]
        myNewDB.editMDofDB(
            folder_name=folder_names,
            category='source',
            content=myContent
        )
        # edit other entries
        myContent = ['2009','2021','2017']
        myNewDB.editMDofDB(
            folder_name=folder_names,
            category='year',
            content=myContent
        )

        #see changes
        print(myNewDB.getMDfrom_db())




        =======================================================================

        """
        existing_folders = list(self.getMDfrom_db()['Folder'])
        with h5py.File(self.h5file_name, 'a') as db:
            # check if folder is str and content is str
            # as they are to be connected
            if isinstance(folder_name, str) and isinstance(content, str):
                # if this attribute exists in database, go ahead
                if db.attrs.__contains__(category) \
                        and folder_name in existing_folders:
                    # get attribute of category and
                    # look up the index where folder is
                    existing_content = db.attrs[category]
                    my_folder_index = list(db.attrs['Folder']).index(folder_name)
                    # replace existing content with new content
                    existing_content[my_folder_index] = content
                    # store replacement in attributes of database
                    db.attrs[category] = existing_content
                else:
                    raise Exception(
                        'Either the category' +
                        category +
                        ' or the folder' +
                        folder_name +
                        ' could not be found in database!'
                    )
            elif isinstance(folder_name, list) and isinstance(content, list):
                if len(folder_name) != len(content):
                    raise Exception(
                        'both list of folders and list of '
                        'content need to be the same length!'
                    )
                for it, el in enumerate(content):
                    if db.attrs.__contains__(category) and \
                            folder_name[it] in existing_folders:
                        # get attribute of category and
                        # look up the index where folder is
                        existing_content = list(db.attrs[category])
                        if len(existing_content) == 0:
                            raise Exception(
                                str(category) +
                                ' should result in a list with at least one '
                                'entry. Error in database md schema!'
                            )
                        my_folder_index = list(
                            db.attrs['Folder']
                        ).index(folder_name[it])
                        # replace existing content with new content
                        existing_content[my_folder_index] = el
                        # store replacement in attributes of database
                        db.attrs[category] = existing_content
                    else:
                        raise Exception(
                            'Either category ' +
                            category +
                            ' or folder ' +
                            str(folder_name[it]) +
                            ' could not be found in database!'
                        )
            else:
                raise Exception(
                    'Both \'category\' and \'content\' must be either str '
                    'OR list. No mixing up please!'
                )

    # TODO test
    def exportTemplateMDSchemaofDB2CSV(
            self,
            filepath_db_schema
    ):
        """
        purpose:
        store the current metadata schema of the database as a
        template csv file, for later import
        creates a template DataFrame csv file
        containing minimum mandatory metadata information
        which can be filled in csv file
        and read in via importMDSchemaofDBfromCSV


        input:
        :param filepath_db_schema: file path to where the template is
        stored to a csv file

        :return: none

        example:
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.exportTemplateMDSchemaofDB2CSV('myBasicMDschemaofDB.csv')

        myNewDB.add2TemplateMDofDB(
            [
                'a new category',
                'another new one',
                'not another one of these'
            ]
        )

        myNewDB.exportTemplateMDSchemaofDB2CSV('expandedMDschemaofDB.csv')



        =======================================================================

        """
        self.filepath_db_schema = filepath_db_schema
        import csv
        with open(self.filepath_db_schema, 'w') as csvfile:
            temp_writer = csv.writer(csvfile, delimiter=';')
            temp_writer.writerow(self.listOfTemplateMDofDB)
        print("meta data schema exported...to " + filepath_db_schema)

    # TODO test
    def exportTemplateMDSchemaofDataset2CSV(
            self,
            filepath_folder_schema
    ):
        """
        purpose:
        stores the current metadata schema into an csv file.
        information about dataset may be added and later import in via
        importMDSchemaofDatasetFromCSV.


        input:
        :param filepath_folder_schema: file path to where the template is
        stored to a csv file

        :return: none

        example:
        from supplychainmodelhelper import mds

        myNewDB = mds.Datacube('test.hdf5', 'new')

        myNewDB.exportTemplateMDSchemaofDataset2CSV(
            'myBasicMDschemaforAllDatasets.csv'
        )

        # adding more categories
        myNewDB.add2TemplateMDofDataset(['something old', 'something new'])

        myNewDB.exportTemplateMDSchemaofDataset2CSV(
            'myAdvancedMDschemaforAllDatasets.csv'
        )



        =======================================================================
        """
        self.filepath_folder_schema = filepath_folder_schema
        import csv
        with open(self.filepath_folder_schema, 'w') as csvfile:
            temp_writer = csv.writer(csvfile, delimiter=';')
            temp_writer.writerow(self.list_template_md_dataset)
        print("meta data schema exported...to " + filepath_folder_schema)

    # TODO test in combination with other stuff
    # TODO check if add2folder doesnt mess with sync the db
    # TODO check if md schema is in agreement with db loaded
    # TODO check if ID is unique
    # TODO check if user imports new md data into existing db -> use case?
    # TODO set flag sure, for user that wants to overwrite current md schema
    def importMDDataofDBfromCSV(
            self,
            csv_file_name
    ):
        """
        purpose:
        User may export current md schema with function
        exportTemplateMDSchemaofDB2CSV to a csv file, then
        edit csv file and then import the content into the
        Datacube.
        NOTE that database should be freshly initialised and NOT
        contain any other data than an extended md schema up to this point.
        This case has not been tested.

        MD schema of csv and current md schema of db (via add2TemplateMDofDB)
        need to be identical (returns error if doesnt fit).
        I.e. the first row of the csv file should contain the
        fields of the md schema.
        All folders are to be created in the database. The name
        and the ID need to be unique (is enforced!).

        User may want to import self created csv:
        If csv file is not created by exportTemplateMDSchemaofDB2CSV
        the separator used should be a ';'.

        input:
        :param csv_file_name: file_name of the csv file, filled in by user

        :return:

        example:
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.exportTemplateMDSchemaofDB2CSV('file_name.csv')

        #...
        # user sees this in 'file_name.csv'
        # 'Folder';'ID';'Title';'Description'
        #...
        # >>> FILE MANIPULATION BY HAND <<<
        # user fills in the fields : csv mock up of 'file_name.csv'
        #'Folder';'ID';'Title';'Description'
        #'test1';'1';'my first Title';'my first description'
        #'test2';'2';'my second Title';'my second description'
        #'test3';'3';'my third Title';'my third description'
        #'test4';'4';'my fourth Title';'my fourth description'

        #...

        myNewDB.importMDDataofDBfromCSV('file_name.csv')

        # show me the new folders incl. md schema
        print(myNewDB.getMDfrom_db())




        =======================================================================

        """
        my_table = pd.read_csv(csv_file_name, delimiter=';')

        for row in my_table.index:
            currentlist_entries = []
            for el in self.listOfTemplateMDofDB:
                currentlist_entries.append(my_table[el][row])
            self.addFolder2ExistingDB(currentlist_entries)

    # TODO test
    # TODO write self test to test new db sync functionality
    # TODO check if add2folder doesnt mess with sync the db
    # TODO check if md schema is in agreement with db loaded
    # TODO check if ID is unique
    # TODO if folder doesnt exist in db, create folder!
    def importMDDataofDatasetFromCSV(
            self,
            folder_name,
            csv_file_name
    ):
        """
        purpose:
        User may export current md schema with function
        exportTemplateMDSchemaofDataset2CSV to a csv file, then
        edit csv file and then import the content into the
        Datacube.

        Checks if current md schema is compatible with imported csv.
        Checks if input parameter folder_name exists as folder in database.
        This function imports all assiociated files named in respective
        md schema and imports them automatically into the database.
        Search for files either in directory where csv file with md data is
        stored or in a subdirectory named 'folder_name'. Returns error if
        neither option is good.

        User may want to import self created csv:
        If csv file is not created by exportTemplateMDSchemaofDB2CSV
        the separator used should be a ';'.



        input:
        :param folder_name: name of existing folder in database
        if data files are stored in subdirectory, it should have
        the same name
        :param file_name: file path to where the template is
        stored to a csv file. file_names given in md schema should
        match the file_names on disk.

        :return: dataframe to check given input

        example:
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.addFolder2ExistingDB(['myfolder'])

        myNewDB.exportTemplateMDSchemaofDataset2CSV('file_name.csv')

        print(myNewDB.

        #...
        # user sees this in 'file_name.csv'
        'Dataset';'file_name';'Format';'ID';'Title';'Rows';'Columns';'Encoding'
        # ...
        # user fills in information
        # >>> FILE MANIPULATION BY HAND <<<
        #importMDDataofDBfromCSV
        #'Dataset';'file_name';'Format';'ID';'Title';'Rows';'Columns
        #';'Encoding'
        #'data1';'data1.csv';'csv';'1';'my first title';'4';'3';'utf-8'
        #'data2';'data2.csv';'csv';'2';'my new title';'12';'31';'utf-8'
        #'data3';'data3.csv';'csv';'3';'my other title';'123';'13';'utf-8'
        # ...

        myNewDB.importMDDataofDatasetFromCSV('myfolder','file_name.csv')
        print(myNewDB.getMDFromFolder('myfolder'))



        =======================================================================

        """
        my_table = pd.read_csv(csv_file_name, delimiter=';')
        csv_dir = os.path.dirname(os.path.abspath(csv_file_name))

        # check if given folder_name exists
        db_md = self.getMDfrom_db()
        existing_folders = [db_md['Folder'][i] for i in db_md.index]
        if folder_name not in existing_folders:
            raise Exception(
                'Please use function \'addFolder2ExistingDB\' '
                'to add folder with metadata schema to database!'
            )

        expected_files = []
        for myFile in my_table.index:
            expected_files.append(my_table['Filename'][myFile])

        # check if dataset file_names in folder_name are consistent with given md
        # sf -> subfolder (if nothing found in same directory,
        # subfolder folder_name is searched)
        if not os.path.isdir(os.path.join(csv_dir, folder_name)):
            sf = False
            warnings.warn(
                'Cant find subfolder ' +
                str(folder_name) +
                '. Lets check if the files are in the same '
                'folder as the given csv file...'
            )

            # checking as warning indicates
            if not all(
                    [
                        True if i in os.listdir(csv_dir)
                        else False for i in expected_files
                    ]
            ):
                not_found = [
                    i if i not in os.listdir(csv_dir)
                    else 'Found' for i in expected_files
                ]
                raise Exception(
                    'Report on missing files: ' +
                    str(not_found)
                )
        else:
            sf = True

        # check if headers of table are consistent with current md schema
        all_found = [True if i in list(my_table.columns)
                     else False for i in self.list_template_md_dataset
                     ]
        if not all_found:
            raise Exception(
                'Did not find all metadata columns needed '
                'for current md schema, please check!'
            )

        # start reading in files:
        for row in my_table.index:
            currentlist_entries = []
            current_file_name = my_table['Filename'][row]
            if sf:
                my_dataset = pd.read_csv(
                    os.path.join(
                        csv_dir,
                        folder_name,
                        current_file_name
                    ),
                    ';'
                )
            else:
                my_dataset = pd.read_csv(current_file_name, ';')
            for el in self.list_template_md_dataset:
                currentlist_entries.append(my_table[el][row])
            print('nothing')
            self.addDataSet2ExistingFolder(
                folder_name,
                currentlist_entries,
                my_dataset
            )

    # TODO everything
    def exportSchemaDF2CSV(
            self,
            folder_path,
            df_md
    ):
        """
        # TODO everything
        purpose:
        save csv file to disk
        create folders named in columns "Folder"
        create corresponding folder metadata files

        input:
        :param xxx:

        :return:

        example:



        =======================================================================

        """
        self.folder_path = folder_path
        self.df_md = df_md

    # TODO subfolder!
    def addFolder2ExistingDB(
            self,
            list_entries
    ):
        """
        purpose:
        if md schema exists, add row to table
        create folder md template from column folder
        add md schema to db for all folders

        input:
        :param list_entries: list of meta data information.
        check mandatory fields via listOfTemplateMDofDB

        :return: none

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        print(testDC.listOfTemplateMDofDB)
        # >>['Folder','ID','Title','Description']

        # add a folder to your database
        my_list2FillOut = [
            'newfolder',
            '1',
            'This is a test',
            'some kind of description text to describe ' +
            'the reason for the existence of this folder'
            ]
        testDC.addFolder2ExistingDB(list_entries=my_list2FillOut)



        =======================================================================

        """
        if len(list_entries) != len(self.listOfTemplateMDofDB):
            raise Exception(
                'given list of entries incompatible '
                'with current metadata schema(' +
                str(len(list_entries)) +
                ' vs. ' +
                str(len(self.listOfTemplateMDofDB)) +
                ')!'
            )

        if list_entries[0] != list_entries[0].replace(" ", ""):
            list_entries[0] = list_entries[0].replace(" ", "")
            warnings.warn(
                'Please be advised, no whitespaces in folder_names! '
                '\nRemoving whitespaces before entering into database'
            )

        with h5py.File(self.h5file_name, 'a') as db:
            # check if folder exists already!
            list_existing_folders = list(db.keys())
            folder_exists = bool(
                set(
                    [list_entries[0]]
                ).intersection(
                    set(list_existing_folders)
                )
            )
            if not folder_exists:
                db.create_group(list_entries[0])
                for index, run in enumerate(self.listOfTemplateMDofDB):
                    # for each folder 1 entry exists
                    # if this is the first entry
                    if not db.attrs.__contains__(run):
                        my_list = []
                    else:  # otherwise just add to the list
                        my_list = list(db.attrs.__getitem__(run))
                    my_list.append(list_entries[index])
                    db.attrs[run] = my_list
            else:
                raise Exception('This folder already exists!')

    # TODO add error of user catches
    # TODO test
    # TODO write self test
    # TODO test what happens if data is in the folder? if everythin is deleted,
    #  add sure flag
    def removeFolder(
            self,
            folder_name: str
    ):
        """
        purpose:
        removes an existing folder from database.

        input:
        :param folder_name: the name of the folder in the db
        (first entry in md schema)

        :return: none

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # add a folder to your database
        my_list2FillOut = [
            'newfolder',
            '1',
            'This is a test',
            'some kind of description text to describe the ' +
            'reason for the existence of this folder'
            ]
        testDC.addFolder2ExistingDB(list_entries=my_list2FillOut)

        testDC.getMDfrom_db()

        testDC.removeFolder('newfolder')

        testDC.getMDfrom_db()


        =======================================================================
        """
        with h5py.File(self.h5file_name, "a") as db:
            db.__delitem__(folder_name)
            fold_ind = list(db.attrs['Folder']).index(folder_name)
            for attr in db.attrs.keys():
                my_list = list(db.attrs[attr])
                del my_list[fold_ind]
                db.attrs[attr] = my_list

        print('folder and corresponding meta data removed')

    # TODO test
    # TODO subfolder!
    # TODO check axis are realy attached to correct dataframes!
    def addDataSet2ExistingFolder(
            self,
            folder_name,
            list_data_entries,
            dataset_df
    ):
        """
        purpose:
        if md schema exists, add row to metadata table in folder
        add dataset to hdf5, reference to name of Dataset
        add metadata scheme of dataset to folder md schema
        NOTE that only 2D dataframes are tested to be stored in this DB!
        NOTE that category 'ID' needs to be unique in this Folder,
        otherwise returns error!

        input:
        :param folder_name: name of an existing folder within hdf5 database
        :param list_data_entries: list of metadata information of current
        md schema
        :param dataset_df: a pandas dataframe with information about axis

        :return:

        example:
        from supplychainmodelhelper import mds
        import pandas as pd

        loc = ['BER','SXF','TXL']

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # creating a folder
        my_list2FillOut = [
            'newfolder',
            '1',
            'This is a test',
            'some kind of description text to describe the reason ' +
            'for the existence of this folder'
        ]
        testDC.addFolder2ExistingDB(list_entries=my_list2FillOut)

        # Creating dataset
        my_data={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        my_df = pd.DataFrame(my_data,index=loc)

        # check current md schema
        print(testDC.list_template_md_dataset)
        #>>['Dataset','file_name','Format','ID','Title','Rows','Columns',
        #'Encoding']

        # add dataset to an existing folder
        my_list2FillOut = [
            'distancematrix',
            'distmatrix.csv',
            'csv',
            '1',
            'Distance matrix',
            str(len(list(my_df.index))),
            str(len(list(my_df.columns))),
            'utf-8'
        ]
        testDC.addDataSet2ExistingFolder(
            folder_name='newfolder',
            list_data_entries=my_list2FillOut,
            dataset_df=my_df
        )



        =======================================================================

        """
        self.list_data_entries = list_data_entries
        self.folder_name = folder_name
        self.dataset_df = dataset_df
        if len(self.list_data_entries) != len(self.list_template_md_dataset):
            raise Exception(
                'given list of entries incompatible '
                'with current metadata schema!'
            )

        if list_data_entries[0] != list_data_entries[0].replace(" ", ""):
            list_data_entries[0] = list_data_entries[0].replace(" ", "")
            warnings.warn(
                'Please be advised, no whitespaces in dataset_names! '
                'Removing whitespaces before entering into database'
            )

        is_there_an_object = [
            True if i == object
            else False for i in list(dataset_df.dtypes)
        ]
        if any(is_there_an_object):
            if is_there_an_object[0]:
                dataset_df.index = dataset_df[list(dataset_df.columns)[0]]
                del dataset_df[list(dataset_df.columns)[0]]
            else:
                raise Exception(
                    'currently only numbers are accepted in this database'
                )

        # create dataset
        # add list of datasets with metadata to database
        # attach metadata of dataset to folder
        # list_template_md_dataset = [
        #   'Dataset'-0,
        #   'file_name'-1,
        #   'Format'-2,
        #   'ID'-3,
        #   'Title'-4,
        #   'Rows'-5,
        #   'Columns'-6,
        #   'Encoding'-7
        #  ]
        with h5py.File(self.h5file_name, 'a') as db:
            # check if folder exists
            list_existing_folders = list(db.keys())
            folder_exists = bool(
                set([folder_name]).intersection(set(list_existing_folders)))

            if folder_exists:
                # adding dataset to hdf5 file
                name_dataset = list_data_entries[0]
                # check if name of data set exists already in this folder
                list_existing_datasets_in_folder = list(db[folder_name].keys())
                dataset_exists = bool(set([name_dataset]).intersection(
                    set(list_existing_datasets_in_folder)))
                # id checker
                if db[folder_name].attrs.__contains__('ID'):
                    list_existing_ids_in_folder = list(
                        db[folder_name].attrs['ID']
                    )
                    id_dataset = list_data_entries[3]
                    id_exists = bool(
                        set([id_dataset]).intersection(
                            set(list_existing_ids_in_folder)
                        )
                    )
                else:
                    id_exists = False

                if id_exists:
                    raise Exception('Please choose another ID!')

                # start entering data after checking
                # if folder exists and dataset is new
                if not dataset_exists:
                    # store data set in db
                    my_d = db[folder_name].create_dataset(
                        name=name_dataset,
                        data=dataset_df
                    )

                    # store md attached to dataset in db
                    for index, run in enumerate(
                            self.list_template_md_dataset):
                        # adding metadata to hdf5 file attached to dataset
                        db[
                            folder_name +
                            '/' +
                            name_dataset
                            ].attrs[run] = self.list_data_entries[index]

                        # adding metadata schema to folder
                        # if first entry in this folder, create list
                        if not db[folder_name].attrs.__contains__(run):
                            my_list = []
                        else:  # otherwise add to existing list
                            my_list = list(
                                db[folder_name].attrs.__getitem__(run))
                        my_list.append(self.list_data_entries[index])
                        db[folder_name].attrs[run] = my_list

                    # store axis information of dataframe attached to dataset
                    try:
                        dt_index = 'i'
                        db[self.folder_name].create_dataset(
                            "ScaleRowOfDataSet" +
                            str(list_data_entries[3]),
                            data=self.dataset_df.index.astype(int).values,
                            dtype=dt_index
                        )
                    except TypeError:
                        dt_index = h5py.string_dtype(encoding='utf-8')
                        db[self.folder_name].create_dataset(
                            "ScaleRowOfDataSet" + str(list_data_entries[3]),
                            data=self.dataset_df.index.values,
                            dtype=dt_index
                        )
                    my_d.dims[0].label = self.list_template_md_dataset[5]
                    my_d.dims[0].attach_scale(
                        db[
                            folder_name +
                            '/ScaleRowOfDataSet' +
                            str(list_data_entries[3])
                            ]
                    )

                    try:
                        dt_col = 'i'
                        db[self.folder_name].create_dataset(
                            "ScaleColOfDataSet" +
                            str(list_data_entries[3]),
                            data=self.dataset_df.columns.astype(int).values,
                            dtype=dt_col
                        )
                    except TypeError:
                        # this only works for py3!
                        dt_col = h5py.string_dtype(encoding='utf-8')
                        db[self.folder_name].create_dataset(
                            "ScaleColOfDataSet" + str(list_data_entries[3]),
                            data=self.dataset_df.columns.values,
                            dtype=dt_col
                        )
                    # encoding list of strings to list of b-strings
                    # (py3 necessity)
                    my_d.dims[1].label = self.list_template_md_dataset[6]
                    my_d.dims[1].attach_scale(
                        db[
                            self.folder_name +
                            "/ScaleColOfDataSet" +
                            str(list_data_entries[3])
                            ]
                    )
                    # list_template_md_dataset = [
                    #   'Dataset'-0,
                    #   'file_name'-1,
                    #   'Format'-2,
                    #   'ID'-3,
                    #   'Title'-4,
                    #   'Rows'-5,
                    #   'Columns'-6,
                    #   'Encoding'-7
                    #  ]
                else:
                    raise Exception(
                        'Name of data set already exists in this '
                        'particular folder, must be unique!'
                    )
            else:
                raise Exception(
                    'This folder does NOT exist. '
                    'Please create a folder by this name!'
                )

    # TODO add error of user catches
    # TODO test
    # TODO write self test now
    def removeDatasetFromFolder(
            self,
            folder_name,
            dataset_name
    ):
        """
        purpose:
        removes an existing dataset in an existing folder from database.

        input:
        :param folder_name: the name of the folder in the db
        :param dataset_name: the name of the dataset in the folder 'folder_name'

        :return: none

        example:
        from supplychainmodelhelper import mds
        import pandas as pd

        loc = ['BER','SXF','TXL']

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # creating a folder
        my_list2FillOut = [
            'newfolder',
            '1',
            'This is a test',
            'some kind of description text to describe the reason' +
            'for the existence of this folder'
        ]
        testDC.addFolder2ExistingDB(list_entries=my_list2FillOut)

        # Creating dataset
        my_data={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        my_df = pd.DataFrame(my_data,index=loc)

        # check current md schema
        print(testDC.list_template_md_dataset)
        #>>['Dataset','file_name','Format','ID','Title','Rows','Columns',
        #'Encoding']

        # add dataset to an existing folder
        my_list2FillOut = [
            'distancematrix',
            'distmatrix.csv',
            'csv',
            '1',
            'Distance matrix',
            str(len(list(my_df.index))),
            str(len(list(my_df.columns))),
            'utf-8'
        ]
        testDC.addDataSet2ExistingFolder(
            folder_name='newfolder',
            list_data_entries=my_list2FillOut,
            dataset_df=my_df
        )

        testDC.removeDatasetFromFolder('newfolder','distancematrix')


        =======================================================================
        """

        with h5py.File(self.h5file_name, "a") as db:
            ds_ind = list(db[folder_name].attrs['Dataset']).index(dataset_name)
            for index, run in enumerate(db[folder_name].attrs.keys()):
                my_list = list(db[folder_name].attrs[run])
                del my_list[ds_ind]
                db[folder_name].attrs[run] = my_list

            del db[folder_name + '/' + dataset_name]
            # list_md_names = list()
        print('dataset removed')

    # TODO test
    def getDataFrameFromFolder(
            self,
            folder_name,
            name_dataset
    ):
        """

        purpose: retrieve dataset from hdf5 db as pandas data frame

        input:
        :param folder_name: name of an existing folder within hdf5 database
        :param name_dataset: the name of the dataset given in list of
        md schema (first element of this list)

        :return: the dataframe with axis(if exist)

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing dataset back from database
         #(created by addDataSet2ExistingFolder)
         my_datasetFromhdf5DB = testDC.getDataFrameFromFolder(
            folder_name='newfolder',
            name_dataset='distancematrix'
        )

        =======================================================================
        """
        self.folder_name = folder_name
        self.name_dataset = name_dataset

        with h5py.File(self.h5file_name, 'r') as db:
            list_existing_folders = list(db.keys())
            folder_exists = bool(set([self.folder_name]).intersection(
                set(list_existing_folders)))
            if not folder_exists:
                raise Exception('Folder name doesnt exist. Please check!')
            try:
                from_db = db[folder_name + '/' + name_dataset]
            except KeyError:
                raise Exception('data set with this name is not stored here!')
            my_df = pd.DataFrame(
                data=from_db,
                index=decBSList(list(from_db.dims[0][0])),
                columns=decBSList(list(from_db.dims[1][0]))
            )
        return my_df

    # TODO test
    def getMDFromDataSet(
            self,
            folder_name,
            name_dataset
    ):
        """

        purpose: retrieve metadata from dataset in hdf5 db

        input:
        :param folder_name: name of an existing folder within hdf5 database
        :param name_dataset: the name of the dataset given in list of md schema
        (first element of this list)

        :return: a dataframe(2 column table) of information about an existing
        dataset with headers: MD Names, Content

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

        # retrieve existing dataset back from database
        # (created by addDataSet2ExistingFolder)
        print(
            testDC.getMDFromDataSet(
                folder_name='newfolder',
                name_dataset='distancematrix'
            )
        )



        =======================================================================

        """
        self.folder_name = folder_name
        self.name_dataset = name_dataset
        list_md_names = []
        list_md_contents = []

        with h5py.File(self.h5file_name, 'r') as db:
            try:
                for x in db[folder_name +
                            '/' +
                            name_dataset
                ].attrs.__iter__():
                    list_md_names.append(x)
                    list_md_contents.append(
                        db[folder_name +
                           '/' +
                           name_dataset
                           ].attrs.__getitem__(x))
            except KeyError:
                raise Exception('data set with this name is not stored here!')
        return pd.DataFrame(
            data={'MD Names': list_md_names, 'Content': list_md_contents})

    # TODO get like DB otherwise IT WONT WORK!
    def getMDFromFolder(
            self,
            folder_name
    ):
        """
        purpose:
        retrieve metadata from folder, information about the folder in question
        and which information they contain

        input:
        :param folder_name: name of an existing folder within hdf5 database

        :return:  a dataframe(2 column table) of information about an existing
        dataset with headers: MD Names, Content wit list of all datasets

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing folder back from database
         # (created by addDataSet2ExistingFolder)
        print(testDC.getMDFromFolder(folder_name='newfolder'))



        =======================================================================

        """
        self.folder_name = folder_name
        list_md_names = []
        list_md_contents = []

        with h5py.File(self.h5file_name, 'r') as db:
            try:
                for x in db[folder_name].attrs.__iter__():
                    list_md_names.append(x)
                    list_md_contents.append(
                        db[folder_name].attrs.__getitem__(x)
                    )
            except KeyError:
                raise Exception(
                    'folder name with this name is not stored here!'
                )
        return pd.DataFrame(
            data={'MD Names': list_md_names, 'Content': list_md_contents}
        )

    # TODO test with different content and customized metadata schemas
    def getMDfrom_db(self):
        """
        purpose:
        retrieve metadata from db, information about folders in this database
        and which information they contain returned as pandas dataframe

        input: no parameters needed, as each instance deals with just one
        database

        :return: a dataframe (multi-column table) of information about an
        existing dataset with headers based on current md schema
        (basic schema headers: Description, Folder, ID, Title)

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve md info about database
         # (created by addDataSet2ExistingFolder)
        print(testDC.getMDfrom_db())

        ======================================================================
        """
        try:
            with h5py.File(self.h5file_name, 'r') as db:
                my_keys = [key for key in db.attrs.keys()]
                my_vals = [val for val in db.attrs.values()]
        except KeyError:
            raise Exception('data set with this name is not stored here!')

        my_df = pd.DataFrame(columns=my_keys)
        for i, x in enumerate(my_vals):
            my_df[my_keys[i]] = list(my_vals[i])
        return my_df
