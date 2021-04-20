from __future__ import print_function

import json

import networkx as nx
import matplotlib.pyplot as plt
from builtins import range
from datetime import date
import sys
import MiniNAM as mnam
from networkx.readwrite import json_graph


class FlowEntry:
    def __init__(self, id, src, dst, action):
        self.id = id
        self.src = src
        self.dst = dst
        self.action = action
        self.counter = 0

    def get_src(self):
        return (self.src)

    def get_dst(self):
        return (self.dst)

    def get_id(self):
        return (self.id)

    def get_action(self):
        return (self.action)

    def get_counter(self):
        return (self.counter)


class NetworkTopology(object):
    def __init__(self):
        self.G = nx.Graph()
        #self.miniNam = None
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




    def show_flow_table(self, node):
        for i in (self.G.nodes[node]['flow_table']):
            print("Entrada de flujo " + str(i.get_id()))
            print("     Origen: " + str(i.get_src()))
            print("     Destino: " + str(i.get_dst()))
            print("----------------------")

    def match_and_action(self, switch, id, h_src, h_dst):
        for i in (self.G.nodes[switch]['flow_table']):
            if i.get_id() == id and i.get_src() == h_src and i.get_dst() == h_dst:
                return i.get_action()
        return 0

    def controller_action(self, miniNAM, id, h_src, h_dst, switch, proactive):
        # verInformacionConcretaNodo(self.G)
        all_path = dict(nx.all_pairs_dijkstra_path(self.G, cutoff=None, weight='weight'))

        path = nx.dijkstra_path(self.G, h_src, h_dst, 'weight')

        # Enviamos a cada Switch un flowMod (Enviar graficamente)

        for i in range(1, len(path) - 1):

            if proactive == True and path[i] != switch:
                self.add_flow_entry_to_node(path[i], FlowEntry(id, h_src, h_dst, path[i + 1]))
                print('flowMod a ', path[i])
                miniNAM.displayPacket('c0', path[i], '')

            if path[i] == switch:
                action = path[i + 1]
                # Enviamos paquet_out a switch (Enviar graficamente)
                self.add_flow_entry_to_node(path[i], FlowEntry(id, h_src, h_dst, path[i + 1]))
                print('flowMod a ', switch)
                miniNAM.displayPacket('c0', switch, 'sadasd')
                print('paquetOut a ', switch)
                miniNAM.displayPacket('c0',switch, 'asdasdsa')


        # Enviamos paquet_out a switch (Enviar graficamente)
        print('paquetOut a ', switch)
        #self.miniNam.displayPacket('c0', 's' + str(switch), '')
        return action

    def communication_hots(self,miniNAM, id, h_src, h_dst):

        if self.G.degree(h_src) == 1:  # solo puede un host estar conectado a un Switch

            listEnlaces = list(self.G.edges(h_src))
            Switch = tuple(listEnlaces[0])[1] # Cogemos el Switch al cual esta conectado [1]
            print(h_src, Switch)
            miniNAM.displayPacket(h_src, Switch, 'hola')
            print('Enviamos paquete a', Switch)

            has_arrived = False

            while has_arrived == False:

                action = self.match_and_action(Switch, id, h_src, h_dst)

                if action == 0:
                    print('No Matchin')
                    miniNAM.displayPacket(Switch, 'c0', 'hola')
                    action = self.controller_action(miniNAM,id, h_src, h_dst, Switch, True)

                print('enviamos paquete a', action)

                # Reenviamos el paquete a al siguiente Switch indicado por action (Enviar graficamente)

                if action == h_dst:
                    # Se envia al host destino y ha llegado al destino (Enviar graficamente)
                    print('Llega paquete al destino', action)
                    miniNAM.displayPacket(Switch, h_dst, 'hola')
                    has_arrived = True
                else:
                    print('Llega paquete a', action)
                    miniNAM.displayPacket(Switch, action, 'hola')

                Switch = action

                # Enviamos paquet_in al controlador
    def create_topology(self, num_host, num_switch):

        nodo = []
        links = []

        # for i in list(self.G.nodes):
        #


        for i in range(1, num_host + 1):
            self.add_host(i)
            nodo.append((i, 'host'))

        for i in range(num_host + 1, num_host + 1 + num_switch):
            self.add_switch(i, flow_table=[])
            nodo.append((i, 'switch'))

        self.add_controller(0)
        nodo.append((0, 'controller'))

        self.add_link(1, 3, 1)
        links.append((1, 3, self.G.nodes[1]['type'], self.G.nodes[3]['type'])) #############################################
        self.add_link(2, 5, 1)
        links.append((2, 5, self.G.nodes[2]['type'], self.G.nodes[5]['type']))
        self.add_link(3, 4, 1)
        links.append((3, 4, self.G.nodes[3]['type'], self.G.nodes[4]['type']))
        self.add_link(3, 5, 5)
        links.append((3, 5, self.G.nodes[3]['type'], self.G.nodes[5]['type']))
        self.add_link(4, 5, 1)
        links.append((4, 5, self.G.nodes[4]['type'], self.G.nodes[5]['type']))
        self.add_link(3, 0, sys.maxsize)
        links.append((3, 0, self.G.nodes[3]['type'], self.G.nodes[0]['type']))
        self.add_link(4, 0, sys.maxsize)
        links.append((4, 0, self.G.nodes[4]['type'], self.G.nodes[0]['type']))
        self.add_link(5, 0, sys.maxsize)
        links.append((5, 0, self.G.nodes[5]['type'], self.G.nodes[0]['type']))
        # G.set_minin(mnam.MiniNAM(list_links=links, list_nodes=nodo))
        print(links,nodo)
        #print(json.dumps(json_graph.node_link_data(self.G), indent=4))
        return links, nodo

    #def save_topology(self):


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


#SDN()

