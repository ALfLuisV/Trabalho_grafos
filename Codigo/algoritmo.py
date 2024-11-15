from grafo import Grafo

def kosaraju(grafo: Grafo):
    # 1º Passo: Realizar uma DFS e salvar os tempos de término
    tempos_termino = []
    visitados = set()

    def dfs1(vertice, tempo):
        visitados.add(vertice.rotulo)
        for aresta in vertice.arestas:
            if aresta.vertices[0] == vertice:
                prox_vertice = aresta.vertices[1]
                if prox_vertice.rotulo not in visitados:
                    tempo = dfs1(prox_vertice, tempo)
        tempos_termino.append(vertice)
        return tempo + 1

    for vertice in grafo.vertices:
        if vertice.rotulo not in visitados:
            dfs1(vertice, 0)

    # 2º Passo: Construir o grafo transposto
    grafo_transposto = Grafo(grafo.direcionado)
    for vertice in grafo.vertices:
        grafo_transposto.adicionar_vertice(vertice.rotulo, vertice.peso)
    for aresta in grafo.arestas:
        grafo_transposto.adicionar_aresta(
            aresta.rotulo, aresta.peso,
            grafo_transposto.vertices[grafo.vertices.index(aresta.vertices[1])],
            grafo_transposto.vertices[grafo.vertices.index(aresta.vertices[0])]
        )

    # 3º Passo: Fazer DFS no grafo transposto na ordem decrescente de tempos de término
    componentes = []
    visitados.clear()

    def dfs2(vertice, componente):
        visitados.add(vertice.rotulo)
        componente.append(vertice)
        for aresta in vertice.arestas:
            if aresta.vertices[0] == vertice:
                prox_vertice = aresta.vertices[1]
                if prox_vertice.rotulo not in visitados:
                    dfs2(prox_vertice, componente)

    while tempos_termino:
        vertice = tempos_termino.pop()
        if vertice.rotulo not in visitados:
            componente = []
            dfs2(grafo_transposto.vertices[grafo.vertices.index(vertice)], componente)
            componentes.append(componente)

    return componentes
