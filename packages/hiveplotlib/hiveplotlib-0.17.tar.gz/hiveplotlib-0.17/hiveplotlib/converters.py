# Gary Koplik
# gary<dot>koplik<at>geomdata<dot>com
# December, 2021
# converters.py

"""
Converters from various data structures to ``hiveplotlib``-ready structures.
"""


from hiveplotlib import Node
import numpy as np


def networkx_to_nodes_edges(graph: "networkx.classes.graph.Graph instance"):
    """
    Take a ``networkx`` graph and return a list of ``hiveplotlib.Node`` instances and an ``(n, 2)`` ``np.ndarray`` of
    edges.

    :param graph: ``networkx`` graph.
    :return: ``list`` of ``Node`` instances, ``(n, 2)`` ``np.ndarray`` of edges.
    """

    nodes = [Node(unique_id=i, data=data) for i, data in list(graph.nodes.data())]
    edges = np.array(graph.edges)
    return nodes, edges
