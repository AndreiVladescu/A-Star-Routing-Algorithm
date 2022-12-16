from network_devices import *
import matplotlib.pyplot as plt
import networkx as nx
import PIL

# Image URLs for graph nodes
icons = {
    "router": "imgs/router.jpg",
    "pc": "imgs/pc.jpg",
}

# Load images
images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

R_A = NetworkDevice(type='router', name='R_A')
R_B = NetworkDevice(type='router', name='R_B')
R_C = NetworkDevice(type='router', name='R_C')
R_D = NetworkDevice(type='router', name='R_D')
PC_A = NetworkDevice(type='pc', name='PC_A')
PC_B = NetworkDevice(type='pc', name='PC_B')
PC_C = NetworkDevice(type='pc', name='PC_C')
PC_D = NetworkDevice(type='pc', name='PC_D')

COM_1 = NetworkEdge(type='Fiber')
COM_2 = NetworkEdge(type='Fiber')
COM_3 = NetworkEdge(type='Fiber')
COM_4 = NetworkEdge(type='Serial')
COM_5 = NetworkEdge(type='Serial')
COM_6 = NetworkEdge(type='Ethernet')
COM_7 = NetworkEdge(type='Ethernet')
COM_8 = NetworkEdge(type='Ethernet')

NETWORK_GRAPH = {R_A: [[R_B, COM_1], [R_C, COM_4]],
                 R_B: [[R_D, COM_3]],
                 R_C: [[R_D, COM_5]],
                 R_D: [[PC_B, COM_6], [PC_C, COM_7], [PC_D, COM_8]],
                 PC_A: [[R_A, COM_2]],
                 PC_B: [],
                 PC_C: [],
                 PC_D: []
                 }

INF = 10000
VISITED = []

G = {PC_A: 0, R_A: INF, R_B: INF, R_C: INF, R_D: INF, PC_B: INF, PC_C: INF, PC_D: INF}
parent = {R_A: None, R_B: None, R_C: None, R_D: None, PC_A: None, PC_B: None, PC_C: None, PC_D: None}
h_net = {R_A: R_A.get_weight(), R_B: R_B.get_weight(), R_C: R_C.get_weight(), R_D: R_D.get_weight(),
         PC_A: PC_A.get_weight(),
         PC_B: PC_B.get_weight(),
         PC_C: PC_C.get_weight(),
         PC_D: PC_D.get_weight()}
hops = 0


def update_g(node, next_node, path):
    if G[node] + path.weight < G[next_node]:
        G[next_node] = G[node] + path.weight
        parent[next_node] = node


def g(n):
    return G[n]


def h(n):
    return h_net[n]


def f(n):
    return h(n) + g(n)


def expand(n, target):
    for next in NETWORK_GRAPH[n]:
        update_g(n, next[0], next[1])
    # return [next[0] for next in NETWORK_GRAPH[n]]
    reachable_device_list = []
    for next in NETWORK_GRAPH[n]:
        if next[0].is_routable or next[0] == target:
            reachable_device_list.append(next[0])
    return reachable_device_list


def a_star(node, target):
    global hops
    hops += 1
    # 32 Hops Max
    if hops > 32:
        return False

    global VISITED
    VISITED.append(node)
    if node == target:
        return True

    M = expand(node, target)
    M.sort(key=f)

    for m in M:
        if m not in VISITED:
            if a_star(m, target):
                return True
    return False


def main():
    global parent
    start = PC_A
    goal = PC_C
    a_star(start, goal)

    path = []
    child = goal
    while child != start:
        path.append(child.name)
        child = parent[child]

    path.append(start.name)
    path.reverse()
    print("Calea este {} si a fost gasita in {} iteratii.".format(path, hops))

    Graph = nx.Graph()
    Graph.add_node(R_A.name, image=images["router"])
    Graph.add_node(R_B.name, image=images["router"])
    Graph.add_node(R_C.name, image=images["router"])
    Graph.add_node(R_D.name, image=images["router"])
    Graph.add_node(PC_A.name, image=images["pc"])
    Graph.add_node(PC_B.name, image=images["pc"])
    Graph.add_node(PC_C.name, image=images["pc"])
    Graph.add_node(PC_D.name, image=images["pc"])

    Graph.add_edge(R_A.name, R_B.name, weight=COM_1.weight)
    Graph.add_edge(R_A.name, R_C.name, weight=COM_4.weight)
    Graph.add_edge(R_B.name, R_D.name, weight=COM_3.weight)
    Graph.add_edge(R_C.name, R_D.name, weight=COM_5.weight)
    Graph.add_edge(R_D.name, PC_B.name, weight=COM_6.weight)
    Graph.add_edge(PC_A.name, R_A.name, weight=COM_2.weight)
    Graph.add_edge(R_D.name, PC_C.name, weight=COM_7.weight)
    Graph.add_edge(R_D.name, PC_D.name, weight=COM_8.weight)

    pos = nx.spring_layout(Graph, seed=1734289230)
    fig, ax = plt.subplots()
    options = {
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }
    nx.draw_networkx_edges(
        Graph,
        pos=pos,
        ax=ax,
        min_source_margin=15,
        min_target_margin=15,
    )
    nx.draw_networkx(Graph, pos, **options)
    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform

    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.05
    icon_center = icon_size / 2.0

    for n in Graph.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        a = plt.axes([xa + icon_center / 1.2, ya - icon_center, icon_size, icon_size])
        a.imshow(Graph.nodes[n]["image"])
        a.axis("off")
    plt.show()


if __name__ == "__main__":
    main()
