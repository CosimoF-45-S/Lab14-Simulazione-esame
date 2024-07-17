from database import DAO
import networkx as nx

graph = nx.Graph()

nodes = DAO.DAO.getNodesTreZ()
graph.add_nodes_from(nodes)

edges = DAO.DAO.getEdgesTreZ()
graph.add_weighted_edges_from(edges)


print(graph.number_of_nodes())
print(graph.number_of_edges())

connected = list(nx.connected_components(graph))
max = max(connected, key=len)
print(max)
