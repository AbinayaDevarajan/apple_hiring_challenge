

from types import SimpleNamespace
import argparse
from collections import OrderedDict
import matplotlib.pyplot as plt
import sys
import networkx
from networkx import algorithms
sys.path.append('../utils')
sys.path.append('../conf')
sys.path.append('../common')
from  input_reader import AutomationInputReader
from  command_dictionary import command_description_dict, command_dictionary
available_commands = SimpleNamespace(**command_dictionary)

"""
Generic Graph ADT Template
Graph ADT for constructing Graphs


This program uses networkx and matplotlib for visualization 
_____________________________________________________________________________________

pip install matplotlib
pip install networkx
for the usage 
usage: installation_automation.py [-h] [--input_file INPUT_FILE]

Script to install the dependencies

optional arguments:
  -h, --help            show this help message and exit
  --input_file INPUT_FILE
                        This is the input configuration file to be parsed.


The algorithm used is DAG -- Directed acyclic graph algorithm for constructing the graphs 
for the traversal:
    dfs_post_order is used 
    - get_successors is used  detect the successors and the incoming edges for finding out the 
    dependencies

"""


class Edge:
    def __init__(self, a, b):
        self.start = a
        self.end = b

    def __eq__(self, other):
        return self.start == self.start and self.end == other.end

    def __hash__(self):
        return hash(str(self.start) + "-->" + str(self.start))

    def __str__(self):
        return str(self.start) + "-->" + str(self.end)


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


installed_items = OrderedDict()
installed_order=[]
def execute_automation(test_automation=False,test_automation_file=None):

    file_name =""
    order = 1 
    if not test_automation:
        parser = argparse.ArgumentParser(
            description='Script to install the dependencies')
        parser.add_argument(
            '--input_file',
            help='This is the input configuration file to be parsed.')
        args = parser.parse_args()
        file_name = args.input_file
        
    else:
        file_name = test_automation_file
    
    dependency_graph = G = networkx.DiGraph()
    for command_line in AutomationInputReader(file_name).get_command_action_list():
        print(" ".join(map(str, command_line)))
        if (command_line[0] not in command_description_dict):
            print("The command is an invalid command not found in the specification, skipping it")
            continue
        else:
            if (command_line[0] == available_commands.dependency_build):
                dependency_graph.add_node(command_line[1])
                for vertex in range(2,len(command_line)):
                    dependency_graph.add_node(command_line[vertex])
                    dependency_graph.add_edge(command_line[1], command_line[vertex])

            elif (command_line[0] == available_commands.installation):
                try:
                   
                    for item in list(networkx.dfs_postorder_nodes(dependency_graph, command_line[1])):
                        if (item not in installed_items):
                            installed_items[item] = order 
                           
                            print("\t Installing ", item)
                            order = order + 1 
                        elif(command_line[1] in installed_items):
                            print("\t{} is already installed.".format(item))
                    
                except (KeyError, networkx.exception.NetworkXError):
                    print("\t Installing ", command_line[1])
                    installed_items[command_line[1]] = order
                    order = order + 1 

            elif (command_line[0] == available_commands.list_installed_components):
                for key, value in installed_items.items():
                    print("\t",key)

            elif (command_line[0] == available_commands.uninstallation):
                dep_list  =list(dependency_graph.in_edges(command_line[1]))
                
                successors = list(dependency_graph.successors(command_line[1]))
            
                for succ in  successors:
                    dependency_graph.remove_edge(command_line[1],succ)
        
                if len(dep_list)==0:

                    try:
                        removed_value = installed_items.pop(command_line[1])
                        
                        print("\t Removing {}".format(command_line[1]))
                        for successor in successors:
                            dep_succ = list(dependency_graph.in_edges(successor))
                
                            if(len(dep_succ) == 0):
                                removed_value = installed_items.pop(successor)
                                print("\t Removing {}".format(successor))
                    except KeyError:
                        print("\t{} is not installed.".format(command_line[1]))

                    
                
                else:
                    print("\t{} is still needed.".format(command_line[1]))

            elif (command_line[0] == available_commands.terminate_program):
                sys.exit(0)       

    """
    TESTS
    ____________________________________________________________________________
    print(networkx.ancestors(dependency_graph,"NETCARD"))
    print(networkx.algorithms.dfs_successors(dependency_graph, "BROWSER"))
    print(networkx.algorithms.dfs_successors(dependency_graph, "DNS"))
    print(list(networkx.dfs_postorder_nodes(dependency_graph, "DNS")))
    print(list(networkx.dfs_postorder_nodes(dependency_graph, "BROWSER")))
    print(list(networkx.dfs_postorder_nodes(dependency_graph, "TCPIP")))

    print(dependency_graph.edges())
    print(dependency_graph.successors("BROWSER"))
    for item in dependency_graph.successors("BROWSER"):
        print(item)

    print(dependency_graph.in_edges("BROWSER"))

    for item in dependency_graph.in_edges("NETCARD"):
        print(item)

    print(networkx.algorithms.dfs_successors(dependency_graph, "DNS"))
    print(networkx.algorithms.dfs_successors(dependency_graph, "NETCARD"))
    print(networkx.algorithms.dfs_successors(dependency_graph, "TELNET"))
    
    #print(dependency_graph.get_graph_dict())
    #print(dependency_graph.find_all_paths("BROWSER", "NETCARD"))
    """

if __name__ == "__main__":
    installed_list = []
    execute_automation(test_automation=False)
    
