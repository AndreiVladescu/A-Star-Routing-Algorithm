class NetworkDevice:
    counter_router = 1
    counter_pc = 1

    is_routable = False

    bandwidth = 1
    latency = 1
    load = 1

    def __init__(self, type, name =''):
        if type == 'router':
            self.type = 'router'
            self.image = 'imgs/router.jpg'
            is_routable = True
            if name == '':
                self.name = 'R' + str(self.counter_router)
                self.counter_router += 1
            else:
                self.name = name
        else:
            self.type = 'pc'
            self.image = 'imgs/pc.jpg'
            if name == '':
                self.name = 'PC' + str(self.counter_pc)
                self.counter_pc += 1
            else:
                self.name = name
    def can_route(self):
        return self.is_routable

    def get_weight(self):
        return self.bandwidth + self.latency + self.load

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

class Firewall:
    def __int__(self, rules):
        self.firewall_rules =  rules
        if len(rules) > 0:
            self.is_active = True
        else:
            self.is_active = False
    def get_rules(self):
        return self.firewall_rules
    def can_block(self, protocol):
        return self.firewall_rules[protocol.get_name()]

class Protocol:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class NetworkEdge:
    weight = 0
    def __init__(self, type, override = 0):
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
    def get_weight(self):
        return self.weight
    def get_type(self):
        return self.type

class Message:
    def __init__(self, protocol, data):
        self.protocol = protocol
        self.data = data
    def get_protocol(self):
        return self.protocol
    def get_data(self):
        return self.data
