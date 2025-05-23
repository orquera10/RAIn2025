from crawler import get_initial_articles, crawl_articles
from graph_builder import build_graph, export_graph, visualize_graph, export_graph_html

def main():
    print("🔍 Recolectando artículos...")
    urls = get_initial_articles(limit=30)
    print(f"{len(urls)} artículos encontrados")

    print("🔗 Extrayendo enlaces internos...")
    data = crawl_articles(urls)

    print("🧠 Construyendo grafo...")
    graph = build_graph(data)

    print(f"💾 Exportando grafo con {graph.number_of_nodes()} nodos y {graph.number_of_edges()} aristas...")
    export_graph(graph, 'grafo_infobae.gexf')
    export_graph_html(graph, 'grafo_infobae.html')

    print("📊 Mostrando visualización...")
    visualize_graph(graph)


if __name__ == '__main__':
    main()
