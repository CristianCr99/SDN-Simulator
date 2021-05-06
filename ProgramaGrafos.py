from __future__ import print_function
from builtins import range
import networkx as nx
from scapy.layers.inet import *


class FlowEntry:
    def __init__(self, mac_src, mac_dst, ip_src, ip_dst, transport_protocol, port_src, port_dst, action):
        # self.id = id
        self.mac_src = mac_src
        self.mac_dst = mac_dst
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.port_src = port_src
        self.port_dst = port_dst
        self.transport_protocol = transport_protocol
        self.counter_packet_number = 0
        self.counter_packet_byte = 0
        self.action = action

    def get_ip_src(self):
        return (self.ip_src)

    def get_ip_dst(self):
        return (self.ip_dst)

    def get_mac_src(self):
        return (self.mac_src)

    def get_mac_dst(self):
        return (self.mac_dst)

    def get_port_src(self):
        return (self.port_src)

    def get_port_dst(self):
        return (self.port_dst)

    def get_transport_protocol(self):
        return (self.transport_protocol)

    def get_action(self):
        return (self.action)

    def get_counter_packet_number(self):
        return self.counter_packet_number

    def get_counter_packet_byte(self):
        return self.counter_packet_byte

    def set_counter_packet_number(self, counter_packet_number):
        self.counter_packet_number = counter_packet_number

    def set_counter_packet_byte(self, counter_packet_byte):
        self.counter_packet_byte = counter_packet_byte


