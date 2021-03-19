from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt
from builtins import range
from datetime import date
import sys
import MiniNAM as mn


def menu():
    print("\n\n---------------------- Grafos ----------------"
          "------")
    print("1. Aniadir/Modificar Atributos del grafo")
    print("2. Vaciar Grafo")
    print("3. Crear nodo / Modificar y o aniadir atributos a"
          " nodo")
    print("4. Crear enlace / Modificar y o aniadir atributos"
          " a enlace")
    print("5. Ver informacion detallada de un nodo")
    print("6. Ver informacion detallada de un enlace")
    print("7. Ver informacion general del grafo")
    print("8. Comprobar si un camino es valido")
    print("9. Crear Grafo por defecto con nodos, atributos,"
          " enlaces ...")
    print("10. Pintar Grafo")
    print("11. Ejecutar algoritmo camino mas corto desde "
          "un nodo al resto")
    print("12. Ejecutar algoritmo camino mas corto entre "
          "cada par de nodos")
    print("-----------------------------------------------"
          "----------")
    return input("¿Que opcion desea hacer (0 para salir)? ")


def insertarOmodificarAtri_Grafo(G):
    opcion = input("Indique si desea asignarle mas atributos"
                   " al grafo"
                   " o cambiar alguno existente (si/no):")
    while opcion != 'no':
        nAtributo = input("Introduzca nombre del atributo:")
        vAtributo = input("Introduzca valor del atributo:")
        G.graph[nAtributo] = vAtributo
        opcion = input("Indique si desea asignarle mas "
                       "atributos al "
                       "grafo o cambiar alguno existente "
                       "(si/no):")


def insertarOmodificarAtri_Nodo(G):
    nombre = input("Nombre del nodo:")
    G.add_node(nombre)
    opcion = input("Indique si desea asignarle atributos "
                   "al nodo o "
                   "cambiar alguno existente (si/no):")
    while opcion != 'no':
        nAtributo = input("Introduzca nombre del atributo:")
        vAtributo = input("Introduzca valor del atributo:")
        G.nodes[nombre][nAtributo] = vAtributo
        opcion = input("Indique si desea asignarle atributos"
                       " al nodo "
                       "o cambiar alguno existente (si/no):")


def insertarOmodificarAtri_Enlace(G):
    enlace1 = input("Nombre del nodo 1:")
    enlace2 = input("Nombre del nodo 2:")
    G.add_edge(enlace1, enlace2)
    opcion = input("Indique si desea asignarle atributos al"
                   " enlace o cambiar alguno existente (si/no):")
    while opcion != 'no':
        nAtributo = input("Introduzca nombre del atributo:")
        vAtributo = int(input("Introduzca valor del atributo"
                              " (valor entero):"))
        G.edges[enlace1, enlace2][nAtributo] = vAtributo
        opcion = input("Indique si desea asignarle atributos al o "
                       "cambiar alguno existente (si/no):")


def caminoValido(g, p):
    plen = len(p)
    for i in range(plen - 1):
        if not g.has_edge(p[i], p[i + 1]):
            return False
    return True


def hayCaminoPorNodos(G):
    nodo = input("Introduzca el nodo (no para finalizar la entrada"
                 " de nodos):")
    nodos = []
    while nodo != 'no':
        nodos.append(nodo)
        nodo = input("Introduzca el nodo (no para finalizar la "
                     "entrada de nodos):")
    return caminoValido(G, nodos)


def hayEnlaceEntreNodos(G, nodo1, nodo2):
    return G.has_edge(nodo1, nodo2)


def verInformacionGrafo(G):
    print('\n\n  Características del Grafo G:',
          '\n    Atributos del grafo:', G.graph,
          '\n    Numero de nodos:', G.number_of_nodes(),
          '\n    Numero de arcos:', G.number_of_edges(),
          '\n    Lista de nodos:', list(G.nodes),
          '\n    Lista de arcos:', list(G.edges))


def verInformacionConcretaNodo(G):
    nodo = int(input("Introduzca nombre del nodo:"))
    print('\n  Informacion del nodo:', nodo,
          '\n    Atributos del nodo:', G.nodes[nodo],
          '\n    Numero de enlaces incidentes a', nodo, ':',
          G.degree(nodo),
          '\n    Enlaces de', nodo, ':', G.edges(nodo))

    # print(tuple(list(G.edges(nodo))[0])[1])
    # print(G.(nodo))
    # destino = G.edges('h1')
    # h = destino.items()
    # destino.
    # print(destino)


def verInformacionConcretaEnlace(G):
    nodo1 = int(input("Introduzca nombre del nodo:"))
    nodo2 = int(input("Introduzca nombre del nodo:"))
    print('\n  Caracteristicas del enlace: (', nodo1, nodo2,
          ')',
          '\n    Atributos:', G.edges[nodo1, nodo2])


def pintarGrafo(G):
    nx.draw_shell(G, with_labels=True, font_weight='bold')
    plt.show()


