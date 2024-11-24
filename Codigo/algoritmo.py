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

def fleury(grafo):
    """
    Implementação do algoritmo de Fleury para encontrar um caminho euleriano.
    """
    if not grafo._verificar_conectividade_simples():
        return "O grafo não é conexo! Não é possível encontrar um caminho euleriano."

    vertices_grau_impar = [v for v in grafo.vertices if len(v.arestas) % 2 != 0]
    if len(vertices_grau_impar) > 2:
        return "O grafo possui mais de 2 vértices de grau ímpar. Não é euleriano."

    # Criar uma cópia do grafo para manipulação
    ciclo = []

    # Iniciar com um vértice de grau ímpar ou qualquer outro vértice
    vertice_atual = grafo.vertices[
        grafo.vertices.index(vertices_grau_impar[0] if vertices_grau_impar else grafo.vertices[0])
    ]

    while len(grafo.arestas) > 0:
        arestas_validas = []

        for idx, aresta in enumerate(vertice_atual.arestas):
            if not e_ponte(grafo, aresta):
                arestas_validas.append((idx, aresta))

        # Se nenhuma aresta válida, escolher qualquer uma
        if len(arestas_validas) == 0:
            idx = 0
        else:
            # Preferir arestas que não sejam pontes
            idx = arestas_validas[0][0]

        aresta_escolhida = vertice_atual.arestas[idx]
        ciclo.append(aresta_escolhida.rotulo)

        # Atualizar o vértice atual para o próximo
        vertice_atual = (
            aresta_escolhida.vertices[1]
            if aresta_escolhida.vertices[0] == vertice_atual
            else aresta_escolhida.vertices[0]
        )

        # Remover a aresta do grafo auxiliar
        grafo.remover_aresta(aresta_escolhida)

    return ciclo

def e_ponte(grafo, aresta):
    """
    Verifica se uma aresta é uma ponte (se sua remoção desconecta o grafo).
    Parâmetros:
        grafo: Instância de Grafo.
        aresta: Instância de Aresta.
    Retorno:
        True se for ponte, False caso contrário.
    """
    # Encontrar o índice da aresta no grafo
    idx = grafo.arestas.index(aresta)

    # Remover a aresta temporariamente usando o índice
    aresta_removida = grafo.arestas[idx]
    origem, destino = aresta_removida.vertices
    grafo.remover_aresta(aresta_removida)

    # Verificar conectividade do grafo após a remoção
    print(grafo.direcionado)
    conexo_apos_remocao = grafo._simplismente_conexo(grafo.direcionado)

    # Restaurar a aresta removida
    grafo.adicionar_aresta(aresta.rotulo, aresta.peso, origem, destino)

    # Retornar True se a remoção desconectou o grafo
    resultado = not conexo_apos_remocao
    return resultado



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

def fleury_com_tarjan(grafo):
    """
    Implementação do algoritmo de Fleury usando Tarjan para detectar pontes.
    :param grafo: Instância de Grafo.
    :return: Lista com o caminho Euleriano ou mensagem de erro.
    """
    if not grafo._verificar_conectividade_simples():
        return "O grafo não é conexo! Não é possível encontrar um caminho Euleriano."

    vertices_grau_impar = [v for v in grafo.vertices if len(v.arestas) % 2 != 0]
    if len(vertices_grau_impar) > 2:
        return "O grafo possui mais de 2 vértices de grau ímpar. Não é euleriano."

    # Criar uma cópia do grafo para manipulação
    ciclo = []

    # Iniciar com um vértice de grau ímpar ou qualquer outro vértice
    vertice_atual = grafo.vertices[
        grafo.vertices.index(vertices_grau_impar[0] if vertices_grau_impar else grafo.vertices[0])
    ]

    while len(grafo.arestas) > 0:
        pontes = encontrar_pontes_tarjan(grafo)
        arestas_validas = [
            aresta
            for aresta in vertice_atual.arestas
            if (aresta.vertices[0].rotulo, aresta.vertices[1].rotulo) not in pontes and
               (aresta.vertices[1].rotulo, aresta.vertices[0].rotulo) not in pontes
        ]

        # Se não houver arestas não-pontes, escolher qualquer uma
        if len(arestas_validas) == 0:
            aresta_escolhida = vertice_atual.arestas[0]
        else:
            aresta_escolhida = arestas_validas[0]

        # Adicionar a aresta ao ciclo e remover do grafo
        ciclo.append(aresta_escolhida.rotulo)
        grafo.remover_aresta(aresta_escolhida)

        # Atualizar o vértice atual para o próximo
        vertice_atual = (
            aresta_escolhida.vertices[1]
            if aresta_escolhida.vertices[0] == vertice_atual
            else aresta_escolhida.vertices[0]
        )

    return ciclo

