from network_devices import *

R_A = NetworkDevice(type='wireless-router', name='R_A')
R_B = NetworkDevice(type='router', name='R_B')
R_C = NetworkDevice(type='wireless-router', name='R_C')
R_D = NetworkDevice(type='router', name='R_D')
R_E = NetworkDevice(type='wireless-router', name='R_E')
R_F = NetworkDevice(type='space-router', name='R_F')
PC_A = NetworkDevice(type='pc', name='PC_A')
PC_B = NetworkDevice(type='pc', name='PC_B')
PC_C = NetworkDevice(type='pc', name='PC_C')
PC_D = NetworkDevice(type='pc', name='PC_D')
PC_E = NetworkDevice(type='pc', name='PC_E')
PC_F = NetworkDevice(type='pc', name='PC_F')
Laptop_A = NetworkDevice(type='laptop', name='Laptop_A')
Tablet_A = NetworkDevice(type='tablet', name='Tablet_A')
Phone_A = NetworkDevice(type='phone', name='Phone_A')
Phone_B = NetworkDevice(type='phone', name='Phone_B')
Phone_C = NetworkDevice(type='phone', name='Phone_C')

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

    # R_C.firewall = r_c_firewall

    network = Network(start=PC_E, goal=PC_B, message=message)
    network.hop_limit = 32
    network.add_nodes(
        [PC_A, PC_B, PC_C, PC_D, PC_E, PC_F, Laptop_A, Phone_A, Phone_B, Phone_C, Tablet_A, R_A, R_B, R_C, R_D, R_E,
         R_F])

    network.add_paths([[PC_A, R_A, GEN_COM_Fiber],
                       [R_A, R_B, GEN_COM_Fiber],
                       [R_A, R_C, GEN_COM_Serial],
                       [R_B, R_D, GEN_COM_Fiber],
                       [R_C, R_D, GEN_COM_Serial],
                       [R_D, PC_B, GEN_COM_Ethernet],
                       [R_D, PC_C, GEN_COM_Ethernet],
                       [R_D, PC_D, GEN_COM_Ethernet],
                       [R_E, Laptop_A, GEN_COM_WiFi],
                       [R_E, Phone_A, GEN_COM_WiFi],
                       [R_E, R_D, GEN_COM_Fiber],
                       [R_E, R_B, GEN_COM_Serial],
                       [R_C, PC_E, GEN_COM_Ethernet],
                       [R_C, PC_F, GEN_COM_Ethernet],
                       [R_A, Tablet_A, GEN_COM_WiFi],
                       [R_F, Phone_B, GEN_COM_Satellite],
                       [R_F, Phone_C, GEN_COM_Satellite],
                       [R_F, R_D, GEN_COM_Satellite],
                       ])

    network.setup()
    # network.NETWORK_GRAPH = NETWORK_GRAPH
    network.run()


if __name__ == "__main__":
    main()
