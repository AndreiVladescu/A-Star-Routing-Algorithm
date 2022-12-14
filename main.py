from network_devices import *
import matplotlib.pyplot as plt
import networkx as nx

GRAPH = {'A': [['B', 1], ['C', 1], ['D', 2]],
         'B': [['C', 2], ['E', 1]],
         'C': [['F', 1]],
         'D': [['C', 2], ['F', 1]],
         'E': [['F', 1]],
         'F': [['G', 1]],
         'G': []
         }

INF = 10000
VISITED = []

G = {'A': 0, 'B': INF, 'C': INF, 'D': INF, 'E': INF, 'F': INF, 'G': INF}
parent = {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': ''}
bandwidth_h = {'A': 1, 'B': 1, 'C': 2, 'D': 2, 'E': 2, 'F': 3, 'G': 0}
load_h = {'A': 0, 'B': 0, 'C': 1, 'D': 4, 'E': 3, 'F': 0, 'G': 2}
delay_h = {'A': 2, 'B': 5, 'C': 2, 'D': 5, 'E': 2, 'F': 1, 'G': 0}


def update_g(node, next_node, dist):
    if G[node] + dist < G[next_node]:
        G[next_node] = G[node] + dist
        parent[next_node] = node


def g(n):
    return G[n]


def h(n):
    return bandwidth_h[n] + delay_h[n] + load_h[n]


def f(n):
    return h(n) + g(n)


def expand(n):
    for next in GRAPH[n]:
        update_g(n, next[0], next[1])
    return [next[0] for next in GRAPH[n]]


iter = 0


def a_star(node, scop):
    global iter
    iter += 1
    global VISITED
    VISITED.append(node)
    if node == scop:
        return True

    M = expand(node)
    M.sort(key=f)  # incercati key=h si key=g. Explicati diferentele.

    for m in M:
        if m not in VISITED:
            if a_star(m, scop):
                return True
    return False


start = 'A'
goal = 'G'
a_star(start, goal)

path = []
child = goal
while child != start:
    path.append(child)
    child = parent[child]

path.append(start)
path.reverse()
print("Calea este {} si a fost gasita in {} iteratii.".format(path, iter))
