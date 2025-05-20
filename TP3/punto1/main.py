from crawler import get_initial_articles, crawl_articles
from graph_builder import build_graph, export_graph, visualize_graph

def main():
    print("🔍 Recolectando artículos...")
    urls = get_initial_articles(limit=30)
    print(f"{len(urls)} artículos encontrados")

    print("🔗 Extrayendo enlaces internos...")
    data = crawl_articles(urls)

    print("🧠 Construyendo grafo...")
    graph = build_graph(data)

    export_graph(graph, 'grafo_infobae.gexf')

    print("📊 Mostrando visualización...")
    visualize_graph(graph)

if __name__ == '__main__':
    main()
