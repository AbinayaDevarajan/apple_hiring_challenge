
import matplotlib.pyplot as plt
import sys
import networkx
sys.path.append('../utils')
sys.path.append('../conf')
sys.path.append('../common')
from  input_reader import AutomationInputReader
from  command_dictionary import command_description_dict
import argparse

"""
Generic Graph ADT Template
Graph ADT for constructing 
"""


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __eq__(self, other):
        return self.u == self.u and self.v == other.v

    def __hash__(self):
        return hash(str(self.u) + "-->" + str(self.v))

    def __str__(self):
        return str(self.u) + "-->" + str(self.v)


class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def find_isolated_vertices(self):
        """ returns a list of isolated vertices. """
        graph = self.__graph_dict
        isolated = []
        for vertex in graph:
            print(isolated, vertex)
            if not graph[vertex]:
                isolated += [vertex]
        return isolated

    def get_children(self,vertex):
        graph = self.__graph_dict
        return graph[vertex]

    def get_graph_dict(self):
        return self.__graph_dict



def execute_automation():
    parser = argparse.ArgumentParser(
        description='Script to install the dependencies')
    parser.add_argument(
        '--input_file',
        help='This is the input configuration file to be parsed.')
    args = parser.parse_args()
    file_name = args.input_file
   
    dependency_graph = G = networkx.DiGraph()

    
    for command_line in AutomationInputReader(file_name).get_command_action_list():
        if (command_line[0] not in command_description_dict):
            print("The command is an invalid command not found in the specification, skipping it")
            continue
        else:
            if (command_line[0]=='DEPEND'):
                print("Processing the dependencies", command_line[1],command_line[2:len(command_line)])
                dependency_graph.add_node(command_line[1])
                for vertex in range(2,len(command_line)):
                    print("processing the element",command_line[vertex])   
                    dependency_graph.add_node(command_line[vertex])
                    dependency_graph.add_edge(command_line[1], command_line[vertex])
    print (str(dependency_graph))
    
    networkx.draw(G, with_labels=True, edge_color='r')
    plt.show()

    print(dependency_graph.edges())
    #print(dependency_graph.get_graph_dict())
    #print(dependency_graph.find_all_paths("BROWSER", "NETCARD"))

if __name__ == "__main__":
    execute_automation()
    
