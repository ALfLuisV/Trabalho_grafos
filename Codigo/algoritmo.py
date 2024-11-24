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

def encontrar_pontes_tarjan(grafo):
    """
    Encontra todas as pontes em um grafo usando o algoritmo de Tarjan.
    :param grafo: Instância de Grafo.
    :return: Lista de tuplas representando as pontes (v1, v2).
    """
    tempo = [0]
    ids = {}
    lows = {}
    visitados = set()
    pontes = []

    def dfs(vertice, parent=None):
        """
        Função auxiliar para realizar DFS e encontrar pontes.
        :param vertice: Vértice atual.
        :param parent: Vértice pai na árvore DFS.
        """
        visitados.add(vertice)
        ids[vertice] = lows[vertice] = tempo[0]
        tempo[0] += 1

        for aresta in vertice.arestas:
            vizinho = aresta.vertices[1] if aresta.vertices[0] == vertice else aresta.vertices[0]
            if vizinho == parent:
                continue
            if vizinho not in visitados:
                dfs(vizinho, vertice)
                lows[vertice] = min(lows[vertice], lows[vizinho])

                if lows[vizinho] > ids[vertice]:
                    pontes.append((vertice.rotulo, vizinho.rotulo))
            else:
                lows[vertice] = min(lows[vertice], ids[vizinho])

    for vertice in grafo.vertices:
        if vertice not in visitados:
            dfs(vertice)

    return pontes
