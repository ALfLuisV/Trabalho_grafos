from grafo import Grafo
from vertice import Vertice
from aresta import Aresta

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
    Verifica se o grafo é euleriano e retorna o ciclo euleriano se possível.
    Parâmetros:
        grafo: Instância de Grafo.
    Retorno:
        Lista representando o ciclo euleriano ou mensagem de erro.
    """
    if not grafo._verificar_conectividade_simples():
        return "O grafo não é conexo! Não é possível encontrar um ciclo euleriano."

    vertices_grau_impar = [v for v in grafo.vertices if len(v.arestas) % 2 != 0]
    if len(vertices_grau_impar) > 2:
        return "O grafo possui mais de 2 vértices de grau ímpar. Não é euleriano."

    arestas_restantes = list(set(grafo.arestas))  # Remover duplicatas
    ciclo_euleriano = []

    vertice_atual = vertices_grau_impar[0] if vertices_grau_impar else grafo.vertices[0]

    while arestas_restantes:
        aresta = None

        # Priorizar arestas que não são pontes
        for a in vertice_atual.arestas:
            if a in arestas_restantes and not e_ponte(grafo, a):
                aresta = a
                break

        # Se todas as arestas restantes forem pontes, selecionar uma
        if not aresta:
            for a in vertice_atual.arestas:
                if a in arestas_restantes:
                    aresta = a
                    break

        if not aresta:
            return "Erro: Não foi possível continuar o ciclo Euleriano. Verifique o grafo."

        # Adicionar a aresta ao ciclo e remover das arestas restantes
        print(f"Removendo aresta: {aresta}")
        ciclo_euleriano.append(aresta)
        arestas_restantes.remove(aresta)

        # Caminhar para o próximo vértice
        vertice_atual = aresta.vertices[1] if aresta.vertices[0] == vertice_atual else aresta.vertices[0]
        print(f"Movendo para {vertice_atual.rotulo}")

    return ciclo_euleriano


def e_ponte(grafo, aresta):
    """
    Verifica se uma aresta é uma ponte (se sua remoção desconecta o grafo).
    Parâmetros:
        grafo: Instância de Grafo.
        aresta: Instância de Aresta.
    Retorno:
        True se for ponte, False caso contrário.
    """
    # Remover temporariamente a aresta
    grafo.remover_aresta(aresta)
    conexo_apos_remocao = grafo._simplismente_conexo()
    print(conexo_apos_remocao)
    # Restaurar a aresta
    grafo.adicionar_aresta(aresta.rotulo, aresta.peso, aresta.vertices[0], aresta.vertices[1])
    return not conexo_apos_remocao