class NetworkTopology(object):
    def __init__(self):
        self.G = nx.Graph()
        # self.list_Packets_to_send = {}
        # self.miniNam = None
        # self.MNAM = mn.MiniNAM()

    def get_graph(self):
        return (self.G)

    def set_graph(self, G):
        self.G = G

    # def set_minin(self, minin):
    #     self.miniNam = minin

    def add_switch(self, num_switch, flow_table=[]):
        self.G.add_node(num_switch, type='switch', name='s' + str(num_switch), flow_table=flow_table)
        # self.MNAM.addNode(num_switch,'switch')

    def add_host(self, num_host):
        self.G.add_node(num_host, type='host', name='h' + str(num_host))
        # self.MNAM.addNode(num_host, 'host')

    def add_controller(self, num_controller):
        self.G.add_node(num_controller, type='controller', name='c' + str(num_controller))
        # self.MNAM.addNode(num_controller, 'controller')

    def add_link(self, node_a, node_b, weight_link):
        self.G.add_edge(node_a, node_b, weight=weight_link)
        # self.MNAM.drawLink(self.G.nodes[node_a]['name'], self.G.nodes[node_b]['name'])

    def add_flow_entry_to_node(self, node, flowentry):
        self.G.nodes[node]['flow_table'].append(flowentry)

    # def get_list_packets_to_send(self):
    #     return self.list_Packets_to_send

    def set_list_packets_to_send(self, list):
        self.list_Packets_to_send = list

    def show_flow_table(self, node):
        print("Tabla de flujo del switch:", node)
        j = 0
        for i in (self.G.nodes[node]['flow_table']):
            print('------- Entrada ' + str(j) + ' -------')
            print("     MAC src: " + i.get_mac_src())
            print("     MAC dst: " + i.get_mac_dst())
            print("     IP src: " + i.get_ip_src())
            print("     IP src: " + i.get_ip_dst())
            print("     Transport protocol: " + i.get_transport_protocol())
            print("     Port src: " + str(i.get_port_src()))
            print("     Port dst: " + str(i.get_port_dst()))
            print("     Packet number counter: " + str(i.get_counter_packet_number()) + ' packets')
            print("     Packet bytes counter: " + str(i.get_counter_packet_byte()) + ' bytes')
            print("-----------------------------------")
            j += 1

    def match_and_action(self, switch, packet):

        for i in (self.G.nodes[switch]['flow_table']):
            # print('src MAC:', packet[Ether].src, 'dst MAC', packet[Ether].dst, 'src:', packet[IP].src, 'dst:',
            #       packet[IP].dst)
            if 'TCP' in packet:
                protocol = 'TCP'
            else:
                protocol = 'UDP'
            print(i.get_mac_src() == packet[Ether].src, i.get_mac_src() == '*', i.get_mac_dst() == packet[
                Ether].src,i.get_mac_dst() == '*', i.get_ip_src() == packet[IP].src, i.get_ip_dst() == packet[
                IP].dst, i.get_transport_protocol() == protocol, i.get_port_src() == packet[protocol].sport,  i.get_port_dst() == packet[protocol].dport)

            if i.get_mac_src() == packet[Ether].src or i.get_mac_src() == '*' and i.get_mac_dst() == packet[
                Ether].src or i.get_mac_dst() == '*' \
                    and i.get_ip_src() == packet[IP].src and i.get_ip_dst() == packet[
                IP].dst and i.get_transport_protocol() == protocol \
                    and i.get_port_src() == packet[protocol].sport and i.get_port_dst() == packet[protocol].dport:

                i.set_counter_packet_number(i.get_counter_packet_number() + 1)
                i.set_counter_packet_byte(i.get_counter_packet_byte() + len(packet))

                return i.get_action()
        return 0

    def find_hosts_by_ip_packet(self, packet):
        src_host = None
        dst_host = None
        for i in list(self.G.nodes):
            if i[0] == 'h':
                if self.G.nodes[i]['ip'] == packet[IP].src:
                    src_host = i
                if self.G.nodes[i]['ip'] == packet[IP].dst:
                    dst_host = i
        return src_host, dst_host

    def controller_action(self, miniNAM, packet, src_host, dst_host, switch, proactive):
        # verInformacionConcretaNodo(self.G)
        # TODO Preguntar por la otra funcion que te debuelve solo el camino deseado de un origen a un destino

        #all_path = dict(nx.all_pairs_dijkstra_path(self.G, cutoff=None, weight='weight'))

        path = nx.dijkstra_path(self.G, src_host, dst_host, 'weight')

        # Enviamos a cada Switch un flowMod (Enviar graficamente)

        if 'TCP' in packet:
            protocol = 'TCP'
        else:
            protocol = 'UDP'

        for i in range(1, len(path) - 1):

            if proactive == True and path[i]:
                # def __init__(self, mac_src, mac_dst, ip_src, ip_dst, transport_protocol,port_src, port_dst, action):
                miniNAM.displayPacket('c0', path[i], None, True, 'Flow_Mod', 'c0' + '->' + path[i])
                self.add_flow_entry_to_node(path[i], FlowEntry('*', '*', packet[IP].src,
                                                               packet[IP].dst, protocol ,packet[protocol].sport,
                                                               packet[protocol].dport, path[i + 1]))
                print('flowMod a ', path[i])


            if path[i] == switch:
                action = path[i + 1]


        # Enviamos paquet_out a switch (Enviar graficamente)
        print('paquetOut a ', switch)
        miniNAM.displayPacket('c0', switch, None, True, 'Packet_Out', 'c0' + '->' + switch)
        # self.miniNam.displayPacket('c0', 's' + str(switch), '')
        return action

    def communication_hots(self, miniNAM, h_src, packet):

        src_host, dst_host = self.find_hosts_by_ip_packet(packet)
        print('Hosts:',src_host, dst_host)

        if src_host == h_src and dst_host is not None:

            if self.G.degree(src_host) == 1:  # solo puede un host estar conectado a un Switch

                listEnlaces = list(self.G.edges(src_host))
                Switch = tuple(listEnlaces[0])[1]  # Cogemos el Switch al cual esta conectado [1]
                print(src_host, Switch)
                miniNAM.displayPacket(src_host, Switch, packet, False, None, src_host + '->' + dst_host)
                print('Enviamos paquete a', Switch)

                has_arrived = False

                while has_arrived == False:

                    action = self.match_and_action(Switch, packet)

                    if action == 0:
                        print('No Matchin')
                        miniNAM.displayPacket(Switch, 'c0', packet, True, 'Packet_In', Switch + '->' + 'c0')
                        #def controller_action(self, miniNAM, packet, src_host, dst_host, switch, proactive):
                        action = self.controller_action(miniNAM, packet, src_host, dst_host, Switch, True)

                    print('enviamos paquete a', action)

                    # Reenviamos el paquete a al siguiente Switch indicado por action (Enviar graficamente)

                    if action == dst_host:
                        # Se envia al host destino y ha llegado al destino (Enviar graficamente)
                        print('Llega paquete al destino', action)
                        miniNAM.displayPacket(Switch, dst_host, packet, False, None, src_host + '->' + dst_host)
                        has_arrived = True
                    else:
                        print('Llega paquete a', action)
                        miniNAM.displayPacket(Switch, action, packet, False, None, src_host + '->' + dst_host)

                    Switch = action

                # Enviamos paquet_in al controlador
    # def create_topology(self, num_host, num_switch):
    #
    #     nodo = []
    #     links = []
    #
    #     # for i in list(self.G.nodes):
    #     #
    #
    #
    #     for i in range(1, num_host + 1):
    #         self.add_host(i)
    #         nodo.append((i, 'host'))
    #
    #     for i in range(num_host + 1, num_host + 1 + num_switch):
    #         self.add_switch(i, flow_table=[])
    #         nodo.append((i, 'switch'))
    #
    #     self.add_controller(0)
    #     nodo.append((0, 'controller'))
    #
    #     self.add_link(1, 3, 1)
    #     links.append((1, 3, self.G.nodes[1]['type'], self.G.nodes[3]['type'])) #############################################
    #     self.add_link(2, 5, 1)
    #     links.append((2, 5, self.G.nodes[2]['type'], self.G.nodes[5]['type']))
    #     self.add_link(3, 4, 1)
    #     links.append((3, 4, self.G.nodes[3]['type'], self.G.nodes[4]['type']))
    #     self.add_link(3, 5, 5)
    #     links.append((3, 5, self.G.nodes[3]['type'], self.G.nodes[5]['type']))
    #     self.add_link(4, 5, 1)
    #     links.append((4, 5, self.G.nodes[4]['type'], self.G.nodes[5]['type']))
    #     self.add_link(3, 0, sys.maxsize)
    #     links.append((3, 0, self.G.nodes[3]['type'], self.G.nodes[0]['type']))
    #     self.add_link(4, 0, sys.maxsize)
    #     links.append((4, 0, self.G.nodes[4]['type'], self.G.nodes[0]['type']))
    #     self.add_link(5, 0, sys.maxsize)
    #     links.append((5, 0, self.G.nodes[5]['type'], self.G.nodes[0]['type']))
    #     # G.set_minin(mnam.MiniNAM(list_links=links, list_nodes=nodo))
    #     print(links,nodo)
    #     #print(json.dumps(json_graph.node_link_data(self.G), indent=4))
    #     return links, nodo

    # def save_topology(self):

