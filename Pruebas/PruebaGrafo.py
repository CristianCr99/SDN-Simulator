from __future__ import print_function
import networkx as nx
import matplotlib.pyplot as plt
from builtins import range
from networkx.readwrite import json_graph
import json
from datetime import date

def path_valid(g, p):
    """ Checks whether the list nodes p is a valid path in g."""
    plen = len(p)
    for i in range(plen - 1):
        if not g.has_edge(p[i], p[i + 1]):
            return False
    return True


def caracteristicasGrafo(G):
    # Muestro las características de mi grafo:
    print('\n\nCaracterísticas del Grafo G:', '\n\nNumero de nodos:', G.number_of_nodes(), '\nNumero de arcos:',
          G.number_of_edges(), '\nLista de nodos:', list(G.nodes), '\nLista de arcos:', list(G.edges),
          '\nNodo adyacente de hola:',list(G.adj)[6], '\nNumero de enlaces incidentes a hola:', G.degree('hola'),
          '\nNumero de enlaces incidentes a hola y a o:', G.degree(['hola', 'o']), '\nEnlaces de h:', G.edges('h'),
          '\nEnlaces de h y o:', G.edges(['h', 'o']))  # Pregunta: Por que a partir de 6 da error si tenemos 10 nodos



# Creo un grafo (G):
G = nx.Graph()

# Creamos nodos en el grafo G:
G.add_node(1)
G.add_nodes_from([2, 3])
G.add_nodes_from([
    (4, {"color": "red"}),
    (5, {"color": "green"}),
])

G.add_node("hola")  # Creamos el nodo hola
G.add_nodes_from("hola")  # Creamos los nodos 'h' 'o' 'l' 'a'

# Creamos los enlaces entre los nodos (de diferent4s maneras):

G.add_edge(1, 2)
G.add_edges_from([(1, 2), (1, 3)])  # Aquí los aniadimos mediante una lista de tuplas
G.add_edges_from([('hola', 'h'), ('hola', 'o')])
G.add_edges_from([(1, 4), (1, 5), (5, 'o')])
caracteristicasGrafo(G)

# ********** Podemos crear un grafo a partir de otro mediante el contructor parametrizado (Grafo nuevo H) **************

# Creacion de un nuevo grafo a partir del contructor parametrizado
H = nx.Graph(G)

# Podemos eliminar nodos y enlaces:
H.remove_node(2)
H.remove_nodes_from("hola")
H.remove_edge(1, 3)

print('\n\nLista de nodos de H:', list(H.nodes), '\nLista de enlaces de H:', list(H.edges))

# Eliminamos todos los nodos y enlaces:
H.clear()

print('\n\nLista de nodos de H:', list(H.nodes), '\nLista de enlaces de H:', list(H.edges))

# **********************************************************************************************************************


# Podemos asignar atributos a los grafos, a los enlaces y a los nodos:

# Atributos de un grafo:

G.graph['Nombre'] = "G"
G.graph['FechaCreacion'] = format(date.today())
print("\n\nAtributos del Grafo:\n  ", G.graph, '\n  Nombre: ', G.graph['Nombre'], '\n  Fecha Creacion: ',
      G.graph['FechaCreacion'])

# Atributos de un nodo:

G.add_node('hola',
           Tipo='Letra')  # Se pueden aniadir cuando aniades un nuevo nodo o despues (y modificarlo, obviamente).
G.nodes['hola']['Tamanio'] = '4 bytes'
G.nodes['hola']['Tipo'] = 'Palabra'

print('\n\nTodos los atributos de un grafo:\n',
      G.nodes.data())  # Podemos ver de esta manera todos los atributos de todos los nodos del grafo

# Nota: Tambien podemos establecer los atributos de los nosdos cuando los aniadimos al grafo, como se ha hecho al aniador los nodos 4 y 5

# Atributos de un enlace:

G.edges['hola', 'h']['Peso'] = 5.0

print('\nAtributos de todos los enlaces:', G.edges.data())
print('\nPeso del enlace (hola,h):', G.edges['hola', 'h']['Peso'])

# Podemos ver si hay enlaces entre nodos:
print("Hay enlace entre los nodos 1 y 2?", G.has_edge(1, 2))

# Podemos ver si hay camino entre nodos:
print("Hay camino entre los nodos 1 y h?", path_valid(G, [2, 1, 5]))

# Podemos acceder a nodos y ver y cambiar sus caracteristicas:
# print('Nodos adyacentes a 1 y sus características (caracteristicas del enlace que los une):', G[1])

# print(G[1])

# G = nx.Graph([(1, 2, {"color": "yellow"})])
# print(G[1][2])

nx.draw_networkx(G)
# Podemos pintar el nodo:
#nx.draw_shell(G, with_labels=True, font_weight='bold')
plt.show()



# Si quisieramos exportar el grafo por completo lo haríamos de la siguiente manera:
print(json.dumps(json_graph.node_link_data(G), indent=4))

# Este enlace muestra como importar y exportar archivos json: https://www.analyticslane.com/2018/07/16/archivos-json-con-python/
# También revisar este enlace: https://www.grotto-networking.com/SDNfun.html
# Lectura de un json:
#gnl = json.load(open("../exampleNets/MultiSwitchVLANNet1.json"))
#print("gnl = {}".format(gnl))
#g = json_graph.node_link_graph(gnl)
