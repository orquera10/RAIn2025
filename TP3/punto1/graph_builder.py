import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def build_graph(graph_data):
    """
    Construye un grafo dirigido a partir del diccionario de enlaces.
    graph_data: dict con {url_nota: [url_nota_enlazada, ...]}
    """
    G = nx.DiGraph()
    edge_weights = defaultdict(int)

    for source, targets in graph_data.items():
        G.add_node(source)
        for target in targets:
            if target in graph_data:  # Solo enlaces dentro del conjunto recolectado
                edge_weights[(source, target)] += 1

    for (source, target), weight in edge_weights.items():
        G.add_edge(source, target, weight=weight)

    return G


def export_graph(graph, filename="grafo_infobae.gexf"):
    """
    Exporta el grafo a un archivo GEXF (Gephi compatible).
    """
    nx.write_gexf(graph, filename)
    print(f"Grafo exportado a {filename}")


def visualize_graph(graph):
    """
    Visualiza el grafo con nodos coloreados y escalados según su centralidad.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Distribución de nodos
    pos = nx.spring_layout(graph, k=0.5, iterations=50, seed=42)
    
    # Centralidad de los nodos (grado normalizado)
    centrality = nx.degree_centrality(graph)
    node_sizes = [300 + 3000 * centrality[node] for node in graph.nodes()]
    node_colors = list(centrality.values())
    
    # Pesos de las aristas
    edge_weights = [graph[u][v]['weight'] for u, v in graph.edges()]
    
    # Dibujar nodos
    nodes = nx.draw_networkx_nodes(graph, pos,
                                   node_size=node_sizes,
                                   node_color=node_colors,
                                   cmap=plt.cm.viridis,
                                   alpha=0.9,
                                   ax=ax)
    
    # Dibujar aristas
    nx.draw_networkx_edges(graph, pos,
                           width=[0.5 + w for w in edge_weights],
                           alpha=0.4,
                           edge_color='gray',
                           ax=ax)
    
    # Etiquetas (ID simple)
    labels = {
        n: n.split("/")[-2][:25] + "..."  # Limita a 25 caracteres
        for n in graph.nodes()
    }
    nx.draw_networkx_labels(graph, pos, labels, font_size=9, ax=ax)
    
    # Barra de color
    cbar = fig.colorbar(nodes, ax=ax)
    cbar.set_label("Centralidad del nodo", rotation=270, labelpad=15)
    
    ax.set_title("Grafo de enlaces entre noticias de Infobae - Sección Deportes", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.show()

# def visualize_graph(graph):
#     """
#     Visualiza un grafo dirigido simple con etiquetas de nodos (simplificadas)
#     y pesos en las aristas. Sin color ni escalado.
#     """
#     fig, ax = plt.subplots(figsize=(14, 10))

#     # Posiciones de los nodos
#     pos = nx.spring_layout(graph)

#     # Dibujar nodos (todos mismo tamaño y color)
#     nx.draw_networkx_nodes(graph, pos, node_color="skyblue", ax=ax)

#     # Dibujar aristas con flechas
#     nx.draw_networkx_edges(graph, pos, arrowstyle='->', arrowsize=12, edge_color="gray", ax=ax)

#     # Etiquetas simplificadas de nodos (última parte de la URL)
#     labels = {
#         n: n.split("/")[-2][:25] + "..."  # Limita a 25 caracteres
#         for n in graph.nodes()
#     }
#     nx.draw_networkx_labels(graph, pos, labels=labels, font_size=7, ax=ax)

#     ax.set_title("Grafo simple de enlaces entre noticias", fontsize=14)
#     ax.axis('off')
#     plt.tight_layout()
#     plt.show()