def caminoMasCorto(G):
    nodo = input("Introduzca nombre del nodo:")
    nodoPredecesor, distanciaNodo = \
        nx.dijkstra_predecessor_and_distance(G, nodo,
                                             cutoff=None,
                                             weight='weight')
    print('Lista de nodos predecesores para llegar al '
          'nodo i desde el nodo', nodo, ':',
          sorted(nodoPredecesor.items()))
    print('Distancia a cada nodo desde el nodo', nodo,
          ':', sorted(distanciaNodo.items()))


def all_dijkstra_path(G):
    nodo1 = input("Introduzca nombre del nodo1:")
    nodo2 = input("Introduzca nombre del nodo2:")
    camino = dict(nx.all_pairs_dijkstra_path(G,
                                             cutoff=None,
                                             weight='weight'))
    print('Camino a seguir para ir del nodo', nodo1,
          'al nodo', nodo2, camino[nodo1][nodo2])
    nx.dijkstra_path(G, '0', '4')  # Esta es la funcion que debería usar


# *************************************** Esta es la parte de SDN ***************************************

class tablaFlujo:

    def __init__(self):
        self.listaEntradasFlujo = {}

    def insertarEntradaFlujo(self, identificadorFlujo, hOrigen, hDestino):
        self.listaEntradasFlujo[identificadorFlujo] = (hOrigen, hDestino)

    def borrarEntradaFlujo(self, identificadorFlujo):
        del self.listaEntradasFlujo[identificadorFlujo]

    def obtenerOrigenDestinoFlujo(self, identificadorFlujo):
        return self.listaEntradasFlujo.get(identificadorFlujo)

    def existeFlujo(self, identificadorFlujo):
        return self.listaEntradasFlujo.has_key(identificadorFlujo)


def grafoPorDefecto(G, mapaTablasSwitches):
    flujos = []
    tablaFlujos = tablaFlujo()

    for i in range(1, 3):
        G.add_nodes_from([('h' + str(+i), {'tipo': 'Host', 'flujos': flujos})])

    for i in range(1, 4):
        G.add_nodes_from([('s' + str(i), {"tipo": "Switch", tablaFlujos: tablaFlujo()})])
        mapaTablasSwitches['s' + str(i)] = tablaFlujo()

    G.add_nodes_from([('c' + str(1), {"tipo": "Controlador"})])

    G.add_edges_from([('h1', 's1', {'weight': 1}),
                      ('h2', 's3', {'weight': 1}),
                      ('s1', 's2', {'weight': 1}),
                      ('s1', 's3', {'weight': 1}),
                      ('s2', 's3', {'weight': 1}),
                      ('s1', 'c1', {'weight': sys.maxsize}),
                      ('s2', 'c1', {'weight': 1}),
                      ('s3', 'c1', {'weight': 1})])
    G.graph['Nombre'] = "G"
    G.graph['FechaCreacion'] = format(date.today())


