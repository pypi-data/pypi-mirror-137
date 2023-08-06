from supplychainmodelhelper import graphoperations as go

#import csv
#import pandas as pd # 0.25.2
#import os.path

import unittest
  
#testDF = {'col1': [1,2], 'col2':[3,4]}
# # Testing mds
class Mygo(unittest.TestCase):

    # Testing graph operations
    def test_combineActorBrand(self):
        assert go.combineActorBrand("test",["one","two"]) == ["test_one","test_two"]

    def test_createGraph(self):
        actorsWrong = 3
        locationWrong = 'string'
        productWrong = (2,4)

        actorOK = ['dfdf','dfdw','ddfdwq']
        locationOK = ['dfds']
        productOK = ['dfds','dsfs']
        
        with self.assertRaises(Exception):
            myNW = go.createGraph(listOfActors=actorsWrong,\
                listOfLocations=locationOK,\
                    listOfProducts=productOK)
        with self.assertRaises(Exception):
            myNW = go.createGraph(listOfActors=actorOK,\
                listOfLocations=locationWrong,\
                    listOfProducts=productOK)
        with self.assertRaises(Exception):
            myNW = go.createGraph(listOfActors=actorOK,\
                listOfLocations=locationOK,\
                    listOfProducts=productWrong)
                
        with self.assertRaises(Exception):
            myNW = go.createGraph(listOfActors=[],\
                listOfLocations=locationOK,\
                    listOfProducts=productOK)
        with self.assertRaises(Exception):
            myNW = go.createGraph(listOfActors=actorOK,\
                listOfLocations=[],\
                    listOfProducts=productOK)
        with self.assertRaises(Exception):
            myNW = go.createGraph(listOfActors=actorOK,\
                listOfLocations=locationOK,\
                    listOfProducts=[])
        
        myNW = go.createGraph(listOfActors=actorOK,\
                listOfLocations=locationOK,\
                    listOfProducts=productOK)

        assert len(list(myNW.nodes))==len(actorOK)*len(locationOK)*len(productOK)

    def test_getListOfNodeIDs(self):
        actorsWrong = 3
        locationWrong = 'string'
        productWrong = (2,4)

        actorOK = ['dfdf','dfdw','ddfdwq']
        locationOK = ['dfds']
        productOK = ['dfds','dsfs']

        myNW = go.createGraph(listOfActors=actorOK,\
                listOfLocations=locationOK,\
                    listOfProducts=productOK)

        with self.assertRaises(Exception):
            myList = go.getListOfNodeIDs(myNW,actors=actorsWrong,\
                locations=locationOK,\
                    products=productOK)
        with self.assertRaises(Exception):
            myList = go.getListOfNodeIDs(myNW,actors=actorOK,\
                locations=locationWrong,\
                    products=productOK)
        with self.assertRaises(Exception):
            myList = go.getListOfNodeIDs(myNW,actors=actorOK,\
                locations=locationOK,\
                    products=productWrong)
                
        with self.assertRaises(Exception):
            myList = go.getListOfNodeIDs(myNW,actors=[],\
                locations=locationOK,\
                    products=productOK)
        with self.assertRaises(Exception):
            myList = go.getListOfNodeIDs(myNW,actors=actorOK,\
                locations=[],\
                    products=productOK)
        with self.assertRaises(Exception):
            myList = go.getListOfNodeIDs(myNW,actors=actorOK,\
                locations=locationOK,\
                    products=[])
        
        assert len(go.getListOfNodeIDs(myNW)) == len(actorOK)*len(locationOK)*len(productOK)
        assert len(go.getListOfNodeIDs(myNW,products=[productOK[0]]))\
             == len(actorOK)*len(locationOK)
        assert len(go.getListOfNodeIDs(myNW,locations=[locationOK[0]]))\
             == len(actorOK)*len(productOK)
        assert len(go.getListOfNodeIDs(myNW,actors=[actorOK[0]]))\
             == len(productOK)*len(locationOK)


        # test if exception about actors is raised
        # test if exception about location is raised
        # test if exception about product is raised
 
    def test_addAttr2ExistingNodes(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'])
        listOfAGS = ['01111','01112','01113','01111','01112','01113','01111','01112','01113']

        assert go.addAttr2ExistingNodes(myNW, listOfNodeIDs=producerIDs, nameOfAttr='ags', listOfAttr=listOfAGS)

    def test_getNodeIDswAttr(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'], products=['milk'])
        assert go.getNodeIDswAttr(myNW,nameOfAttr='location',listOfNodeIDs=producerIDs) ==\
            go.convertTup2LoT(producerIDs,loc)

    def test_convertLoT2NTsANDconvertTup2LoT(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']

        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)
        
        senderIDs = go.getListOfNodeIDs(myNW, actors=['producer'],products=['milk'])
        receiverIDs = go.getListOfNodeIDs(myNW, actors=['consumer'],products=['milk'])
        
        myEdges4Graph = go.getEdgeID(myNW,senderIDs,receiverIDs)
        list1,list2 = go.convertLoT2NTs(myEdges4Graph)
        assert go.convertTup2LoT(list1,list2) == myEdges4Graph


    def test_proxyModel(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)
        senderIDs = go.getListOfNodeIDs(myNW, actors=['producer'],products=['milk'])

        nationalProduction = 100.
        proxynatProduction = 10.

        print('creating list for input for proxymodel')
        proxyregProduction = [2,4,2]

        regionalProduction = go.proxyModel(inputNr=nationalProduction, proxyData=proxyregProduction, proxyNr=proxynatProduction)
        print(regionalProduction)
        
        print('creating list of tuples for input for proxymodel')
        proxyregProdWithNodeIDs = go.convertTup2LoT(senderIDs,proxyregProduction)
        
        regionalProduction = go.proxyModel(inputNr=nationalProduction, proxyData=proxyregProdWithNodeIDs, proxyNr=proxynatProduction)
        _,list2 = go.convertLoT2NTs(regionalProduction)
        assert list2 == [10*i for i in proxyregProduction]

    def test_getExistingAttrs(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        assert all([x for x in ['location', 'product', 'actor'] if x in go.getExistingAttrs(myNW, gtype = 'nodes')])
        assert go.getExistingAttrs(myNW, gtype = 'edges') == []

    def test_getAllCombinations(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
    
        myNewList1,myNewList2 = go.getAllCombinations(prod,act)
        assert prod*4 == myNewList1
        assert [val for val in act for _ in (0,1,2)] == myNewList2

    def test_getEdgeID(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']

        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)
        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'])
        consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
      
        myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=producerIDs, incomingNodes=consumerOfSchnapsIDs)
        assert myEdgeIDs == go.convertTup2LoT(producerIDs,consumerOfSchnapsIDs)

    def test_addAttr2Edges(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'])
        consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
        myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=producerIDs, incomingNodes=consumerOfSchnapsIDs)

        listOfShipping = [10,1,2000]
        listOfDistances = [50.2,10.3,111.2]

        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfShipping)
        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfDistances, attr='distance')

    def test_getEdgesAttr(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'])
        consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
        myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=producerIDs, incomingNodes=consumerOfSchnapsIDs)

        listOfShipping = [10,1,2000]
        listOfDistances = [50.2,10.3,111.2]

        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfShipping)
        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfDistances, attr='distance')

        assert [listOfDistances[1]] == go.getEdgesAttr(myNW, attr = 'distance', listOfEdgeIDs = [myEdgeIDs[1]])

    def test_getEdgeIDswAttr(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'], products=['schnaps'])
        consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
        
        myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=producerIDs, incomingNodes=consumerOfSchnapsIDs)

        listOfShipping = [10,1,2000]
        listOfDistances = [50.2,10.3,111.2]

        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfShipping)
        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfDistances, attr='distance')

        print(go.getEdgeIDswAttr(myNW, attr = 'weight'))
        print(go.getEdgeIDswAttr(myNW, attr = 'distance', listOfEdgeIDs = myEdgeIDs))

        nodeOut, nodeIn, dist = go.convertLoT2NTs(\
            go.getEdgeIDswAttr(myNW,'distance'))
        
        assert nodeOut == producerIDs
        assert nodeIn == consumerOfSchnapsIDs
        assert dist == listOfDistances

    def test_optFlow(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'], products=['schnaps'])
        consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
        
        myNewList1,myNewList2 = go.getAllCombinations(producerIDs,consumerOfSchnapsIDs)
        myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=myNewList1, incomingNodes=myNewList2)
        
        listOfDistances = [50.2,111.,333.,111.,10.3,551.1,333.,551.1,111.2]

        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfDistances, attr='distance')
                
        with self.assertRaises(Exception):
            go.optFlow(beta=0.1, \
                SCGraph=myNW, \
                    listOfSenderIDs=producerIDs, \
                        listOfReceiverIDs=consumerOfSchnapsIDs, \
                            edgeattrDistName='distance', \
                                distanceModel='exp')
        
        listOfOutGoing = [1,2,3]
        listOfIncoming = [3,2,1]
        assert go.addAttr2ExistingNodes(myNW,producerIDs,'output',listOfOutGoing)
        assert go.addAttr2ExistingNodes(myNW,consumerOfSchnapsIDs,'input',listOfIncoming)
        go.optFlow(beta=0.1, \
            SCGraph=myNW, \
                listOfSenderIDs=producerIDs, \
                    listOfReceiverIDs=consumerOfSchnapsIDs, \
                        edgeattrDistName='distance', \
                            distanceModel='exp')
        
    def test_getDistMatrix(self):
        import pandas as pd

        # creating the graph
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)    

        # Creating Distance matrix
        myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        myDF = pd.DataFrame(myData,index=loc)

        # creating list of node IDs of participants
        senderIDs = go.getListOfNodeIDs(myNW, actors=['producer'],products=['milk'])
        receiverIDs = go.getListOfNodeIDs(myNW, actors=['consumer'],products=['milk'])

        # creating edgeIDs for adding 'distance' to graph
        allcombIDs1,allcombIDs2 = go.getAllCombinations(senderIDs,receiverIDs,order='1st')
        myEdges4Graph = go.getEdgeID(myNW,allcombIDs1,allcombIDs2)
        assert go.addAttr2Edges(myNW,myEdges4Graph, myDF.values.flatten(),attr='distance')

        assert all((myDF.values == \
            go.getDistMatrix(myNW, \
                listOfSenderIDs=senderIDs, \
                    listOfReceiverIDs=receiverIDs, \
                        edgeattrDistName='distance')).flatten())
    
    def test_propFlow(self):
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)

        producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'], products=['schnaps'])
        consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
        
        myNewList1,myNewList2 = go.getAllCombinations(producerIDs,consumerOfSchnapsIDs)
        myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=myNewList1, incomingNodes=myNewList2)
        
        listOfDistances = [50.2,111.,333.,111.,10.3,551.1,333.,551.1,111.2]

        assert go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfDistances, attr='distance')
  
        with self.assertRaises(Exception):
            go.propFlow(myNW,producerIDs,consumerOfSchnapsIDs)
        
        listOfOutGoing = [1,2,3]
        listOfIncoming = [3,2,1]
        assert go.addAttr2ExistingNodes(myNW,producerIDs,'output',listOfOutGoing)
        assert go.addAttr2ExistingNodes(myNW,consumerOfSchnapsIDs,'input',listOfIncoming)

        go.propFlow(myNW,producerIDs,consumerOfSchnapsIDs)

    def test_calcPotTransportDistances(self):
        import pandas as pd
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)  

        senderIDs = go.getListOfNodeIDs(myNW, actors=['producer'],products=['milk'])
        receiverIDs = go.getListOfNodeIDs(myNW, actors=['consumer'],products=['milk'])
        allcombIDs1,allcombIDs2 = go.getAllCombinations(senderIDs,receiverIDs,order='1st')
        myEdges4Graph = go.getEdgeID(myNW,allcombIDs1,allcombIDs2)
        sendingMilk = [10,50,40]
        receivingMilk = [30,30,40]
        assert go.addAttr2ExistingNodes(myNW,senderIDs,'output',sendingMilk)
        assert go.addAttr2ExistingNodes(myNW,receiverIDs,'input',receivingMilk)

        # building distance matrix from scratch
        myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        myDF = pd.DataFrame(myData,index=loc)
        print(myDF)
        assert go.addAttr2Edges(myNW,myEdges4Graph, myDF.values.flatten(),attr='distance')
        
        print('\n Give me the average transport distances for these fake data points')
        myTDs = go.calcPotTransportDistances(myNW, listOfSenderIDs=senderIDs, listOfReceiverIDs=receiverIDs, nrOfValues=5)
        assert myTDs == [5.0, 9.0, 13.0, 17.0, 21.0]

    def test_hymanANDfurnessModel(self):
        import numpy as np
        import pandas as pd
        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']
        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)  

        senderIDs = go.getListOfNodeIDs(myNW, actors=['producer'],products=['milk'])
        receiverIDs = go.getListOfNodeIDs(myNW, actors=['consumer'],products=['milk'])
        allcombIDs1,allcombIDs2 = go.getAllCombinations(senderIDs,receiverIDs,order='1st')
        myEdges4Graph = go.getEdgeID(myNW,allcombIDs1,allcombIDs2)
        sendingMilk = [10,50,40]
        receivingMilk = [30,30,40]
        go.addAttr2ExistingNodes(myNW,senderIDs,'output',sendingMilk)
        go.addAttr2ExistingNodes(myNW,receiverIDs,'input',receivingMilk)

        # building distance matrix from scratch
        myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        myDF = pd.DataFrame(myData,index=loc)

        assert go.addAttr2Edges(myNW,myEdges4Graph, myDF.values.flatten(),attr='distance')
        myTDs = go.calcPotTransportDistances(myNW, listOfSenderIDs=senderIDs, listOfReceiverIDs=receiverIDs, nrOfValues=5)

        test = np.array([[ 4.89436823,4.48960544,0.61597657],[23.1959832,  23.56995789,  3.23381242],[1.90964857,  1.94043667, 36.15021101]])
        assert np.sum(np.abs(go.hymanModel(myNW, listOfSenderIDs=senderIDs, listOfReceiverIDs=receiverIDs, transportDistance=myTDs[0], tolerance = 0.01)-test)) < 0.01

    def test_calibrationProcess(self):
        pass
'''     
test calibrationProcess
'''