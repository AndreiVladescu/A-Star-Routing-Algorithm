from network_devices import *

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

# Generic Communication Cables
GEN_COM_Fiber = NetworkEdge(type='Fiber')
GEN_COM_Serial = NetworkEdge(type='Serial')
GEN_COM_Ethernet = NetworkEdge(type='Ethernet')
GEN_COM_Satellite = NetworkEdge(type='Satellite')
GEN_COM_WiFi = NetworkEdge(type='WiFi')
GEN_COM_GSM = NetworkEdge(type='GSM')


def main():

    protocol = Protocol('FTP')
    message = Message(protocol=protocol, data='USER')
    # If detect data == USER from FTP protocol, then drop it
    rule = [protocol, 'USER', True]
    r_c_firewall = Firewall()
    r_c_firewall.add_rule(rule)
    r_c_firewall.is_active = True

    R_C.firewall = r_c_firewall

    network = Network(start=PC_A, goal=PC_B, message=message)

    network.add_nodes([PC_A, PC_B, PC_C, PC_D, R_A, R_B, R_C, R_D])
    '''NETWORK_GRAPH = {R_A: [[R_B, COM_1], [R_C, COM_4]],
                             R_B: [[R_D, COM_3], [R_A, COM_1]],
                             R_C: [[R_D, COM_5], [R_A, COM_4]],
                             R_D: [[PC_B, COM_6], [PC_C, COM_7], [PC_D, COM_8]],
                             PC_A: [[R_A, COM_2]],
                             PC_B: [],
                             PC_C: [],
                             PC_D: []
                             }'''

    network.add_paths([[PC_A, R_A, GEN_COM_Fiber],
                       [R_A, R_B, GEN_COM_Fiber],
                       [R_A, R_C, GEN_COM_Serial],
                       [R_B, R_D, GEN_COM_Fiber],
                       [R_C, R_D, GEN_COM_Serial],
                       [R_D, PC_B, GEN_COM_Ethernet],
                       [R_D, PC_C, GEN_COM_Ethernet],
                       [R_D, PC_D, GEN_COM_Ethernet],
                       #[R_A, R_D, GEN_COM_Satellite]
                       ])

    network.setup()
    # network.NETWORK_GRAPH = NETWORK_GRAPH
    network.run()


if __name__ == "__main__":
    main()
