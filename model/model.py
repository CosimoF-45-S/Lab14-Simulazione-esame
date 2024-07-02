import copy
import itertools

import networkx as nx
from database import DAO
class Model:
    def __init__(self):
        self.graph = nx.DiGraph()

    def creaGrafo1(self):

        nodi = DAO.DAO.getNodes()
        self.graph.add_nodes_from(nodi)

        edges = DAO.DAO.getEdges()
        for edge in edges:
            self.graph.add_edge(edge[0], edge[1], weight=edge[2])

        output_list = []
        output_list.append(self.graph.number_of_nodes())
        output_list.append(self.graph.number_of_edges())

        sorted_edges = sorted(self.graph.edges(data=True), key=lambda x: x[2]["weight"])
        output_list.append(sorted_edges[0][2]["weight"])
        output_list.append(sorted_edges[-1][2]["weight"])

        return output_list

    def creaGrafo2(self):

        nodi = DAO.DAO.getNodes()
        self.graph.add_nodes_from(nodi)

        node_tuple = list(itertools.combinations(nodi, 2))
        for t in node_tuple:
            weightTo = DAO.DAO.getWeightTo(t[0], t[1])
            if weightTo is not None:
                self.graph.add_edge(t[0], t[1], weight=weightTo)
            weightFrom = DAO.DAO.getWeightFrom(t[0], t[1])
            if weightFrom is not None:
                self.graph.add_edge(t[1], t[0], weight=weightFrom)

        output_list = []
        output_list.append(self.graph.number_of_nodes())
        output_list.append(self.graph.number_of_edges())

        sorted_edges = sorted(self.graph.edges(data=True), key=lambda x: x[2]["weight"])
        output_list.append(sorted_edges[0][2]["weight"])
        output_list.append(sorted_edges[-1][2]["weight"])

        return output_list

    def handle_count(self, soglia):
        num_min = 0
        num_max = 0
        for edge in self.graph.edges(data=True):
            if edge[2]["weight"] > soglia:
                num_max += 1
            elif edge[2]["weight"] < soglia:
                num_min += 1
        return num_min, num_max

    def handlepath(self, soglia):
        self.maxdistance = 0
        self.bestpath = []

        for nodo in self.graph.nodes():
            last_node = nodo
            self.recursive(last_node, [], soglia)

        printable_path = self.printablepath(self.bestpath)

        return self.maxdistance, printable_path

    def recursive(self, last_node, partial, soglia):

        archiammissibili = self.getArchiAmmissibili(last_node, soglia, partial)

        if not archiammissibili:
            distTot = self.calcolaDistTot(partial)
            if distTot > self.maxdistance:
                self.maxdistance = distTot
                self.bestpath = copy.deepcopy(partial)
        else:
            for edge in archiammissibili:
                partial.append(edge)
                self.recursive(edge[1], partial, soglia)
                partial.pop()



    def getArchiAmmissibili(self, last_node, soglia, partial):
        output = []
        for edge in self.graph.edges(last_node, data=True):
            if edge[2]["weight"] >= soglia and edge not in partial:
                output.append(edge)
        return output

    def calcolaDistTot(self, partial):
        distTot = 0
        for edge in partial:
            dist = edge[2]["weight"]
            distTot += dist
        return distTot

    def printablepath(self, path):
        result = []
        for edge in path:
            result.append(f"{edge[0]}->{edge[1]}, peso: {edge[2]['weight']}")
        return result