# def SDN():
#     # Creación de una instancia de la clase NetworkTopology
#     graph = NetworkTopology()
#     num_host = 2
#     num_switch = 3
#     create_topology(graph, num_host, num_switch)
#
#     graph.communication_hots(1, 1, 2)
#     graph.communication_hots(2, 2, 1)
#     graph.communication_hots(1, 1, 2)
#     graph.communication_hots(2, 2, 1)
#     #graph.communication_hots(1, 2, 1)
#
#     # Añadimos la entrada de flujo a la lista de entradas de flujos del nodo 1 de la topologia de red (instancia de la clase FlowEntry (src=1,dst=4,id=0))
#     # graph.add_flow_entry_to_node(1, FlowEntry(1, 4, 0, ))
#     # Añadimos la entrada de flujo a la lista de entradas de flujos del nodo 1 de la topologia de red (otra instancia de la clase FlowEntry (src=1,dst=8,id=1))
#     # graph.add_flow_entry_to_node(1, FlowEntry(1, 8, 1))
#     # Comprobamos que se añade correctamente
#     # graph.show_flow_table(1)
#     # verInformacionConcretaNodo(graph)
#     # verInformacionConcretaEnlace(graph)
#     # graph.add_flow_entry_to_node(1, FlowEntry(1, 8, 1, 1))
#     # graph.show_flow_table(1)
#     '''
#     for i in range(1, 3):
#         graph.add_host(i)
#     for i in range(3, 6):
#         graph.add_switch(i, flow_table=[])
#
#     graph.add_controller(6)
#     '''
#
#     # self.MNAM.createNodes()
#     # self.MNAM.createNodes()
#     # self.MNAM.drawLink('h1', 'h2')


# SDN()