'''
G = nx.Graph()

opcion = menu()

while opcion != "0":
    try:
        if opcion == "1":
            print(' \n\n\n\n-- Aniadir/Modificar Atributos '
                  'del grafo --')
            insertarOmodificarAtri_Grafo(G)
        elif opcion == "2":
            print('\n\n  -- Vaciar Grafo --')
            G.clear()
        elif opcion == "3":
            print('\n\n  -- Crear nodo / Modificar y o '
                  'aniadir atributos a nodo --')
            insertarOmodificarAtri_Nodo(G)
        elif opcion == "4":
            print('\n\n  -- Crear enlace / Modificar y o '
                  'aniadir atributos a enlace --')
            insertarOmodificarAtri_Enlace(G)
        elif opcion == "5":
            print('\n\n  -- Ver informacion detallada de '
                  'un nodo --')
            verInformacionConcretaNodo(G)
        elif opcion == "6":
            print('\n\n  -- Ver informacion completa del '
                  'enlace --')
            verInformacionConcretaEnlace(G)
        elif opcion == "7":
            print('\n\n  -- Ver informacion completa del'
                  ' grafo --')
            verInformacionGrafo(G)
        elif opcion == "8":
            print('\n\n  -- Comprobar si un camino es'
                  ' valido --')
            print('Hay camino:',hayCaminoPorNodos(G))
        elif opcion == "9":
            print('\n\n  -- Crear Grafo por defecto con'
                  ' nodos, atributos, enlaces ...  --')
            grafoPorDefecto(G)
        elif opcion == "10":
            print('\n\n  -- Pintar Grafo --')
            pintarGrafo(G)
        elif opcion == "11":
            print('\n\n  -- Camino mas corto de desde un'
                  ' nodo al resto --')
            caminoMasCorto(G)
        elif opcion == "12":
            print('\n\n  -- Camino mas corto entre cada'
                  ' par de nodo --')
            all_dijkstra_path(G)
        elif opcion == "13":
            print('\n\n  -- xxx --')
            SDN(G)
        else:
            print('\n\n  Error: Opcion elegida '
                  'incorrecta.')
    except Exception as exc:
        print('Ha ocurrido algun error:', exc)
    opcion = menu()

'''


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
        # self.MNAM = mn.MiniNAM()

    def get_graph(self):
        return (self.G)

    def add_switch(self, num_switch, flow_table=[]):
        self.G.add_node(num_switch, tipo='switch', name='s' + str(num_switch), flow_table=flow_table)
        # self.MNAM.addNode(num_switch,'switch')

    def add_host(self, num_host):
        self.G.add_node(num_host, tipo='host', name='h' + str(num_host))
        # self.MNAM.addNode(num_host, 'host')

    def add_controller(self, num_controller):
        self.G.add_node(num_controller, tipo='controller', name='c' + str(num_controller))
        # self.MNAM.addNode(num_controller, 'controller')

    def add_link(self, node_a, node_b, weight_link):
        self.G.add_edge(node_a, node_b, weight=weight_link)
        name1 = self.G.nodes[node_a]['name']
        name2 = self.G.nodes[node_b]['name']
        # self.MNAM.drawLink(self.G.nodes[node_a]['name'], self.G.nodes[node_b]['name'])

    def add_flow_entry_to_node(self, node, flowentry):
        self.G.nodes[node]['flow_table'].append(flowentry)

    def create_topology(self):

        self.G = NetworkTopology()


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

    def controller_action(self, id, h_src, h_dst, switch, proactive):
        # verInformacionConcretaNodo(self.G)
        all_path = dict(nx.all_pairs_dijkstra_path(self.G, cutoff=None, weight='weight'))

        path = nx.dijkstra_path(self.G, h_src, h_dst, 'weight')

        # Enviamos a cada Switch un flowMod (Enviar graficamente)

        for i in range(1, len(path) - 1):

            if proactive == True:
                self.add_flow_entry_to_node(path[i], FlowEntry(id, h_src, h_dst, path[i + 1]))
                print('flowMod a ', path[i])
            if path[i] == switch:
                action = path[i + 1]

        # Enviamos paquet_out a switch (Enviar graficamente)
        print('paquetOut a ', switch)
        return action

    def communication_hots(self, id, h_src, h_dst):

        if self.G.degree(h_src) == 1:  # solo puede un host estar conectado a un Switch

            listEnlaces = list(self.G.edges(h_src))
            Switch = int(tuple(listEnlaces[0])[1])  # Cogemos el Switch al cual esta conectado [1]
            print('Enviamos paquete a', Switch)
            has_arrived = False

            while has_arrived == False:

                action = self.match_and_action(Switch, id, h_src, h_dst)

                if action == 0:
                    print('No Matchin')
                    action = self.controller_action(id, h_src, h_dst, Switch, True)

                print('enviamos paquete a', action)

                # Reenviamos el paquete a al siguiente Switch indicado por action (Enviar graficamente)
                Switch = action

                if action == h_dst:
                    # Se envia al host destino y ha llegado al destino (Enviar graficamente)
                    print('Llega paquete al destino', action)
                    has_arrived = True
                else:
                    print('Llega paquete a', action)

                # Enviamos paquet_in al controlador


def SDN():
    # Creación de una instancia de la clase NetworkTopology
    graph = NetworkTopology()
    # Añadimos la entrada de flujo a la lista de entradas de flujos del nodo 1 de la topologia de red (instancia de la clase FlowEntry (src=1,dst=4,id=0))
    # graph.add_flow_entry_to_node(1, FlowEntry(1, 4, 0, ))
    # Añadimos la entrada de flujo a la lista de entradas de flujos del nodo 1 de la topologia de red (otra instancia de la clase FlowEntry (src=1,dst=8,id=1))
    # graph.add_flow_entry_to_node(1, FlowEntry(1, 8, 1))
    # Comprobamos que se añade correctamente
    # graph.show_flow_table(1)
    # verInformacionConcretaNodo(graph)
    # verInformacionConcretaEnlace(graph)
    # graph.add_flow_entry_to_node(1, FlowEntry(1, 8, 1, 1))
    # graph.show_flow_table(1)

    for i in range(1, 3):
        graph.add_host(i)
    for i in range(3, 6):
        graph.add_switch(i, flow_table=[])

    graph.add_controller(6)

    # self.MNAM.createNodes()
    # self.MNAM.createNodes()
    # self.MNAM.drawLink('h1', 'h2')

    graph.add_link(1, 3, 1)
    graph.add_link(2, 5, 1)
    graph.add_link(3, 4, 1)
    graph.add_link(3, 5, 5)
    graph.add_link(4, 5, 1)
    graph.add_link(3, 6, sys.maxsize)
    graph.add_link(4, 6, sys.maxsize)
    graph.add_link(5, 6, sys.maxsize)


    graph.communication_hots(1, 1, 2)
    graph.communication_hots(1, 1, 2)


def comunicacionHosts(G, hOrigen, hDestino, idFlujo):
    if G.degree(hOrigen) == 1:  # solo puede un host estar conectado a un Switch
        listaEnlaces = list(G.edges(hOrigen))
        Switch = tuple(listaEnlaces[0])[1]  # Cogemos el Switch al cual esta conectado [1]
        # Cogemos la tabla de flujos del S:
        # hola = mapTablas.get(Switch)


SDN()
