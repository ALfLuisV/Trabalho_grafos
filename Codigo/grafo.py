# grafo.py
import random
from vertice import Vertice
from aresta import Aresta
from aresta import listar_arestas


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

    def checar_articulacoes(self):
        """Encontra e retorna os pontos de articulação do grafo."""
        def buscaProfundidade(v, visited):
            """Realiza uma busca em profundidade a partir do vértice v."""
            visited.add(v)
            for u in self.obter_vizinhos(v):
                if u not in visited:
                    # chamada recursiva a partir do vizinho não visitado
                    buscaProfundidade(u, visited)

        def contar_componentes():
            """Conta o número de componentes conectados no grafo."""
            visited = set()
            componentes = 0
            for vertice in self.vertices:
                if vertice.rotulo not in visited:  # se o vértice não foi visitado
                    # chamada recursiva a partir de algum vertice não visitado
                    buscaProfundidade(vertice.rotulo, visited)
                    componentes += 1
            return componentes

        articulacoes = []
        componentes_iniciais = contar_componentes()

        # Usa uma cópia da lista para evitar problemas de iteração
        for vertice in self.vertices[:]:
            rotulo = vertice.rotulo  # Salva o rótulo do vértice
            # Remove o vértice para verificar se é uma articulação
            self.vertices.remove(vertice)
            # Conta os componentes após a remoção
            componentes_apos_remocao = contar_componentes()
            self.vertices.append(vertice)  # Restaura o vértice removido
            # Se o número de componentes aumentou, é uma articulação
            if componentes_apos_remocao > componentes_iniciais:
                # Adiciona o vértice à lista de articulações
                articulacoes.append(rotulo)

        if not articulacoes:
            return "O grafo não possui pontos de articulação"
        return f"O grafo possui pontos de articulação: {', '.join(articulacoes)}"

    def obter_vizinhos(self, vertice_rotulo):
        """Retorna os vizinhos de um vértice dado seu rótulo."""
        vizinhos = set()
        for aresta in self.arestas:
            if aresta.vertices[0].rotulo == vertice_rotulo:
                vizinhos.add(aresta.vertices[1].rotulo)
            elif aresta.vertices[1].rotulo == vertice_rotulo:
                vizinhos.add(aresta.vertices[0].rotulo)
        return vizinhos

    def exibir_matriz_adjacenciaND(self):
        """Monta a matriz de adjacencia para grafos não direcionados"""
        matrizAdj = []
        print("vertices::::")
        for v in self.arestas:
            print("Vertice inicial::::")
            print(v.vertices[0])
            print("Vertice final::::")
            print(v.vertices[1])

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

    def exibir_matriz_adjacenciaD(self):
        """Monta a matriz de adjacencia para grafos  direcionados"""
        matrizAdj = []

        for vertice1 in self.vertices:
            linha = []
            for vertice2 in self.vertices:
                if vertice1 == vertice2:
                    linha.append(0)
                    continue
                found = False
                for aresta in self.arestas:
                    if (aresta.vertices[0] == vertice1 and aresta.vertices[1] == vertice2):
                        found = True
                        break
                if found:
                    linha.append(1)
                else:
                    linha.append(0)
            matrizAdj.append(linha)
        return matrizAdj

    def exibir_matriz_incidenciaND(self):
        """Monta a matriz de incidencia de um grafo não direcionado"""
        matrizInc = []

        for vertice in self.vertices:
            linha = []
            for aresta in self.arestas:
                found = False
                if (vertice in (aresta.vertices[0], aresta.vertices[1])):
                    found = True
                if found:
                    linha.append(1)
                else:
                    linha.append(0)
            matrizInc.append(linha)
        return matrizInc

    def exibir_matriz_incidenciaD(self):
        """Monta a matriz de incidencia de um grafo direcionado"""
        matrizInc = []

        for vertice in self.vertices:
            linha = []
            for aresta in self.arestas:
                found = 0

                if (aresta.vertices[0] == vertice):
                    found = -1
                elif (aresta.vertices[1] == vertice):
                    found = 1

                linha.append(found)
            matrizInc.append(linha)

        return matrizInc

    def _simplismente_conexo(self, direcionado):
        vetorAlc = []

        verticeRef = self.vertices[0]

        for aresta in self.arestas:
            if (aresta.vertices[0] == verticeRef):
                if (aresta.vertices[1] in vetorAlc):
                    continue
                vetorAlc.append(aresta.vertices[1])

        i = 0

        while i < len(vetorAlc):
            # Pega o vértice atual de `vetorAlc` para processar
            verticeRef2 = vetorAlc[i]

            # Itera sobre as arestas para verificar conexões
            for aresta in self.arestas:
                if aresta.vertices[0] == verticeRef2:
                    if aresta.vertices[1] not in vetorAlc:
                        # Adiciona o vértice conectado a `vetorAlc`
                        vetorAlc.append(aresta.vertices[1])

            i += 1  # Incrementa o índice para o próximo vértice a ser processado

        vetorAlc.append(verticeRef)

        conexo = True
        for vertice in self.vertices:
            if vertice not in vetorAlc:
                conexo = False
                break

        if conexo:
            if direcionado is True:
                return "O grafo é simplismente conexo!"
           
            return "O grafo é conexo!"

        return "O grafo não é conexo!"

    def verificar_conectividade(self):
        """Verifica o tipo de conectividade do grafo."""
        if not self.vertices:
            return "O grafo está vazio!"

        if self.direcionado:
            if self._fortemente_conexo():
                return "O grafo é fortemente conexo!"
            elif self._semi_fortemente_conexo():
                return "O grafo é semi-fortemente conexo!"
            else:
                return "O grafo não é conexo!"
        else:
            return self._simplismente_conexo(self.direcionado)

    def verificar_conectividade_naive(self):
        """
        Permite ao usuário escolher uma aresta para remover e verifica a conectividade do grafo após a remoção.
        """
        while True:
            print("\nArestas disponíveis para remover:")
            listar_arestas(self.arestas)

            escolha = input(
                "\nDigite o índice da aresta que deseja remover (ou 'sair' para finalizar): ").strip()

            if escolha.lower() == "sair":
                print("Encerrando verificação interativa.")
                break

            if not escolha.isdigit():
                print("Entrada inválida. Digite um índice numérico ou 'sair'.")
                continue

            escolha = int(escolha)

            if escolha < 0 or escolha >= len(self.arestas):
                print("Índice fora do intervalo. Tente novamente.")
                continue

            # Selecionar a aresta escolhida
            aresta_escolhida = self.arestas[escolha]

            # Remover a aresta temporariamente
            self.remover_aresta(aresta_escolhida)

            # Verificar conectividade
            conectividade = self.verificar_conectividade()

            # Mostrar resultado ao usuário
            print(f"\nAresta removida: {aresta_escolhida.rotulo}")
            print(f"Conectividade do grafo: {conectividade}")

            # Perguntar se o usuário deseja restaurar a aresta
            restaurar = input(
                "Deseja restaurar a aresta removida? (s/n): ").strip().lower()
            if restaurar == "s":
                self.adicionar_aresta(
                    aresta_escolhida.rotulo,
                    aresta_escolhida.peso,
                    aresta_escolhida.vertices[0],
                    aresta_escolhida.vertices[1]
                )
                print("Aresta restaurada.")

    def _fortemente_conexo(self):
        """Verifica se o grafo direcionado é fortemente conexo."""
        for vertice in self.vertices:
            if not self._dfs_direcionado(vertice):
                return False
        return True

    def _semi_fortemente_conexo(self):
        """Verifica se o grafo é semi-fortemente conexo."""
        grafo_und = self._converter_nao_direcionado()
        return grafo_und._verificar_conectividade_simples()

    def _dfs_direcionado(self, start):
        """Realiza DFS em um grafo direcionado a partir de um vértice."""
        visitados = set()
        self._dfs_visit(start, visitados)
        return len(visitados) == len(self.vertices)

    def _dfs_visit(self, vertice, visitados):
        """Auxiliar para realizar DFS."""
        visitados.add(vertice)
        for aresta in vertice.arestas:
            vizinho = aresta.vertices[1] if aresta.vertices[0] == vertice else aresta.vertices[0]
            if self.direcionado and aresta.vertices[0] != vertice:
                continue
            if vizinho not in visitados:
                self._dfs_visit(vizinho, visitados)

    def _converter_nao_direcionado(self):
        """Converte o grafo direcionado em não direcionado."""
        grafo_nd = Grafo(direcionado=False)
        grafo_nd.vertices = self.vertices
        for aresta in self.arestas:
            grafo_nd.arestas.append(aresta)
        return grafo_nd

    def _verificar_conectividade_simples(self):
        """Verifica se um grafo não direcionado é simplesmente conexo."""
        visitados = set()
        self._dfs_visit(self.vertices[0], visitados)
        return len(visitados) == len(self.vertices)

    def criarGrafo(self):
        direcionado = input(
            "O grafo será direcionado? (s/n): ").strip().lower() == 's'
        num_vertices = int(input("Digite o número de vértices: "))
        pesos_aleatorios = input(
            "Os pesos das arestas e vértices serão aleatórios? (s/n) n = todos os pesos = 0: ").strip().lower() == 's'
        grafo = Grafo(direcionado=direcionado)

        # Adicionar vértices
        vertices = [Vertice(f'V{i}', random.randint(
            1, 10) if pesos_aleatorios else 0) for i in range(num_vertices)]
        for vertice in vertices:
            grafo.adicionar_vertice(vertice.rotulo, vertice.peso)

        # Adicionar arestas aleatórias
        num_arestas = random.randint(
            num_vertices, num_vertices * (num_vertices - 1) // 2)
        arestas_existentes = set()
        for i in range(num_arestas):
            while True:
                vertice1, vertice2 = random.sample(vertices, 2)

                # Verificar se a aresta é um loop
                if vertice1 == vertice2:
                    continue

                if direcionado:
                    aresta_id = (vertice1.rotulo, vertice2.rotulo)
                    aresta_id_reversa = (vertice2.rotulo, vertice1.rotulo)
                else:
                    aresta_id = tuple(
                        sorted([vertice1.rotulo, vertice2.rotulo]))
                    aresta_id_reversa = aresta_id

                # Verificar se a aresta já existe ou se é antiparalela
                if aresta_id not in arestas_existentes and aresta_id_reversa not in arestas_existentes:
                    arestas_existentes.add(aresta_id)
                    break

            rotulo = f'A{i}'
            peso = random.randint(1, 10) if pesos_aleatorios else 0
            grafo.adicionar_aresta(rotulo, peso, vertice1, vertice2)

        print(grafo.arestas)
        return grafo

    def gerar_csv(self, nome_arquivo, direcionado):

        """Gera um arquivo CSV com a matriz de incidência do grafo."""
        if direcionado is False:
            try:
                nome_arquivo = nome_arquivo + ".csv"

                print(self.exibir_matriz_incidenciaND())

                file = open(nome_arquivo, "w", encoding="utf-8")
                file.write(";")
                for i, vertice in enumerate(self.vertices):
                    if i == len(self.vertices) - 1:  # Último elemento
                        file.write(vertice.rotulo)
                    else:
                        file.write(vertice.rotulo + ";")
                
                file.write("\n")

                matriz_adj = self.exibir_matriz_adjacenciaND()

                for i, vertice in enumerate(self.vertices):
                    file.write(vertice.rotulo + ";")

                    for j, value in enumerate(matriz_adj[i]):

                        if j == len(matriz_adj[i]) - 1:  # Último elemento
                            file.write(str(value))
                        else:
                            file.write(str(value) + ";")

                    file.write("\n")

                print("Grafo exportado com sucesso!")
            except Exception as e:
                print(f"Ocorreu um erro na exportação do grafo: {e}")
        else :
            try:
                nome_arquivo = nome_arquivo + ".csv"

                print(self.exibir_matriz_incidenciaND())

                file = open(nome_arquivo, "w", encoding="utf-8")
                file.write(";")
                for i, vertice in enumerate(self.vertices):
                    if i == len(self.vertices) - 1:  # Último elemento
                        file.write(vertice.rotulo)
                    else:
                        file.write(vertice.rotulo + ";")
                
                file.write("\n")

                matriz_adj = self.exibir_matriz_adjacenciaD() 

                for i, vertice in enumerate(self.vertices):
                    file.write(vertice.rotulo + ";")

                    for j, value in enumerate(matriz_adj[i]):

                        if j == len(matriz_adj[i]) - 1:  # Último elemento
                            file.write(str(value))
                        else:
                            file.write(str(value) + ";")

                    file.write("\n")

                print("Grafo exportado com sucesso!")
            except Exception as e:
                print(f"Ocorreu um erro na exportação do grafo: {e}")
    
    def ler_grafo_from_csv(self, nomeCsv):
        print("Iniciando a leitura")
        try:
            file = open(nomeCsv, 'r', encoding="utf-8") #abre o arquivo em modo de leitura

            array_de_vertices = []
            array_de_arestas=[]
            for counter, line in enumerate(file):
                if counter == 0:
                    new_line = line[1:]  # remove the first character of the string which is a ";"
                    new_line1 = new_line[:-1]  # remove the last character of the string which is "\n"
                    array_de_vertices = new_line1.split(";")  # split and create a new array with vertex labels

                          # print(array_de_vertices)
            
                    for v in array_de_vertices:
                        self.adicionar_vertice(v)
                else:
                    new_line = line[3:]  # remove the first character of the string which is a ";"
                    new_line1 = new_line[:-1]  # remove the last character of the string which is "\n"
                    array_arestas = new_line1.split(";")  # split and create a new array with edge labels
                    array_de_arestas.append(array_arestas)        

            counter = 0
            for k, vertice1 in enumerate(array_de_vertices):
                for j, vertice2 in enumerate(array_de_vertices):
                    if k == j or array_de_arestas[k][j] == '0':
                        continue
                    rotulo = "A"+str(counter)
                    self.adicionar_aresta(rotulo, 0, self.vertices[k], self.vertices[j])
                    counter += 1         

            print("Grafo carregado com sucesso!!!")
        except Exception as e:
                print(f"Ocorreu um erro na exportação do grafo: {e}")
        
        
            





                

