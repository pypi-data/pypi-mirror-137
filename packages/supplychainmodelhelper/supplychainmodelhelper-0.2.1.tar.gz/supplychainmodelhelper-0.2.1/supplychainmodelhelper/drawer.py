"""
purpose: simple drawing extension, specialised for supply chain modelling

version 0:
    boundary conditions:
        stages: order of actors are drawn as stages
            example:
            actors = ['producer', 'consumer']
            -> producer are on stage 1, consumer are on stage 2 of this
            2-stages-graph

        assumption: output = input = node size
            the smaller the node the less the output/input of the node

        heatmap for <<chosen edge_label>>(if its a number): with colorbar

        colormap for different products

"""
import itertools
import operator
import warnings

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from supplychainmodelhelper import graphoperations as go


class Drawer:
    """
    purpose: draw a supply chain graph
    assumption for standard view (V1):
    layers: actor type defines the number of stages (e.g. producer, warehouse,
    store, consumer)
    color of the edges are heatmap distributed -> log10?(amount)
    - from blue to red
    node size is output/input (possibly log)
    products can only be seen one at a time
    """

    # std_sc_attr = ['actor','location','product']
    # TODO: multiple products

    def __init__(self, SCGraph):
        """
        purpose: initialize drawer with standard view

        :param SCGraph: the graph to be drawn
        """
        # TODO: check if graph has all necessary attributes!

        self.SCGraph = SCGraph
        # for it to work these attributes needed to be defined on the graph
        needed_nodes = ['actor', 'output', 'input']
        needed_edges = 'weight'

        found_nodes = [
            node_type for node_type
            in go.getExistingAttrs(self.SCGraph,gtype='nodes')
            if node_type in needed_nodes
        ]

        # error message if discrepancy is found
        # TODO: this is a hot fix. check for all attributes specifically
        if len(found_nodes) < len(needed_nodes):
            raise Exception(
                "found these node types: " +
                str(found_nodes) +
                ", but need these: " +
                str(needed_nodes)
            )
        if needed_edges not in go.getExistingAttrs(
                self.SCGraph,
                gtype='edges'
        ):
            raise Exception(
                "Please add edge attribute: " +
                needed_edges +
                "to the graph."
            )

    def draw_it(self, product, actor_type_names=None):
        """
        purpose: execute drawing of sc graph
        :param product: choose the name of the product to be shown.
        :param actor_type_names: (optional) list of actor types as defined in
        given graph. Expected to be found in node_attribute "actor".
        choose names of actor types (minimum 2).

        :return: image of graph

        TODO potential parameters:
            product -> multiple products if no product is chosen???
            node bg color = treshold color, size
            node fg color
            treshold value
            other heatmaps for edges
            labeling nodes with locations
            no stages
        """
        # get the ids of the nodes to be drawn
        node_ids_to_draw = go.getListOfNodeIDs(
            SCGraph=self.SCGraph,
            products=product,
            actors=actor_type_names
        )

        # check the given list of actor_type_names
        if actor_type_names:
            if isinstance(actor_type_names, list):
                if len(actor_type_names) < 2:
                    raise Exception(
                        "number of elements in 'actor_type_names' "
                        "should be at least 2!"
                    )
            else:
                raise Exception(
                    "the parameter 'actor_type_names' "
                    "should be a list"
                )

        # prepping for different aspects of the process of drawing
        node_positions, node_stages, node_stage_names = self.node_position(
            filtered_nodes=node_ids_to_draw
        )
        sm, edge_options = self.edge_color()
        node_list, node_size = self.node_size()
        node_size_avg = sum(node_size) / len(node_size)
        node_size_max = max(node_size)
        node_size_min = min(node_size)

        # backgroung nodes drawing
        import math
        fig, ax = plt.subplots()
        nx.draw(self.SCGraph,
                node_positions,
                nodelist=node_list,
                node_color='grey',
                node_size=node_size_avg,
                **edge_options,
                ax=ax
                )

        # foreground nodes drawing with edges
        nx.draw_networkx_nodes(self.SCGraph,
                               node_positions,
                               node_color='k',
                               nodelist=node_list,
                               node_size=node_size
                               )

        # adding actor labels
        ax.tick_params(left=True,
                       bottom=False,
                       labelleft=True,
                       labelbottom=False
                       )

        # set labels for actors
        ax.set_yticks(node_stages)
        ax.set_yticklabels(node_stage_names)

        cbar = plt.colorbar(sm)
        cbar.set_label('transported amount of wares in tons')

        plt.axis('on')

        legend_info = self.legend_node_size(
            math.sqrt(math.pi * node_size_min),
            math.sqrt(math.pi * node_size_avg),
            math.sqrt(math.pi * node_size_max)
        )
        ax.legend(handles=legend_info, loc=9, bbox_to_anchor=(1.3, 0.12))
        ax.get_legend().set_title("throughput")
        plt.show()

    @staticmethod
    def legend_node_size(mymin, myavg, mymax):
        """
        purpose: adjust the size of a node according to output / input of node

        :param mymin: node size minimum in area px
        :param myavg: node size average in area px
        :param mymax: node size maximum in area px

        :return: the legend with all chosen colors, markers, sizes and labels
        """
        mylegend = [
            Line2D([0], [0],
                   markerfacecolor='k',
                   marker='o',
                   markersize=mymin + 1,
                   label='min',
                   color='w'
                   ),
            Line2D([0], [0],
                   markerfacecolor='gray',
                   marker='o',
                   markersize=myavg,
                   label='avg',
                   color='w'
                   ),
            Line2D([0], [0],
                   markerfacecolor='k',
                   marker='o',
                   markersize=mymax,
                   label='max',
                   color='w'
                   )
        ]
        return mylegend

    def node_position(self, node_attr='actor', filtered_nodes=None):
        """
        purpose: return node position on several stages based on content of
        graph(node_attr)

        standard: actors of the same type on the same stage (in the order as
        defined by user)

        :param node_attr: (optional, default: actor) attribute of nodes in
        graph that should be displayed. If ignored, the actors are shown.
        :param filtered_nodes: (optional, default: None) input for list of
        specified node IDs. In ignored, all nodes are chosen.

        :return: position of nodes for drawing: dict(node_ids:(xcoord,ycoord))

        TODO: node_attr - what if other attribute than "actor" is chosen?
            use case (product): show interaction between food processors (e.g.
            sugar beets -> sugar -> pastries)
            use case (location): show how central a node is
        TODO: current layout: grid (senders top, receivers bottom) --> new
        layouts?
        """

        # list of tuples with node ids and actor content
        node_ids_with_actors = go.getNodeIDswAttr(
            SCGraph=self.SCGraph,
            nameOfAttr=node_attr,
            listOfNodeIDs=filtered_nodes
        )

        # list of lists, ordered by content of actor
        # each element of the list is a list with the same type of actor

        stagewise_actors = [
            list(group) for _, group
            in itertools.groupby(
                node_ids_with_actors,
                operator.itemgetter(1)
            )
        ]
        nr_of_stages = len(stagewise_actors)
        nr_of_layers = nr_of_stages - 1

        # check if edges between stages contain attribute 'weight'
        for layer in range(nr_of_layers):
            sender_nodes = [i[0] for i in stagewise_actors[layer]]
            receiver_nodes = [i[0] for i in stagewise_actors[layer + 1]]
            comb_sender, comb_receiver = go.getAllCombinations(
                sender_nodes,
                receiver_nodes
            )
            edges_to_be_drawn = go.convertTup2LoT(comb_sender, comb_receiver)

            existing_edges_in_layer = go.getEdgeIDswAttr(
                SCGraph=self.SCGraph,
                attr='weight'
            )
            sid, rid, _ = go.convertLoT2NTs(existing_edges_in_layer)
            existing_edge_ids_in_layer = go.convertTup2LoT(sid, rid)

            found_all_edges_to_be_drawn = all(
                [
                    True if el in existing_edge_ids_in_layer
                    else False
                    for el in edges_to_be_drawn
                ]
            )
            if not found_all_edges_to_be_drawn:
                raise Exception(
                    "ERROR! at least 1 of the edges between "
                    "actors/products to be drawn do NOT contain "
                    "the attribute 'weight'! please check edge "
                    "ids of corresponding nodes!"
                )

        pos = dict()
        # handle each stage sorted by actors
        all_stage_coords = []
        all_stage_names = []
        for st_id, stage in enumerate(stagewise_actors):
            # syntax : (node_id, (x-coord, y-coord)
            # x-coord = for each node ordered by node id
            # y-coord = stage

            name_of_stage = ''.join(
                list(
                    map(str, set([j for (i, j) in stage]))
                )
            )
            my_stage_coord = nr_of_stages - st_id
            pos.update(
                (nid, (i, my_stage_coord)) for i, (nid, _) in enumerate(stage)
            )

            # log all possible coordinates for later use, when drawing
            all_stage_coords.append(my_stage_coord)
            all_stage_names.append(name_of_stage)

        return pos, all_stage_coords, all_stage_names

    def node_size(self, node_attr=['output', 'input']):
        """
        purpose: node size should depend on output/throughput/input of nodes

        :param node_attr: (optional, default: ['output','input'])
        node attribute for determining node_size. needs to be defined on all
        nodes to be drawn. can be 1 attribute(str) or multiple (list of str).

        :return: node options for drawing
        """

        if isinstance(node_attr, list):
            do_they_exist = [
                attr for attr in node_attr
                if attr in go.getExistingAttrs(
                    self.SCGraph,
                    gtype='nodes'
                )
            ]
            if not do_they_exist:
                raise Exception(
                    "no attribute by the names: " +
                    str(node_attr) +
                    " exist on the graph!"
                )
            elif len(do_they_exist) < len(node_attr):
                warnings.warn(
                    "only " +
                    str(do_they_exist) +
                    " of " +
                    str(node_attr) +
                    " are attributes of the graph!"
                )
            node_list = []
            node_size = []
            for attr in node_attr:
                nodes, content = zip(
                    *nx.get_node_attributes(self.SCGraph, attr).items()
                )
                node_list = node_list + list(nodes)
                node_size = node_size + list(content)
        elif isinstance(node_attr, str):
            node_list, node_size = zip(
                *nx.get_node_attributes(self.SCGraph, node_attr).items()
            )

        return node_list, node_size

    def edge_color(self, weight='weight', color_map=plt.cm.plasma):
        """
        purpose: edge color is defined by minimum and maximum of amount of
        wares transported (std: weight)

        :param weight: (optional, default: 'weight'): edge attribute for
        coloring edges via heatmap
        :param color_map: (optional, default: plt.cm.coolwarm) blue =
        minimum, red = maximum, change only if matplotlibs colormap are
        understood!

        :return: colorbar_data, option_data for drawing
        """
        # check if weight exists on graph
        if not weight in go.getExistingAttrs(self.SCGraph, gtype='edges'):
            raise Exception(
                "given edge attribute: " +
                str(weight) +
                " does not exist in the graph"
            )

        # unzip edge ids and their respective content
        edges, weights = zip(*nx.get_edge_attributes(
            self.SCGraph, weight
        ).items())

        # for defining boundaries of color map
        min_weights = min(weights)
        max_weights = max(weights)

        edge_options = {
            "edgelist": edges,
            "edge_color": weights,
            "width": 4,
            "edge_cmap": color_map,
            "with_labels": False,
        }

        sm = plt.cm.ScalarMappable(
            cmap=color_map,
            norm=plt.Normalize(
                vmin=min_weights, vmax=max_weights
            )
        )
        sm._A = []

        return sm, edge_options
