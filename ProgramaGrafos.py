from __future__ import print_function

import uuid
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
        self.proactive = True
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
                Ether].src, i.get_mac_dst() == '*', i.get_ip_src() == packet[IP].src, i.get_ip_dst() == packet[
                      IP].dst, i.get_transport_protocol() == protocol, i.get_port_src() == packet[protocol].sport,
                  i.get_port_dst() == packet[protocol].dport)

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
                    print('host origen:', packet[IP].src)
                if self.G.nodes[i]['ip'] == packet[IP].dst:
                    dst_host = i
                    print('host destino:', packet[IP].dst)
        return src_host, dst_host

    def controller_action(self, miniNAM, packet, src_host, dst_host, switch, proactive):
        # verInformacionConcretaNodo(self.G)

        # all_path = dict(nx.all_pairs_dijkstra_path(self.G, cutoff=None, weight='weight'))

        path = nx.dijkstra_path(self.G, src_host, dst_host, weight='bw')
        print(path)

        # Enviamos a cada Switch un flowMod (Enviar graficamente)

        if 'TCP' in packet:
            protocol = 'TCP'
        else:
            protocol = 'UDP'

        for i in range(1, len(path) - 1):

            if proactive == True and path[i]:
                # def __init__(self, mac_src, mac_dst, ip_src, ip_dst, transport_protocol,port_src, port_dst, action):
                miniNAM.display_multiple_packet('c0', path[i], None, True, 'Flow_Mod', 'c0' + '->' + path[i])
                # miniNAM.join()
                self.add_flow_entry_to_node(path[i], FlowEntry('*', '*', packet[IP].src,
                                                               packet[IP].dst, protocol, packet[protocol].sport,
                                                               packet[protocol].dport, path[i + 1]))
                print('flowMod a ', path[i])

            if path[i] == switch:
                action = path[i + 1]
        # for i in range(1, len(path) - 1):
        # miniNAM.join()

        # Enviamos paquet_out a switch (Enviar graficamente)
        print('paquetOut a ', switch)
        miniNAM.displayPacket('c0', switch, None, True, 'Packet_Out', 'c0' + '->' + switch)
        # self.miniNam.displayPacket('c0', 's' + str(switch), '')
        return action

    def processing_event_packet_generation(self, event, list_packets):
        # print(event['packet_id'])
        src_host, dst_host = self.find_hosts_by_ip_packet(list_packets[event['packet_id']])
        print(src_host,dst_host)
        # print('Hosts:', src_host, dst_host)

        if src_host is not None and dst_host is not None:

            if self.G.degree(src_host) == 1:  # solo puede un host estar conectado a un Switch

                listEnlaces = list(self.G.edges(src_host))
                Switch = tuple(listEnlaces[0])[1]  # Cogemos el Switch al cual esta conectado [1]
                # print(src_host, Switch)

                event = {'type': 'packet_propagation',
                         'src': src_host,
                         'dst': Switch,
                         'time_spawn': event['time_spawn'],
                         'packet_id': event['packet_id']
                         }
            return event
        return 0

    def processing_event_packet_propagation(self, event, list_packets):
        if event['dst'] == 'c0' or event['src'] == 'c0':
            propagation_delay = 0.06
        else:
            propagation_delay = self.G.edges[event['src'], event['dst']]['distance'] / \
                                self.G.edges[event['src'], event['dst']]['propagation_speed'] + len(
                list_packets[event['packet_id']]) / self.G.edges[event['src'], event['dst']]['bw']

        if event['dst'] == 'c0':
            type = 'packet_processing_controller'
        elif event['dst'][0] == 'h' :
            type = 'packet_processing_host'
        else:
            type = 'packet_processing_switch'

        if 'openflow_id' in event:
            event = {'type': type,
                     'src': event['src'],
                     'dst': event['dst'],
                     'time_spawn': event['time_spawn'] + propagation_delay,
                     'packet_id': event['packet_id'],
                     'openflow_id': event['openflow_id']
                     }
            return event
        else:
            event = {'type': type,
                     'src': event['src'],
                     'dst': event['dst'],
                     'time_spawn': event['time_spawn'] + propagation_delay,
                     'packet_id': event['packet_id']
                     }
            return event

    def processing_event_packet_propagation2(self, event, list_packets,list_openflow,miniNAM):
        if event['dst'] == 'c0' or event['src'] == 'c0':
            propagation_delay = 0.06 + 3.5
            is_openflow = True
            type_message = list_openflow[event['openflow_id']]['type']
        else:
            # print('time:',float(miniNAM.appPrefs['flowTime']))
            propagation_delay = (self.G.edges[event['src'], event['dst']]['distance'] / \
                                self.G.edges[event['src'], event['dst']]['propagation_speed'] + len(
                list_packets[event['packet_id']]) / self.G.edges[event['src'], event['dst']]['bw']) + 3.5
            is_openflow = False
            type_message = None
        if event['dst'] == 'c0':
            type = 'packet_processing_controller'
        elif event['dst'][0] == 'h':
            type = 'packet_processing_host'
        else:
            type = 'packet_processing_switch'
        # print(propagation_delay)
        miniNAM.display_multiple_packet(event['src'], event['dst'], list_packets[event['packet_id']], is_openflow, type_message, event['src'] + '->' +  event['dst'], propagation_delay)
        # print('hola')
        if 'openflow_id' in event:
            event = {'type': type,
                     'src': event['src'],
                     'dst': event['dst'],
                     'time_spawn': event['time_spawn'] + propagation_delay,
                     'packet_id': event['packet_id'],
                     'openflow_id': event['openflow_id']
                     }
            return event
        else:
            event = {'type': type,
                     'src': event['src'],
                     'dst': event['dst'],
                     'time_spawn': event['time_spawn'] + propagation_delay,
                     'packet_id': event['packet_id']
                     }
            return event

    def processing_event_packet_match_and_action_switch(self, event, list_packets, list_openflow):
        # print(event)
        if 'openflow_id' in event:
            if list_openflow[event['openflow_id']]['type'] == 'packet_out':
                if 'TCP' in list_packets[event['packet_id']]:
                    protocol = 'TCP'
                else:
                    protocol = 'UDP'
                self.add_flow_entry_to_node(event['dst'], FlowEntry('*', '*', list_packets[event['packet_id']][IP].src,
                                                                    list_packets[event['packet_id']][IP].dst, protocol,
                                                                    list_packets[event['packet_id']][protocol].sport,
                                                                    list_packets[event['packet_id']][protocol].dport,
                                                                    list_openflow[event['openflow_id']]['action']))
                event = {'type': 'packet_propagation',
                         'src': event['dst'],
                         'dst': list_openflow[event['openflow_id']]['action'],
                         'time_spawn': event['time_spawn'] + 0.1 + 0.1, # TODO Preguntar esta parte :(
                         'packet_id': event['packet_id']
                         }
                return event
            elif list_openflow[event['openflow_id']]['type'] == 'flow_mood':
                if 'TCP' in list_packets[event['packet_id']]:
                    protocol = 'TCP'
                else:
                    protocol = 'UDP'
                self.add_flow_entry_to_node(event['dst'], FlowEntry('*', '*', list_packets[event['packet_id']][IP].src,
                                                               list_packets[event['packet_id']][IP].dst, protocol, list_packets[event['packet_id']][protocol].sport,
                                                               list_packets[event['packet_id']][protocol].dport, list_openflow[event['openflow_id']]['action']))
                return 0
        else:
            for i in (self.G.nodes[event['dst']]['flow_table']):
                packet = list_packets[event['packet_id']]
                if 'TCP' in packet:
                    protocol = 'TCP'
                else:
                    protocol = 'UDP'
                print(i.get_mac_src() == packet[Ether].src, i.get_mac_src() == '*', i.get_mac_dst() == packet[
                    Ether].src, i.get_mac_dst() == '*', i.get_ip_src() == packet[IP].src, i.get_ip_dst() == packet[
                          IP].dst, i.get_transport_protocol() == protocol, i.get_port_src() == packet[protocol].sport,
                      i.get_port_dst() == packet[protocol].dport)

                if i.get_mac_src() == packet[Ether].src or i.get_mac_src() == '*' and i.get_mac_dst() == packet[
                    Ether].src or i.get_mac_dst() == '*' \
                        and i.get_ip_src() == packet[IP].src and i.get_ip_dst() == packet[
                    IP].dst and i.get_transport_protocol() == protocol \
                        and i.get_port_src() == packet[protocol].sport and i.get_port_dst() == packet[protocol].dport:
                    i.set_counter_packet_number(i.get_counter_packet_number() + 1)
                    i.set_counter_packet_byte(i.get_counter_packet_byte() + len(packet))

                    event = {'type': 'packet_propagation',
                             'src': event['dst'],
                             'dst': i.get_action(),
                             'time_spawn': event['time_spawn'] + 0.1,
                             'packet_id': event['packet_id']
                             }
                    return event
        id = uuid.uuid4()
        event = {'type': 'packet_propagation',
                 'src': event['dst'],
                 'dst': 'c0',
                 'time_spawn': event['time_spawn'] + 0.1,
                 'packet_id': event['packet_id'],
                 'openflow_id': id
                 }
        list_openflow[id] = {'type': 'packet_in','size': 10}
        return event

    # def processing_event_packet_controller_action(self, miniNAM, packet, src_host, dst_host, switch, proactive):
    def processing_event_packet_controller_action(self, event, list_packets, list_openflow_messages):

        packet = list_packets[event['packet_id']]
        src_host, dst_host = self.find_hosts_by_ip_packet(packet)
        path = nx.dijkstra_path(self.G, src_host, dst_host, weight='bw')
        list_new_events = []

        for i in range(1, len(path) - 1):
            if path[i] == event['src']:
                id = uuid.uuid4()
                list_new_events.append({'type': 'packet_propagation',
                                        'src': event['dst'],
                                        'dst': event['src'],
                                        'time_spawn': event['time_spawn'] + 0.1,
                                        'packet_id': event['packet_id'],
                                        'openflow_id': id
                                        })

                list_openflow_messages[id] = {'type': 'packet_out', 'action': path[i + 1],
                                              'size': 10}  # TODO ver el tamanio real de un mensaje opnflow (p_out) y ponerlo aqui
                # list_openflow_messages.append()
            if self.proactive and path[i] and path[i] != event['src']:
                id = uuid.uuid4()
                list_new_events.append({'type': 'packet_propagation',
                                        'src': event['dst'],
                                        'dst': path[i],
                                        'time_spawn': event['time_spawn'] + 0.1,
                                        'packet_id': event['packet_id'],
                                        'openflow_id': id
                                        })
                list_openflow_messages[id] = {'type': 'flow_mood', 'action': path[i + 1],
                                              'size': 10}  # TODO ver el tamanio real de un mensaje opnflow (f_mood) y ponerlo aqui
        return list_new_events

    def communication_hots(self, miniNAM, h_src, packet):
        # Voy a dividir este metodo en varias partes mediante comentarios para luego pasarlo a diferentes metodos para el
        # simulador de eventos discretos

        #### (1) Estos seria el tratamiento de un paquete generado ####

        # Recibe el evento:
        #    - Type: packet_generation
        #           - Time Spawn: TimeSpawn (del evento que está procesando)
        #           - Origen: None
        #           - Destino: None
        #           - ID_paquete: (El que sea)
        #

        # Cogemos el paquete de la lista de paquetes mediante su id:
        src_host, dst_host = self.find_hosts_by_ip_packet(packet)
        print('Hosts:', src_host, dst_host)

        if src_host == h_src and dst_host is not None:

            if self.G.degree(src_host) == 1:  # solo puede un host estar conectado a un Switch

                listEnlaces = list(self.G.edges(src_host))
                Switch = tuple(listEnlaces[0])[1]  # Cogemos el Switch al cual esta conectado [1]
                print(src_host, Switch)

                # Puede devolver:
                #       o Evento propagacion:
                #           - Type: packet_propagation
                #           - Time Spawn: TimeSpawn recibido (del evento que está procesando)
                #           - Origen: src_host
                #           - Destino: Switch
                #           - ID_paquete: el mismo id que el recibido
                ###############################################################

                #### (2) Estos seria el tratamiento de una propagacion de un paquete por un enlace ####

                # Recive el evento anteriormente mencionado
                miniNAM.displayPacket(src_host, Switch, packet, False, None, src_host + '->' + dst_host)
                print('Enviamos paquete a', Switch)
                # Generaria un evento:
                #       o Evento procesamiento:
                #           - Type: packet_processing
                #           - Time Spawn: TimeSpawn recibido + + TimeSpawn (calculado con el enlace (BW) y el paquete (SIZE))
                #           - Origen: None
                #           - Destino: Switch
                #           - ID_paquete: el mismo id que el id del paquete recibido en el evento

                has_arrived = False

                while has_arrived == False:

                    action = self.match_and_action(Switch, packet)

                    if action == 0:
                        print('No Matchin')
                        miniNAM.displayPacket(Switch, 'c0', packet, True, 'Packet_In', Switch + '->' + 'c0')
                        # def controller_action(self, miniNAM, packet, src_host, dst_host, switch, proactive):
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
