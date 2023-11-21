from heapq import heappop, heappush, heapify
from collections import defaultdict
from unionfind import unionfind
import networkx as nx
import matplotlib.pyplot as plt
import time


def loadfile(filename):
    """This function reads a file ad returns a dict of edges with two endpoint nodes and a cost"""
    graph = defaultdict(list)
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # skip an empty line
            if line == '\n':
                continue
            # the text has the following format:
            # [one node] [another node] [edge cost], representing
            # [one airport] [another airport] [price]
            node1 = int(line.split()[0])
            node2 = int(line.split()[1])
            edge_cost = int(line.split()[2])
            # for every node1, place node2 and edge cost in its value
            graph[node1].append((node2, edge_cost))
    return graph


def kruskal(graph:dict):
    """This algorithm implements Kruskal's algorithm searching a minimum spanning tree"""
    start_time = time.perf_counter()    # start timing
    tree = []   # path
    total = 0   # total cost
    verteces = unionfind(len(graph))    # create a unionfind datastructure of the number of nodes in the graph
    # create a heap datastructure with edges (cost, node1, and node2) arching from a source node
    # (the first node in this case)
    unvisited = [(c, n1, n2) for n1 in graph.keys() for n2, c in graph[n1]]
    heapify(unvisited)  # heapify (sort the list into a heap order)
    while len(unvisited) >= 1:  # until checking all the nodes
        cost, node1, node2 = heappop(unvisited)     # pick up the cheapest edge incident to a node already visited
        if not verteces.issame(node1-1, node2-1):   # if the nodes of the edge are in different unions
            verteces.unite(node1-1, node2-1)    # put them into the same union
            total += cost   # increment the total cost
            tree.append((node1, node2, cost))   # insert the edge into the path list
    end_time = time.perf_counter()  # finish timing
    return end_time-start_time, total


def prim(graph:dict):
    """This algorithm implements Prim's algorithm searching a minimum spanning tree"""
    start_time = time.perf_counter()
    unvisited = []      # list of unvisited nodes
    visited = set()     # set of visited nodes
    start = list(graph.keys())[0]   # source node
    visited.add(start)  # add the source node into the visited set
    tree = []   # path
    total = 0   # total cost
    # get edges (the other node and edge cost) incident to the source node and push them into a heap
    for n2, c in graph[start]:
        heappush(unvisited, (c, start, n2))
    while len(visited) < len(graph):    # until the number of nodes visited reaches the toal number of nodes
        cost, node1, node2 = heappop(unvisited)     # pick up the cheapest edge incident to a visited node
        tree.append((node1, node2, cost))   # append the edge into the path
        total += cost   # increment the total cost
        # add node1 and node2 to the set | To affirm that both the nodes are marked by adding both indicriminately
        visited.add(node1)
        visited.add(node2)
        # update the heap | add edges going out from node2.
        # in the first loop, node1=source vertex is already visited and node2 is added to the visited
        # so, add the edges from node2 into a list of candidate edges for the next loop
        for n3, c in graph[node2]:
            heappush(unvisited, (c, node2, n3))
        # check through each unvisited edge and delete those whose two nodes are in the visited
        for edge in unvisited:
            if edge[1] in visited and edge[2] in visited:
                unvisited.remove(edge)
    end_time = time.perf_counter()  # finish timing
    return end_time-start_time, total


def updateEdgelist(tree):
    """
    update the separate txt file storing MST edges for network visualization
    :param tree: dict
    """
    with open('edgelist.txt', 'w') as f:
        for n1, n2, c in tree:
            f.write(str(n1) + ' ' + str(n2) + " {'cost': " + str(c) + "}\n")


def loadnetwork():
    """
    visualizes the network of the minimum spanning tree by reading MSTedgelist.txt
    """
    graph = nx.read_edgelist('edgelist.txt', nodetype=str)

    pos = nx.spring_layout(graph)   # layout of the netwpork

    plt.figure(3, figsize=(10, 6))  # size of the window
    nx.draw_networkx_edges(graph, pos, edge_color='tab:blue', width=0.3, alpha=0.8)     # appearence of edges
    nx.draw_networkx_nodes(graph, pos, node_color='blue', node_size=20)     # appearence of nodes
    plt.axis('off')     # hide axises
    plt.show()


def showResult(x, kruskaltime, primtime):
    """This function shows runtimes of Kruskas and Prim's algorithm"""
    fig = plt.figure(figsize=(10, 6))   # window size
    # x-axis = size of nodes | y-axis = each runtime | and decorate the graph
    plt.plot(x, kruskaltime, color="blue", label="Kruskal")
    plt.plot(x, primtime, color="green", label="Prim")
    # labels of the axises
    plt.xlabel("Node Size")
    plt.ylabel("Run Time")
    # position of the legend
    plt.legend(loc='upper left')
    plt.title("MST Runtime: Kruskal's algorithm vs Prim's algorithm")
    # show grid
    plt.grid(which="major")
    plt.show()



def main():
    # prepare five distinct graphs and compare the running time
    # output: runtime, total distance of MST
    files = [1000, 5000, 10000, 30000, 50000, 100000, 200000]
    kruskal_times = []
    prim_times = []
    # for each node size, append the runtimes of Kruskal's and Prim's algorithm
    for i in files:
        graph = loadfile(f'MST_Graph{i}.txt')
        ktime, _ = kruskal(graph)
        kruskal_times.append(ktime)
        ptime, _ = prim(graph)
        prim_times.append(ptime)

    """Observation"""
    # runtime of kruskal's algorithm is O(n)
    # For each of the n loops, it seems to do constant works (heappop + unionfind)
    # runtime of prim's algorithm is O(n + log m). For each of the n loops, it seems to do log m works (heappush)
    print(kruskal_times)
    print(prim_times)
    # show graph
    showResult(files, kruskal_times, prim_times)


if __name__ == '__main__':
    main()