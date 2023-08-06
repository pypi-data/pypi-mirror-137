'''
NEED TO LEARN MORE ABOUT CLASSES... !


purpose: create graph from specifications of the user with 
generally used node properties used in supply chain models



Methods:
----------
directly operating on network
* createGraph - the graph is created with node attributes
    'actors','locations','products'
* getListOfNodeIDs - returns a list of nodeIDs with the corresponding
    attributes, used for editing information on the graph
* getNodeIDswAttr - returns a tuple of (nodeIDs,attributes) with the
    corresponding attributes, used for editing information on the graph
* addAttr2ExistingNodes - adds a user specified attribute to the nodes
    of the network
* addAttr2Edges - adds a user specified attribute to the edges of the network
* getEdgeID - returns the IDs for the edges on the graph, given the user
    specified nodes (IDs given by getListOfNodeIDs) on the network
* getEdgesAttr - returns a list of attributes of the edges
    (IDs given by getEdgeID) specified by the user
* getEdgeIDswAttr - returns a tuple of
    ((edge ID, attribute) = (node out,node in, attribute))
    of the edges (IDs given by getEdgeID) specified by the user
* getExistingAttrs - returns a list of existing attributes on the graph
    (either nodes or edges)

toolkit for handling attributes on the network
* combineActorBrand - if an actor consists of different subtypes
    (e.g. warehouse and brand(ALDI,REWE, etc.)), then this function helps
    with a fast way of creating additional actors, before creating the network
* convertLoT2NTs - functions like getEdgeIDswAttr, return a list of
    tuples, but only a part of this is needed. This function accepts a list
    of tuples as input and returns 2 lists with the same order as before.
* convertTup2LoT - functions like addAttr2ExistingNodes, accept a list
    of tuples as input, but only a list available. This function accepts
    2 lists as input and returns a list on tuples with the same order as
    before.
* getAllCombinations - getEdgeID is a function that has the corresponding
    nodes as input, and returns a direct  1-to-1 list (node out, node in).
    If all possible combinations of edges between 2 nodes are to be
    returned, this function helps with that.
* convertMatrix - 2 applications:
    1. for calibration might be needed if calibration measure is
    of different dimension as the calculated flows
    2. if a matrix with redundant information needs to be created
    from a matrix with minimum information (e.g. similar geographical
    distances between nodes to be put into a distance matrix)

mapping raw data objects to network data objects
* proxyModel - simple fraction model. If data for correlated variable
    is available, this model may be used to use the proxy data to model
    the data in question
    (e.g. modellled data = produced eggs, proxy data= number of laying hens)
* getDistMatrix - accesses the graph for attribute 'distance' for
    user-specified nodes, return a dataframe containing information of the
    geographical distance between the locations of given nodes (needs to be
    entered into the graphe beforehand via the function addAttr2Edges)
    NOTE that the attribute 'distance' needs to be defined on the edges
    of the participating nodes.
* optFlow, minOptFlowForBeta - calculating and minimizing the optimal
    flow given supply and demand of a product and the distance between
    participating nodes. Needed for calculating minimum transport
    distance (see calcPotTransportDistances).
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
* propFlow - calculating the proportional flow given supply and demand
    of a product and the distance between participating nodes. Needed for
    calculating maximum transport distance (see calcPotTransportDistances).
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
* furnessModel - given geographical distance, supply and demand of
    the participating nodes and the free parameter (resistance factor)
    beta this function returns the flow between given nodes
    (beta needs to be determined by hymanModel / calibration)
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'input' needs to be defined on the nodes
        demanding the product.
* calcPotTransportDistances - calculates the range of possible average
    transport distances and returns a list of values within this interval.
    The number of returned values from this interval may be specified by
    the user (needed for hymanModel to determine beta for furnessModel).
    NOTE that each of the returned values are POSSIBLE average
    transport distance. The best one still needs to be determined(see
    calibration).
    NOTE that the attribute 'distance' needs to be defined on the
        edges of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'input' needs to be defined on the nodes
        demanding the product.
* hymanModel - calculates resistance factor beta given a transport
    distance. Returns the flow between participating nodes of supply and
    demand.
    NOTE that each of the returned values are POSSIBLE average transport
        distance. The best one still needs to be determined(see calibration).
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'input' needs to be defined on the nodes
        demanding the product.
* getWeightedDist - returns the average transport distance, given the flow
    between participating nodes of supply and demand.
    NOTE that each of the returned values are POSSIBLE average
        transport distance. The best one still needs to be determined(see
        calibration).
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'input' needs to be defined on the nodes
        demanding the product.
* calibration - function for calculating the best configuration of given
    transport distances and corresponding flows. A number of possible
    average transport distances are given by the function
    calcPotTransportDistances. The function hymanModel calculates
    the corresponding flows.
    Now this needs to be calibrated against a measure to determine which
    average transport distance fits best the calibration measure.
    This function accepts a 4D-Tensor of all flows as input
    [supply,demand,product,transport distance] and the calibration measure
    in question.
    NOTE that each of the returned values are POSSIBLE average
        transport distance. The best one still needs to be determined(see
        calibration).
    NOTE that the attribute 'distance' needs to be defined on the edges
        of the participating nodes.
    NOTE that the attribute 'output' needs to be defined on the nodes
        supplying the product.
    NOTE that the attribute 'input' needs to be defined on the nodes
        demanding the product.

* calibrationOLD - deprecated function for calculating the best
    configuration of given transport distances and corresponding flows.
    MCMC simulation. Only here for reasons of nostalgia.




===============================================================================
'''

