from __future__ import print_function

from builtins import range
from datetime import date

import matplotlib.pyplot as plt
import networkx as nx


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
    nodo = input("Introduzca nombre del nodo:")
    print('\n  Informacion del nodo:', nodo,
          '\n    Atributos del nodo:', G.nodes[nodo],
          '\n    Numero de enlaces incidentes a', nodo, ':',
          G.degree(nodo),
          '\n    Enlaces de', nodo, ':', G.edges(nodo))


def verInformacionConcretaEnlace(G):
    nodo1 = input("Introduzca nombre del nodo:")
    nodo2 = input("Introduzca nombre del nodo:")
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


def grafoPorDefecto(G):
    G.add_edges_from([('h1', 's1', {'weight': 1}),
                      ('s1', 'c0', {'weight': 1}),
                      ('c0', 's2', {'weight': 1}),
                      ('c0', 's3', {'weight': 1}),
                      ('s1', 's2', {'weight': 1}),
                      ('s1', 's3', {'weight': 1}),
                      ('s1', 's3', {'weight': 1}),
                      ('s2', 's3', {'weight': 1}),
                      ('s2', 'h2', {'weight': 1})])
    G.graph['Nombre'] = "G"
    G.graph['FechaCreacion'] = format(date.today())


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
            print('Hay camino:', hayCaminoPorNodos(G))
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
        else:
            print('\n\n  Error: Opcion elegida '
                  'incorrecta.')
    except Exception as exc:
        print('Ha ocurrido algun error:', exc)
    opcion = menu()
