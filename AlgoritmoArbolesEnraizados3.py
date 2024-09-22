#!/usr/bin/env python
# coding: utf-8

# # 1.	Lista todos los árboles enraizados de N vertices

# ## Autores: Laia Delgado y Laura Llorente

# Para hacer este algoritmo hemos consultado las siguientes fuentes:
# - https://webhome.cs.uvic.ca/~ruskey/Theses/GangLiMScThesis.pdf
# - https://networkx.org/documentation/latest/tutorial.html

# Librerías usadas para el algoritmo. Si no están instaladas en el entorno, es necesario instalarlas con las siguientes lineas de código:

# In[1]:


# pip install networkx
# pip install matplotlib
# pip install math


# ## Código

# ### Importación de las librerías:

# - networkx permite crear árboles
# - matplotlib.pyplot realiza la visualización de los árboles
# - math realiza algunos cálculos matemáticos necesarios

# In[2]:


import networkx as nx
import matplotlib.pyplot as plt
import math


# ### Generaración de los árboles enraizados

# Para poder generar todos los árboles enraizados hemos hecho tres funciones:
# - def generate_rooted_trees(n) que se encarga de almacenar los árboles en una lista
# - def isomorphic(tree1, tree2) que comprueba si dos árboles son isomorfos
# - def generate_trees_recursive(tree, n, trees) que genera los árboles

# Hacemos uso de un backtracking simplificado, ya que comprobamos todas  las posibles combinaciones de nodos (de forma recursiva) asegurándonos de que cada árbol sea único y no haya isomorfismos. Además tenemos un caso final, cuando se ha completado el árbol, y un caso inicial, cuando todavía no hay ningún nodo raíz. 

# La siguiente imagen ilustra como funcionaría el algoritmo para buscar los árboles enraizados no isomorfos de 5 vértices:
# ![image.png](attachment:f92c96e8-0245-4daf-8e2d-9078642a98c9.png)
# 
# Se puede observar cómo se empieza teniendo un sólo vértice y poco a poco se van añadiendo más hasta tener los 5 que se han pedido.

# In[3]:


def generate_rooted_trees(n):
    trees = [] # Lista para almacenar todos los árboles enraizados no isomorfos de n vértices
    generate_trees_recursive(nx.DiGraph(), n, trees) # Llamada a la función generate_trees_recursive para generar los árboles
    return trees # Retorno con la lista completa de árboles enraizados

def isomorphic(tree1, tree2):
    return nx.is_isomorphic(tree1, tree2) # Con la función is_isomorphic de la librería networkx se comprueba el isomorfismo

def generate_trees_recursive(tree, n, trees):
    # Caso especial: árbol de un solo vértice
    if n == 1:
        tree.add_node(0)  # Añade un solo nodo al árbol
        trees.append(tree.copy())  # Añade el árbol a la lista de árboles
        return

    # Se comprueba si se ha llegado al final, es decir, si el árbol ya tiene los n vértices deseados
    if len(tree.nodes()) == n:
        # Se recorre toda la lista de los árboles para ver si existing_tree es isomorfo a alguno de la lista
        for existing_tree in trees:
            # Se comprueba si los árboles son isomorfos
            if isomorphic(tree, existing_tree):
                return
        
        # Si el árbol no es isomorfo a ninguno de los de la lista, se añade
        trees.append(tree.copy())
        return

    # Se comprueba si el árbol está vacío, y si lo está, se inicializa el árbol con el nodo raíz
    if len(tree.nodes()) == 0:
        tree.add_node(0) # Se añade el nodo 0 al árbol

    # Se recorren todos los nodos del árbol
    for parent in tree.nodes():
        new_node = max(tree.nodes()) + 1 # Se crea un nuevo nodo cogiendo el máximo índice actual y añadiendo 1
        tree.add_node(new_node) # Se añade el nuevo nodo al árbol
        tree.add_edge(parent, new_node) # Se añade un arista entre el nodo actual (parent) y el nuevo nodo (new_node)
        generate_trees_recursive(tree, n, trees) # Llamada a la función generate_trees_recursive con el árbol actual 
        tree.remove_node(new_node) # Después de ver todas las posibles adiciones de nodos desde el nodo padre, se elimina el nuevo nodo


# ### Visualización de los árboles enraizados

# Para poder tener una visualización clara de los árboles, hemos hecho dos funciones:
# - visualize_trees(trees) que muestra todos los árboles
# - hierarchy_pos que calcula las posiciones de los nodos en el árbol con el objetivo de tener uan visualización jerárquica

# In[4]:


