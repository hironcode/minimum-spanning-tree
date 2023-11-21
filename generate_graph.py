import random
from collections import defaultdict
import tqdm


def creategraph(filename='MST_Graph200.txt', n_nodes=200):
    graph = defaultdict(list)
    unused = set(range(1, n_nodes+1))  # unused verteces
    cycle = set()
    prices = list(range(100, 3001 if n_nodes < 3000 else n_nodes*3))  # distinct edge costs

    # start with a random node
    node1 = random.choice(list(unused))
    unused.remove(node1)

    # connect the starting node to new nodes iteratively
    for i in tqdm.tqdm(range(n_nodes - 1)):
        if n_nodes <= 100:
            num_of_edges = random.randint(1, int(len(list(unused)) / (10^(len(str(len(list(unused))))-1)))+1)
        else:
            num_of_edges = random.randint(1, 5)
        n = random.randint(0, 2)
        for j in range(n):
            if len(cycle) < n:
                continue
            node2 = random.choice(list(cycle))
            price = random.choice(prices)
            prices.remove(price)
            graph[node1].append((node2, price))
            graph[node2].append((node1, price))
        for j in range(num_of_edges):
            if len(list(unused)) == 0:
                continue
            node2 = random.choice(list(unused))
            price = random.choice(prices)
            prices.remove(price)
            # for each of node1 and node2 keys, add each pair vertex and edge cost
            graph[node1].append((node2, price))
            graph[node2].append((node1, price))
            unused.remove(node2)
            if random.choice([True, False]):
                cycle.add(node2)
        node1 = node2  # set the last node as the new source node

    # sort based on keys
    demograph = sorted(graph.items())
    graph = {k: v for k, v in demograph}

    # transcript data to txt file in the adjacency representation
    with open(filename, 'w') as f:
        for n1 in graph.keys():
            for n2, p in graph[n1]:
                text = f'{n1} {n2} {p}\n'
                f.write(text)




if __name__ == '__main__':
    n = 40000
    creategraph(f'MST_Graph{n}.txt', n_nodes=n)