import networkx as nx
from networkx.classes.digraph import DiGraph
#from networkx.classes.graph import Graph
import numpy as np
from itertools import chain
from ipfn import ipfn
from scipy import optimize
import warnings
warnings.filterwarnings("ignore")

class SCgraph(DiGraph):
    '''
    purpose: create graph from specifications of the user with 
    generally used node properties used in supply chain models



    Methods:
    ----------
    directly operating on network
    * createGraph - the graph is created with node attributes
    'actors','locations','products'
    * getListOfNodeIDs - returns a list of nodeIDs with the corresponding
        attributes, used for editing information on the graph
    * getNodeIDswAttr - returns a tuple of (nodeIDs,attributes) with the
        corresponding attributes, used for editing information on the graph
    * addAttr2ExistingNodes - adds a user specified attribute to the nodes
        of the network
    * addAttr2Edges - adds a user specified attribute to the edges of the
        network
    * getEdgeID - returns the IDs for the edges on the graph, given the
        user specified nodes (IDs given by getListOfNodeIDs) on the network
    * getEdgesAttr - returns a list of attributes of the edges
        (IDs given by getEdgeID) specified by the user
    * getEdgeIDswAttr - returns a tuple of
        ((edge ID, attribute) = (node out,node in, attribute))
        of the edges (IDs given by getEdgeID) specified by the user
    * getExistingAttrs - returns a list of existing attributes on the
        graph (either nodes or edges)

    toolkit for handling attributes on the network
    * combineActorBrand - if an actor consists of different subtypes
        (e.g. warehouse and brand(ALDI, REWE, etc.)), then this function
        helps with a fast way of creating additional actors, before creating
        the network
    * convertLoT2NTs - functions like getEdgeIDswAttr, return a list of
        tuples, but only a part of this is needed. This function accepts
        a list of tuples as input and returns 2 lists with the same order as
        before.
    * convertTup2LoT - functions like addAttr2ExistingNodes, accept a list of
        tuples as input, but only a list available. This function accepts 2
        lists as input and returns a list on tuples with the same order as
        before.
    * getAllCombinations - getEdgeID is a function that has the corresponding
        nodes as input, and returns a direct  1-to-1 list (node out, node in).
        If all possible combinations of edges between 2 nodes are to be
        returned, this function helps with that.
    * convertMatrix - 2 applications:
        1. for calibration might be needed if calibration measure is of
            different dimension as the calculated flows
        2. if a matrix with redundant information needs to be created from
            a matrix with minimum information (e.g. similar geographical
            distances between nodes to be put into a distance matrix)

    mapping raw data objects to network data objects
    * proxyModel - simple fraction model. If data for correlated variable
        is available, this model may be used to use the proxy data to model
        the data in question (e.g. modellled data = produced eggs,
        proxy data= number of laying hens)
    * getDistMatrix - accesses the graph for attribute 'distance'
        for user-specified nodes, return a dataframe containing information
        of the geographical distance between the locations of given nodes
        (needs to be entered into the graphe beforehand via the
        function addAttr2Edges)
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
    * optFlow, minOptFlowForBeta - calculating and minimizing the optimal
        flow given supply and demand of a product and the distance between
        participating nodes. Needed for calculating minimum transport
        distance (see calcPotTransportDistances).
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the nodes
            supplying the product.
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
    * propFlow - calculating the proportional flow given supply and demand
        of a product and the distance between participating nodes. Needed
        for calculating maximum transport distance
        (see calcPotTransportDistances).
        NOTE that the attribute 'distance' needs to be defined on the
            edges of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the
            nodes supplying the product.
        NOTE that the attribute 'distance' needs to be defined on the
            edges of the participating nodes.
    * furnessModel - given geographical distance, supply and demand of the
        participating nodes and the free parameter (resistance factor)
        beta this function returns the flow between given nodes
        (beta needs to be determined by hymanModel / calibration)
        NOTE that the attribute 'distance' needs to be defined on the
            edges of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the
            nodes supplying the product.
        NOTE that the attribute 'input' needs to be defined on the
            nodes demanding the product.
    * calcPotTransportDistances - calculates the range of possible
        average transport distances and returns a list of values within
        this interval. The number of returned values from this interval may
        be specified by the user (needed for hymanModel to determine
        beta for furnessModel).
        NOTE that each of the returned values are POSSIBLE average
        transport distance. The best one still needs to be determined
        (see calibration).
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the nodes
            supplying the product.
        NOTE that the attribute 'input' needs to be defined on the nodes
            demanding the product.
    * hymanModel - calculates resistance factor beta given a transport
        distance. Returns the flow between participating nodes of supply
        and demand.
        NOTE that each of the returned values are POSSIBLE average transport
            distance. The best one still needs to be determined(see calibration).
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the nodes
            supplying the product.
        NOTE that the attribute 'input' needs to be defined on the nodes
            demanding the product.
    * getWeightedDist - returns the average transport distance, given the
        flow between participating nodes of supply and demand.
        NOTE that each of the returned values are POSSIBLE average
            transport distance. The best one still needs to be determined
            (see calibration).
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the nodes
            supplying the product.
        NOTE that the attribute 'input' needs to be defined on the nodes
            demanding the product.
    * calibration - function for calculating the best configuration of given
        transport distances and corresponding flows. A number of possible
        average transport distances are given by the function
        calcPotTransportDistances. The function hymanModel calculates
        the corresponding flows.
        Now this needs to be calibrated against a measure to determine
        which average transport distance fits best the calibration measure.
        This function accepts a 4D-Tensor of all flows as input
        [supply,demand,product,transport distance]
        and the calibration measure in question.
        NOTE that each of the returned values are POSSIBLE average
        transport distance. The best one still needs to be determined(see
        calibration).
        NOTE that the attribute 'distance' needs to be defined on the edges
            of the participating nodes.
        NOTE that the attribute 'output' needs to be defined on the nodes
            supplying the product.
        NOTE that the attribute 'input' needs to be defined on the nodes
            demanding the product.

    * calibrationOLD - deprecated function for calculating the best
        configuration of given transport distances and corresponding flows.
        MCMC simulation. Only here for reasons of nostalgia.
    '''
    
    myAttributes = ['actors', 'locations', 'products']

    def __init__(
            self,
            actors: list,
            locations: list,
            products: list,
            *args,
            **kwargs
    ):
        """
        purpose: create a directed graph with standard attributes for supply chain modelling:
        on creation of the graph a number of nodes are created based on the input lists.
        The nodes contain all possible combinations of the elements from the input list.
        The attributes are: 'actor','location','product'

        :param actors: a list of participating actors (list of string)
        :param locations: a list of locations involved (e.g. Landkreise in Germany)
        :param products: a list of products being transported (e.g. vegetables, eggs, ...)

        :return: Graph with nodes containing all possible combinations of actors, locations
        and products

        example:
        from supplychainmodulator import graphoperations as go

        prod = ['milk','beer','schnaps']
        act = ['producer','consumer','warehouse','store']
        loc = ['BER','SXF','TXL']

        myNW = go.createGraph(listOfActors=act,listOfLocations=loc,\\
            listOfProducts=prod)




        =======================================================================
        """
        super(SCgraph, self).__init__(*args, **kwargs)
        self.actors = actors
        self.products = products
        self.locations = locations

        isItListA = isinstance(self.actors, list)
        isItListP = isinstance(self.products, list)
        isItListL = isinstance(self.locations, list)
        
        if not isItListA:
            raise Exception('actors ist not a list!')
        if not isItListP:
            raise Exception('products ist not a list!')
        if not isItListL:
            raise Exception('locations ist not a list!')

        howManyActors = len(self.actors)
        howManyProducts = len(self.products)
        howManyLocations = len(self.locations)
    
        if howManyActors == 0:
            raise Exception(
                'incorrect parameter: '
                'actors should be a list, but it is: %20s' % (actors)
            )
        if howManyProducts == 0:
            raise Exception(
                'incorrect parameter: '
                'products should be a list, but it is: %20s' % (products)
            )
        if howManyLocations == 0:
            raise Exception(
                'incorrect parameter: '
                'locations should be a list, but it is: %20s' % (locations)
            )

        
        

        # create names for node attributes
        # (currently hardcoded, since this never changes (as of this moment))
        actor = self.myAttributes[0]
        location = self.myAttributes[1]
        product = self.myAttributes[2]

        '''
        go through all permutations and create nodes with 
        these 3 attribute names and a list of the 
        corresponding 3 attribute contents
        '''
        nodes = zip(
            range(
                len(self.actors)*len(self.locations)*len(self.products)
            ), [
                {actor:al,product:pl,location:ll}
                for al in self.actors
                for pl in self.products
                for ll in self.locations
            ]
        )
        
        self.add_nodes_from(list(nodes))

    def combineActorBrand(
            self,
            actor: str,
            brand: list
    ) -> list:
        """
        purpose: if an actor has a brand, but is the same type, this can be used
        to give it the correct designation
        (e.g. retailer: Warehouse_ALDI or Store_ALDI a.s.o.)
        usually such an actor type has multiple brands

        :param actor: an element of the actor list
        :param brand: a list of brands for different actors: actor_suffix

        :return: a combined list

        example:
        from supplychainmodelhelper import graphoperations as go

        act = ['producer','consumer','warehouse','store']

        newActors = go.combineActorBrand(actor='warehouse',brand=['ALDI','REWE','LIDL'])

        act.remove('warehouse')
        act.extend(newActors)

        print(act)


        ===============================================================================================
        """
        # TODO: sanity check if given actor is in graph
        # TODO: remove actor from graph, add new actors to graph
    
        combinedList = [actor + "_" + go for go in brand]
        return combinedList