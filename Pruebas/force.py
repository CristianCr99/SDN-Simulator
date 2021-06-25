from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt
from builtins import range
import os

clear = lambda: os.system('cls')

def menu():
    print("----------- Grafos -----------")
    print("1. Aniadir/Modificar Atributos del grafo")
    print("2. Vaciar Grafo")
    print("3. Crear nodo / Modificar y o aniadir atributos a nodo")
    print("4. Crear enlace / Modificar y o aniadir atributos a enlace")
    print("5. Ver informacion detallada de un nodo")
    print("6. Ver informacion completa del grafo")
    print("7. Comprobar si un camino es valido")
    print("8. Pintar Grafo")
    print("-----------------------------------")
    return input("¿Que opcion desea hacer?")

def insertarOmodificarAtri_Grafo(Grafo):

    opcion = input("Indique si desea asignarle mas atributos al grafo o cambiar alguno existente (si/no):")
    while opcion != 'no':
        nAtributo = input("Introduzca nombre del atributo:")
        vAtributo = input("Introduzca valor del atributo:")
        Grafo.graph[nAtributo] = vAtributo
        opcion = input("Indique si desea asignarle mas atributos al grafo o cambiar alguno existente (si/no):")


def insertarOmodificarAtri_Nodo(Grafo):
    nombre = input("Nombre del nodo:")
    Grafo.add_node(nombre)
    opcion = input("Indique si desea asignarle atributos al nodo o cambiar alguno existente (si/no):")
    while opcion != 'no':
        nAtributo = input("Introduzca nombre del atributo:")
        vAtributo = input("Introduzca valor del atributo:")
        Grafo.nodes[nombre][nAtributo] = vAtributo
        opcion = input("Indique si desea asignarle atributos al nodo o cambiar alguno existente (si/no):")

def insertarOmodificarAtri_Enlace(Grafo):
    enlace1 = input("Nombre del nodo 1:")
    enlace2 = input("Nombre del nodo 2:")
    Grafo.add_edge(enlace1, enlace2)
    opcion = input("Indique si desea asignarle atributos al enlace o cambiar alguno existente (si/no):")
    while opcion != 'no':
        nAtributo = input("Introduzca nombre del atributo:")
        vAtributo = input("Introduzca valor del atributo:")
        Grafo.edges[enlace1, enlace2][nAtributo] = vAtributo
        opcion = input("Indique si desea asignarle atributos al o cambiar alguno existente (si/no):")


def caminoValido(g, p):
    """ Checks whether the list nodes p is a valid path in g."""
    plen = len(p)
    for i in range(plen - 1):
        if not g.has_edge(p[i], p[i + 1]):
            return False
    return True

def hayCaminoPorNodos(Grafo):

    nodo = input("Introduzca el nodo (no para finalizar la entrada de nodos):")
    nodos = []
    while opcion != 'no':
        nodos.append(nodo)
        nodo = input("Introduzca el nodo (no para finalizar la entrada de nodos):")

    return caminoValido(Grafo,nodos)

def hayEnlaceEntreNodos(Grafo, nodo1, nodo2):
    return Grafo.has_edge(nodo1, nodo2)

def verInformacionGrafo(Grafo):
    print('\n\n Características del Grafo G:',
          '\n  Atributos del grafo:', G.graph,
          '\n  Numero de nodos:', Grafo.number_of_nodes(),
          '\n  Numero de arcos:', Grafo.number_of_edges(),
          '\n  Lista de nodos:', list(Grafo.nodes),
          '\n  Lista de arcos:', list(Grafo.edges))

def verInformacionConcretaNodo(Grafo, nodo):
    print('\n  Nodos adyacentes de', nodo, ':', list(Grafo.adj)[nodo],
          '\n  Numero de enlaces incidentes a', nodo, ':', Grafo.degree(nodo),
          '\n  Enlaces de', nodo, ':', Grafo.edges(nodo))

def pintarGrafo(Grafo):
    nx.draw_shell(Grafo, with_labels=True, font_weight='bold')
    plt.show()


G = nx.Graph()

opcion = menu()

while opcion != 0:
    if opcion == "1":
        clear()
        print('     -- Aniadir/Modificar Atributos del grafo --')
        insertarOmodificarAtri_Grafo(G)

    if opcion == "2":
        clear()
        print('     -- Vaciar Grafo --')
        G.clear()
    elif opcion == "3":
        clear()
        print('     -- Crear nodo / Modificar y o aniadir atributos a nodo --')
        insertarOmodificarAtri_Nodo(G)
    elif opcion == "4":
        clear()
        print('     -- Crear enlace / Modificar y o aniadir atributos a enlace --')
        insertarOmodificarAtri_Enlace(G)

    elif opcion == "5":
        clear()
        print('     -- Ver informacion detallada de un nodo --')
        verInformacionConcretaNodo(G, input("Introduzca nombre del nodo:"))

    elif opcion == "6":
        clear()
        print('     -- Ver informacion completa del grafo --')
        verInformacionGrafo(G)

    elif opcion == "7":
        clear()
        print('  -- Comprobar si un camino es valido --')
        hayCaminoPorNodos(G)

    elif opcion == "8":
        clear()
        print('-- Pintar Grafo --')
        pintarGrafo(G)
    else:
        print('Error: Opcion elegida incorrecta.')


    opcion = menu()



