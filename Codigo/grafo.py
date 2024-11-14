# grafo.py
from vertice import Vertice
from aresta import Aresta


class Grafo:
    def __init__(self, direcionado: bool):
        self.vertices = []        # Lista de vértices no grafo
        self.arestas = []         # Lista de arestas no grafo
        self.direcionado = direcionado  # Determina se o grafo é direcionado

    def adicionar_vertice(self, rotulo: str, peso: int = 0):
        """Adiciona um vértice ao grafo."""
        vertice = Vertice(rotulo, peso)
        self.vertices.append(vertice)
        return vertice

    def adicionar_aresta(self, rotulo: str, peso: int, vertice1: Vertice, vertice2: Vertice):
        """Adiciona uma aresta ao grafo conectando dois vértices."""
        aresta = Aresta(rotulo, peso, vertice1, vertice2)
        self.arestas.append(aresta)
        vertice1.adicionar_aresta(aresta)
        vertice2.adicionar_aresta(aresta)
        return aresta

    def remover_vertice(self, vertice: Vertice):
        """Remove um vértice e todas as arestas associadas a ele."""
        if vertice in self.vertices:
            # Usando list() para evitar mutação durante a iteração
            for aresta in list(vertice.arestas):
                self.remover_aresta(aresta)
            self.vertices.remove(vertice)

    def remover_aresta(self, aresta: Aresta):
        """Remove uma aresta do grafo e desconecta os vértices."""
        if aresta in self.arestas:
            self.arestas.remove(aresta)
            aresta.vertices[0].arestas.remove(aresta)
            aresta.vertices[1].arestas.remove(aresta)

    def checar_adjacencia_vertices(self, vertice1: Vertice, vertice2: Vertice) -> bool:
        """Verifica se dois vértices são adjacentes (conectados por uma aresta)."""
        return any(
            aresta for aresta in self.arestas if (
                aresta.vertices == (vertice1, vertice2) or
                (not self.direcionado and aresta.vertices == (vertice2, vertice1))
            )
        )

    def checar_adjacencia_arestas(self, aresta1: Aresta, aresta2: Aresta) -> bool:
        """Verifica se duas arestas são adjacentes (compartilham um vértice)."""
        return bool(set(aresta1.vertices) & set(aresta2.vertices))

    def alterar_vertice(self, vertice: Vertice, novo_rotulo: str, novo_peso: int):
        """Altera o rótulo e peso de um vértice existente."""
        vertice.rotulo = novo_rotulo
        vertice.peso = novo_peso

    def alterar_aresta(self, aresta: Aresta, novo_rotulo: str, novo_peso: int):
        """Altera o rótulo e peso de uma aresta existente."""
        aresta.rotulo = novo_rotulo
        aresta.peso = novo_peso

    def __str__(self):
        """Retorna uma representação textual do grafo, incluindo vértices e arestas."""
        vertices_str = ", ".join([v.rotulo for v in self.vertices])
        arestas_str = "\n".join([str(a) for a in self.arestas])
        return f"Grafo (Direcionado: {self.direcionado}):\nVertices: {vertices_str}\nArestas:\n{arestas_str}"

    def checar_arestas(self):
        """Metodo que checa a existencia de arestas em um grafo"""
        if len(self.arestas) == 0:
            return "O grafo não possui arestas"

        return self.arestas

    def verificar_arestas(self):
        """Retorna a quantidade de arestas e vértices no grafo."""
        return "O grafo possui " + str(len(self.arestas)) + " arestas, e " + str(len(self.vertices)) + " vertices"

    def checar_grafo(self):
        """Verifica se o grafo é vazio ou se ele é completo."""
        if len(self.vertices) == 0:
            return "Este grafo está vazio!"

        # Verifica se cada vértice está conectado a todos os outros vértices
        for vertice in self.vertices:
            conexoes = {aresta.vertices[1] for aresta in self.arestas if aresta.vertices[0] == vertice} | \
                {aresta.vertices[0]
                    for aresta in self.arestas if aresta.vertices[1] == vertice}

            if len(conexoes) != len(self.vertices) - 1:
                return "O grafo não é completo!"

        return "O grafo é completo!"

    def exibir_matriz_adjacenciaND(self):
        """Monta a matriz de adjacencia para grafos não direcionados"""
        matrizAdj = []

        for vertice1 in self.vertices:
            linha = []
            for vertice2 in self.vertices:
                if vertice1 == vertice2:
                    linha.append(0)
                    continue
                found = False
                for aresta in self.arestas:
                    if (aresta.vertices[0] == vertice1 and aresta.vertices[1] == vertice2) or (aresta.vertices[1] == vertice1 and aresta.vertices[0] == vertice2):
                        found = True
                        break
                if found:
                    linha.append(1)
                else:
                    linha.append(0)
            matrizAdj.append(linha)
        return matrizAdj