def visualize_trees(trees):
    num_trees = len(trees) # Obtiene la cantidad de árboles que hay en la lista
    rows = math.ceil(math.sqrt(num_trees)) # Obtiene el número de filas
    cols = math.ceil(num_trees / rows) # Obtiene el número de columnas
    
    plt.figure(figsize=(cols*5, rows*5)) # Crea una figura de marplotlib para organizar la distribución de los árboles
    
    def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
        # Si G no tiene una estructura de árbol
        if not nx.is_tree(G):
            raise TypeError('G no es un árbol.') # Se lanza una excepción

        # Se comprueba si el diccionario pos no ha sido proporcionado
        if pos is None:
            pos = {root: (xcenter, vert_loc)} # Se inicializa el diccionario pos con el nodo raíz y su posición xcenter y vert_loc
        else: # En caso contrario 
            pos[root] = (xcenter, vert_loc) # Se actuliza para el nodo raíz con las coordenadas especificadas
        
        children = list(G.neighbors(root)) # Se obtiene una lista de los nodos hijos

        # Se compruba si tiene algún hijo
        if len(children) != 0:
            dx = width / 2 # Calcula el ancho disponible para cada nodo hijo
            nextx = xcenter - width/2 - dx/2 # Calcula la posición horizontal del primer nodo hijo con respecto del centro del nodo padre
            # Se recorre cada nodo hijo
            for child in children:
                nextx += dx # Se ajusta la psoción horizontal para el siguiente nodo hijo
                pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed) # Llamada recursiva a la función hierarchy_pos para calcular las posiciones de los nodos hijos  
        
        return pos # Retorno del diccionario con las posiciones de todos los nodos del árbol

    # Se recorren todos los árboles de la lista junto con el ínidice i
    for i, tree in enumerate(trees):
        plt.subplot(rows, cols, i+1) # Crea un subplot en la posición correspondiente en la cuadrícula para el árbol actual
        pos = hierarchy_pos(tree, 0) # Calcula las posisiciones de los nodos del árbol actual
        nx.draw(tree, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=12) # Dibuja el árbol actual con las posiciones calculadas
        root_node = next(node for node, in_degree in tree.in_degree() if in_degree == 0) # Encuentra el nodo raíz del árbol actual
        nx.draw_networkx_nodes(tree, pos, nodelist=[root_node], node_color='red', node_size=700) # Pinta de rojo el nodo raíz del árbol actual
    
    plt.tight_layout() # Ajsuta de forma automática el diseño de la figura para evitar que se superpongan
    plt.show() # Muestra la visualizacion


# ### Función main

# In[5]:


if __name__ == "__main__":
    
    while True:
        try:
            n = int(input("Ingrese el número de vértices para generar los árboles enraizados (entero positivo): "))
            if n <= 0:
                print("El número de vértices debe ser un entero positivo.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    trees = generate_rooted_trees(n)
    print(f"Se generaron {len(trees)} árboles enraizados de {n} vértices.")
    visualize_trees(trees)


# ### Extra

# Este código es el primero que hicimos. Sin embargo, se obtienen todos los árboles enraizados de n vértices sin tener en cuenta si son isomorfos o no, por lo que como resultado final mostraba más árboles de los que debería (en el enunciado asumimos que debían ser árboles no isomorfos).

# Además, en este primer código que hicimos, la visualización de los árboles puede ser más liosa y difícil de comprobar si hay algún árbol isomorfo, pues no están distribuidos de una forma jerárquica (como en el código de arriba) y sólo se identifica el nodo raíz.
# Es por esto que en el código de arriba decidimos mejorar la representación de los árboles, de forma que saliera una "capa" de vértices debajo de otra sucesivamente, según se fueran añadiendo al grafo debajo del vértice correspondiente.

# Por otra parte, este primer código tampoco cuenta con un main donde te pide por pantalla cuántos vértices quieres, ya que lo pensamos después.

# In[ ]:


"""
import networkx as nx
import matplotlib.pyplot as plt
import math

def generate_rooted_trees(n):
    trees = []
    generate_trees_recursive(nx.DiGraph(), n, trees)
    return trees

def generate_trees_recursive(tree, n, trees):
    if len(tree.nodes()) == n:
        trees.append(tree.copy())
        return

    if len(tree.nodes()) == 0:
        tree.add_node(0)

    for parent in tree.nodes():
        new_node = max(tree.nodes()) + 1
        tree.add_node(new_node)
        tree.add_edge(parent, new_node)
        generate_trees_recursive(tree, n, trees)
        tree.remove_node(new_node)

def visualize_trees(trees):
    num_trees = len(trees)
    rows = math.ceil(math.sqrt(num_trees))
    cols = math.ceil(num_trees / rows)

    plt.figure(figsize=(cols*5, rows*5))

    for i, tree in enumerate(trees):
        plt.subplot(rows, cols, i+1)
        pos = nx.spring_layout(tree)
        nx.draw(tree, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=12)
        root_node = [node for node, in_degree in tree.in_degree() if in_degree == 0][0]
        nx.draw_networkx_nodes(tree, pos, nodelist=[root_node], node_color='red', node_size=700)

    plt.tight_layout()
    plt.show()

n = 4
trees = generate_rooted_trees(n)
print(f"Se generaron {len(trees)} árboles enraizados de {n} vértices.")
visualize_trees(trees)
"""


# ## Comprobación

# Hemos comprobado a mano que los resultados eran ciertos hasta 6 vértices. Es decir, hemos dibujado los árboles enraizados hasta 6 vértices y hemos visto que coincidían con los resultados que nos daba nuestro algoritmo. 
# ![arboles_6vertices.jpg](attachment:03afcc37-8a1a-4ec2-8a9f-706a00bc2bee.jpg)
# 
# Por otra parte, como ya a partir de 6 vértices había muchos árboles, nos dimos cuenta de que podíamos calcular la cantidad de árboles que iban a existir. Así que otra forma que hemos hecho para comprobar los resultados es si estos nos daban la misma cantidad. A continuación, mostramos una imagen en la se ilustra la cantidad de grafos que tiene que haber hasta 7 vértices:
# ![null.png](attachment:0bd27d65-29af-45cf-9dae-4ce7e54a7d5d.png)

# In[ ]:




