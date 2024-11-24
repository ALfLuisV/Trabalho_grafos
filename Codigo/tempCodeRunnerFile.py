
    print("9. Deletar aresta")
    print("10. Checar adjacência entre vértices")
    print("11. Checar adjacência entre arestas")
    print("12. Checagem da existência de arestas")
    print("13. Checagem da quantidade de vértices e arestas")
    print("14. Checagem de grafo vazio e completo")
    print("15. Checagem de articulações (por busca em profundidade)")
    print("16. Exibir matriz de adjacência")
    print("17. Exibir matriz de incidência")
    print("18. Verificar conectividade")
    print("19. Verificar conectividade (naive)")
    print("20. Exibir lista de adjacência")
    print("21. Exportar CSV")
    print("22. Sair")
    return input("Escolha uma opção: ")

def criar_vertices_iniciais(grafo):
    try:
        num_vertices = int(input("Quantos vértices deseja criar? "))
        if num_vertices < 1: