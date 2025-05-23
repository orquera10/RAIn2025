import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from pyvis.network import Network

def build_graph(graph_data):
    """
    Construye un grafo dirigido con IDs numéricos. 
    Asocia cada URL a un ID y la guarda como atributo.
    """
    G = nx.DiGraph()
    url_to_id = {}
    id_to_url = {}

    # Asignar ID numérico a cada URL
    for i, url in enumerate(graph_data.keys()):
        url_to_id[url] = i
        id_to_url[i] = url
        G.add_node(i, label=url)  # Agregar el nodo con label=URL

    edge_weights = defaultdict(int)

    for source_url, targets in graph_data.items():
        source_id = url_to_id[source_url]
        for target_url in targets:
            if target_url in url_to_id:
                target_id = url_to_id[target_url]
                edge_weights[(source_id, target_id)] += 1

    for (source_id, target_id), weight in edge_weights.items():
        G.add_edge(source_id, target_id, weight=weight)

    return G


def export_graph(graph, filename="grafo_infobae.gexf"):
    """
    Exporta el grafo en formato GEXF con IDs numéricos y las URLs como etiquetas.
    """
    nx.write_gexf(graph, filename)
    print(f"✅ Archivo GEXF guardado exitosamente en: {filename}")
    
def export_graph_html(graph, filename="grafo_infobae.html"):
    print(f"💾 Exportando grafo interactivo a {filename} con {graph.number_of_nodes()} nodos y {graph.number_of_edges()} aristas...")

    net = Network(height="750px", width="100%", directed=True, notebook=False)

    for node, data in graph.nodes(data=True):
        label = data.get('label', str(node))
        net.add_node(node, label=str(node), title=label)

    for source, target, data in graph.edges(data=True):
        weight = data.get('weight', 1)
        net.add_edge(source, target, value=weight)

    net.show_buttons(filter_=['physics'])

    net.write_html(filename)
    print(f"✅ Archivo HTML guardado exitosamente en: {filename}")


def visualize_graph(graph):
    """
    Visualiza el grafo usando los labels (URLs) como etiquetas visibles.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    pos = nx.spring_layout(graph, k=0.9, iterations=50, seed=42)
    
    centrality = nx.degree_centrality(graph)
    node_sizes = [300 + 3000 * centrality[node] for node in graph.nodes()]
    node_colors = list(centrality.values())
    
    edge_weights = [graph[u][v]['weight'] for u, v in graph.edges()]
    
    nodes = nx.draw_networkx_nodes(graph, pos,
                                   node_size=node_sizes,
                                   node_color=node_colors,
                                   cmap=plt.cm.viridis,
                                   alpha=0.9,
                                   ax=ax)
    
    nx.draw_networkx_edges(graph, pos,
                           width=[0.5 + w for w in edge_weights],
                           alpha=0.4,
                           edge_color='gray',
                           ax=ax)
    
    # Mostrar el ID del nodo como etiqueta
    labels = {n: str(n) for n in graph.nodes()}
    
    nx.draw_networkx_labels(graph, pos, labels, font_size=9, ax=ax)
    
    cbar = fig.colorbar(nodes, ax=ax)
    cbar.set_label("Centralidad del nodo", rotation=270, labelpad=15)
    
    ax.set_title("Grafo de enlaces entre noticias de Infobae - Sección Deportes", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.show()
