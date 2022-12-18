import networkx as nx
import PIL
import matplotlib.pyplot as plt

counter_pc = 1
counter_router = 1


class Protocol:
    def __init__(self, name):
        self.name = name


class Message:
    def __init__(self, protocol, data):
        self.protocol = protocol
        self.data = data


class Firewall:
    firewall_rules = {}

    def __int__(self, rules):
        self.firewall_rules = rules
        if len(rules) > 0:
            self.is_active = True
        else:
            self.is_active = False

    def add_rule(self, rule):
        self.firewall_rules[rule[0]] = [rule[1], rule[2]]

    def can_block(self, protocol):
        return self.firewall_rules[protocol.get_name()]


class NetworkDevice:
    is_routable = False
    bandwidth = 1
    latency = 1
    load = 1
    firewall = None

    def __init__(self, type, name=''):
        global counter_router
        global counter_pc
        if type == 'router':
            self.type = 'router'
            self.image = 'imgs/router.jpg'
            self.is_routable = True
            if name == '':
                self.name = 'R' + str(counter_router)
                counter_router += 1
            else:
                self.name = name
        else:
            self.type = 'pc'
            self.image = 'imgs/pc.jpg'
            if name == '':
                self.name = 'PC' + str(counter_pc)
                counter_pc += 1
            else:
                self.name = name

    def get_weight(self):
        return self.bandwidth + self.latency + self.load

    def __int__(self):
        return self.get_weight()

    def __str__(self):
        return self.name

    def _cmp(self, other):
        return int(self) - int(other)

    def is_blocked(self, message):
        if self.firewall is None:
            print('{} let {} message \'{}\' pass through'.format(self.name, message.protocol.name, message.data))
            return False
        '''
        for rule in self.firewall.firewall_rules:
            if rule[0] == message.protocol and rule[1] == message.data and rule[2] == True:
                return True'''
        for key in self.firewall.firewall_rules:
            if message.protocol == key and message.data == self.firewall.firewall_rules[key][0] and self.firewall.firewall_rules[key][1] == True:
                print('{} blocked {} message \'{}\''.format(self.name, message.protocol.name, message.data))
                return True
        print('{} let {} message \'{}\' pass through'.format(self.name, message.protocol.name, message.data))
        return False


class NetworkEdge:
    weight = 0

    def __init__(self, type, override=0):
        self.type = type

        if override == 0:
            if type == 'WiFi':
                self.weight = 10
            elif type == 'GSM':
                self.weight = 25
            elif type == 'Fiber':
                self.weight = 2
            elif type == 'Ethernet':
                self.weight = 5
            elif type == 'Serial':
                self.weight = 1
            elif type == 'Satellite':
                self.weight = 40
        else:
            self.weight = override


class Network:
    message = None
    paths = []
    node_list = []
    # Image URLs for graph nodes
    icons = {
        "router": "imgs/router.jpg",
        "pc": "imgs/pc.jpg",
    }

    NETWORK_GRAPH = dict()

    INF = 10000
    VISITED = []

    hop_count = 0

    def __init__(self, start, goal, message):
        self.big_G = {}
        self.parent = {}
        self.Graph = nx.Graph()
        self.images = {k: PIL.Image.open(fname) for k, fname in self.icons.items()}
        self.start = start
        self.goal = goal
        self.message = message

    def add_node(self, network_node):
        self.node_list.append(network_node)

    def add_nodes(self, network_nodes):
        for node in network_nodes:
            self.add_node(network_node=node)

    def add_path(self, node1, node2, path):
        self.paths.append([node1, node2, path])

    def add_paths(self, paths_list):
        for path in paths_list:
            self.paths.append(path)
            self.paths.append([path[1], path[0], path[2]])

    def setup(self):
        for node in self.node_list:
            self.big_G[node] = 0 if node == self.start else self.INF
            self.parent[node] = None

        for node in self.node_list:
            self.Graph.add_node(node, image=self.images["router"] if node.type == 'router' else self.images['pc'])
        # (PC_A.name, R_A.name, weight=COM_2.weight)
        for path in self.paths:
            self.Graph.add_edge(path[0], path[1], weight=path[2].weight)
            self.Graph.add_edge(path[1], path[0], weight=path[2].weight)
            self.NETWORK_GRAPH[path[0]] = []
            self.NETWORK_GRAPH[path[1]] = []

        for path in self.paths:
            self.NETWORK_GRAPH[path[0]].append([path[1], path[2]])
            self.NETWORK_GRAPH[path[1]].append([path[0], path[2]])

    def update_g(self, node, next_node, path):
        if self.big_G[node] + path.weight < self.big_G[next_node]:
            self.big_G[next_node] = self.big_G[node] + path.weight
            self.parent[next_node] = node

    def g(self, n):
        return self.big_G[n]

    def h(self, n):
        return n.get_weight()

    def f(self, n):
        return self.h(n) + self.g(n)

    def expand(self, n, target):
        for next in self.NETWORK_GRAPH[n]:
            self.update_g(n, next[0], next[1])
        # return [next[0] for next in NETWORK_GRAPH[n]]
        reachable_device_list = []
        for next in self.NETWORK_GRAPH[n]:
            if (next[0].is_routable or next[0] == target) and not next[0].is_blocked(self.message):
                reachable_device_list.append(next[0])
        return reachable_device_list

    def a_star(self, node, target):
        self.hop_count += 1
        # 32 Hops Max
        if self.hop_count > 32:
            return False

        self.VISITED.append(node)
        if node == target:
            return True

        M = self.expand(node, target)
        M.sort(key=self.f)

        for m in M:
            if m not in self.VISITED:
                if self.a_star(m, target):
                    return True
        return False

    def getKeyPaths(self, obj):
        return obj[0].name

    def run(self):
        self.a_star(self.start, self.goal)

        path = []
        child = self.goal
        while child != self.start:
            path.append(child.name)
            child = self.parent[child]

        path.append(self.start.name)
        path.reverse()
        print("Message took the route {} in {} hops.".format(path, self.hop_count))
        print(
            "Station {} received {} message '{}' from station {}".format(self.goal.name, self.message.protocol.name,
                                                                         self.message.data, self.start.name))
        colors = []
        for i in range(len(self.paths)):
            colors.append("black")
        ## Experimental
        '''
        self.paths.sort(key=self.getKeyPaths)
        for i in range(len(path) - 1):
            for j, path_i in enumerate(self.paths):
                if path_i[0].name == path[i] and path_i[1].name == path[i + 1]:
                    colors[j] = "red"
        '''
        # colors[1] = "red"
        pos = nx.spring_layout(self.Graph, seed=1734289230)
        fig, ax = plt.subplots()
        options = {
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "black",
            "edge_color": colors,
            "linewidths": 5,
            "width": 5,
        }
        nx.draw_networkx_edges(
            self.Graph,
            pos=pos,
            ax=ax,
            min_source_margin=15,
            min_target_margin=15,
        )

        nx.draw_networkx(self.Graph, pos, **options)

        tr_figure = ax.transData.transform
        tr_axes = fig.transFigure.inverted().transform

        icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.02
        icon_center = icon_size / 2.0

        for n in self.Graph.nodes:
            xf, yf = tr_figure(pos[n])
            xa, ya = tr_axes((xf, yf))
            a = plt.axes([xa + icon_center / 1.2, ya - icon_center, icon_size, icon_size])
            a.imshow(self.Graph.nodes[n]['image'])
            a.axis("off")
        plt.show()
