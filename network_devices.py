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
            self.image = 'doc_jpg/router.jpg'
            is_routable = True
            if name == '':
                self.name = 'R' + str(self.counter_router)
                self.counter_router += 1
            else:
                self.name = name
        else:
            self.type = 'pc'
            self.image = 'doc_jpg/pc.jpg'
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
