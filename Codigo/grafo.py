# grafo.py
import random
import time
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
        """Metodo que checa a existencia de arestas em um grafo, se não existir, através da informação do tamanho do 
        array de arestas, ou ele retorna o conteudo do array (se for >=1), ou retorna a mensagem "o grafo não possui arestas" """
        if len(self.arestas) == 0:
            return "O grafo não possui arestas"

        return self.arestas

    def verificar_arestas(self):
        """Retorna a quantidade de arestas e vértices no grafo."""
        return "O grafo possui " + str(len(self.arestas)) + " arestas, e " + str(len(self.vertices)) + " vertices"


#     O método `checar_grafo` verifica se um grafo é vazio ou completo. Primeiro, verifica se a 
# lista de vértices (`self.vertices`) está vazia. Caso esteja, retorna que o grafo está vazio. Caso contrário, 
# percorre cada vértice do grafo e calcula suas conexões utilizando as arestas. Para isso, considera os vértices 
# conectados tanto como origem quanto como destino das arestas.
# Se o número de conexões de um vértice for diferente do total de vértices menos um 
# (ou seja, se ele não está conectado a todos os outros vértices), o método conclui que o grafo não é 
# completo e retorna essa mensagem. Caso todos os vértices estejam adequadamente conectados, o método 
# retorna que o grafo é completo.
# Essa abordagem permite verificar rapidamente a completude ou o vazio do grafo, garantindo que as relações 
# entre os vértices sejam analisadas corretamente.
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
            # Remove o vértice e suas arestas associadas para verificar se é uma articulação
            self.vertices.remove(vertice)
            arestas_removidas = [aresta for aresta in self.arestas if vertice in aresta.vertices]
            for aresta in arestas_removidas:
                self.arestas.remove(aresta)

            # Conta os componentes após a remoção
            componentes_apos_remocao = contar_componentes()

            # Restaura o vértice e suas arestas
            self.vertices.append(vertice)
            self.arestas.extend(arestas_removidas)

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


# O método `exibir_matriz_adjacenciaND` constrói e retorna a matriz de adjacência de um grafo não direcionado. 
# Nessa matriz, cada linha e coluna representam vértices, e o valor `1` indica que há uma aresta conectando os 
# dois vértices, enquanto `0` indica ausência de conexão.
# O método inicia criando uma lista vazia chamada `matrizAdj` para armazenar as linhas da matriz. Para 
# cada par de vértices (`vertice1` e `vertice2`), verifica-se se existe uma conexão entre eles. Se os vértices 
# forem iguais, o valor `0` é adicionado para evitar loops. Caso contrário, o método percorre as arestas do grafo
#  para verificar se há uma conexão direta entre os dois vértices, considerando ambas as direções (de `vertice1` 
# para `vertice2` ou vice-versa). Se uma conexão é encontrada, o valor `1` é adicionado à linha; caso contrário, 
# adiciona-se `0`.
# Após processar todas as conexões para um vértice, a linha é adicionada à matriz. No final, a matriz completa 
# é retornada, representando as conexões entre os vértices de forma simétrica, característica de grafos não 
# direcionados.
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
    

# O método `exibir_matriz_adjacenciaD` constrói e retorna a matriz de adjacência de um grafo direcionado. 
# Nesta matriz, cada linha e coluna representam vértices, e o valor `1` indica que há uma aresta direcionada 
# do vértice da linha para o vértice da coluna, enquanto `0` indica ausência de conexão.
# O método começa criando uma lista vazia chamada `matrizAdj` para armazenar as linhas da matriz. Para 
# cada par de vértices (`vertice1` e `vertice2`), verifica-se se existe uma aresta que conecta `vertice1` 
# a `vertice2`. Se os vértices forem iguais, o valor `0` é adicionado para evitar loops. Caso contrário, um 
# laço percorre as arestas do grafo para verificar a existência de uma conexão. Se encontrada, o valor `1` é 
# adicionado à linha; caso contrário, adiciona-se `0`. Após processar todas as colunas para um vértice, a linha 
# completa é adicionada à matriz.
# Por fim, o método retorna a matriz de adjacência, que fornece uma representação clara das conexões
#  direcionadas no grafo, indicando de forma precisa quais vértices estão conectados e a direção das conexões.
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


# O método `exibir_matriz_incidenciaND` constrói e retorna a matriz de incidência de um grafo não direcionado. 
# Nessa matriz, cada linha representa um vértice, e cada coluna representa uma aresta. Os valores indicam a 
# relação entre vértices e arestas: `1` se o vértice está conectado à aresta e `0` caso contrário.
# O método inicia criando uma lista vazia chamada `matrizInc`, que armazenará as linhas da matriz. Para cada 
# vértice no grafo, ele cria uma nova linha (`linha`) e itera sobre todas as arestas. Durante essa iteração, 
# verifica se o vértice atual é um dos dois extremos da aresta (origem ou destino). Se for, adiciona `1` à linha, 
# caso contrário, adiciona `0`. Após processar todas as arestas para o vértice atual, a linha completa é adicionada 
# à matriz. Quando todos os vértices são processados, a matriz de incidência completa é retornada. Essa matriz 
# fornece uma representação clara das conexões entre vértices e arestas em grafos não direcionados, identificando 
# de forma simples quais vértices estão conectados por cada aresta.
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
    

# O método `exibir_matriz_incidenciaD` cria e retorna a matriz de incidência de um grafo direcionado, 
# onde cada linha da matriz representa um vértice, e cada coluna representa uma aresta. Os valores na 
# matriz indicam a relação entre vértices e arestas: `-1` quando a aresta sai de um vértice, `1` quando a a
# resta entra em um vértice, e `0` quando a aresta não está conectada ao vértice.
# O método começa inicializando uma lista vazia chamada `matrizInc`, que armazenará as linhas da matriz. 
# Em seguida, ele itera sobre todos os vértices do grafo (`self.vertices`). Para cada vértice, uma nova linha 
# (`linha`) é criada para representar a conexão desse vértice com todas as arestas. O método então percorre 
# todas as arestas do grafo (`self.arestas`) e verifica a relação entre o vértice atual e cada aresta. Se a 
# aresta tem o vértice atual como origem (`aresta.vertices[0] == vertice`), o valor `-1` é adicionado à linha. 
# Se o vértice é o destino da aresta (`aresta.vertices[1] == vertice`), o valor `1` é adicionado. Caso o vértice 
# não esteja conectado à aresta, o valor `0` é adicionado.
# Depois de processar todas as arestas para o vértice atual, a linha completa é adicionada à matriz de 
# incidência. Quando todos os vértices são processados, e suas respectivas linhas são adicionadas, a matriz de 
# incidência completa é retornada pelo método. Essa matriz fornece uma representação tabular clara do grafo 
# direcionado, permitindo identificar as conexões entre vértices e arestas de forma precisa e eficiente.
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
    

# O método `_simplismente_conexo` verifica se um grafo é conexo ou simplesmente conexo, 
# dependendo se ele é direcionado. Ele inicia escolhendo o primeiro vértice (`verticeRef`) 
# como ponto de partida e cria uma lista (`vetorAlc`) para armazenar os vértices alcançáveis. 
# Primeiramente, adiciona ao `vetorAlc` os vértices diretamente conectados a `verticeRef` por meio das arestas.
# Depois, em um loop `while`, verifica todas as conexões indiretas: para cada vértice já presente em `vetorAlc`, 
# explora as arestas que partem dele e adiciona à lista os vértices conectados que ainda não foram processados. 
# Isso continua até que todos os vértices acessíveis tenham sido analisados.
# No final, o método verifica se todos os vértices do grafo estão presentes em `vetorAlc`. Se estiverem, 
# retorna que o grafo é "conexo" ou "simplesmente conexo", dependendo se é direcionado ou não. Caso contrário, 
# indica que o grafo não é conexo. Esse método é eficiente ao explorar conexões diretas e indiretas para 
# determinar a conectividade do grafo.
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

# O metodo `verificar_conectividade` verifica o tipo de conectividade do grafo. Se o grafo for direcionado,
# ele chama os métodos `_fortemente_conexo` e `_semi_fortemente_conexo` para verificar se o grafo é fortemente conexo ou semi-fortemente conexo, respectivamente.
# Se o grafo for não direcionado, ele chama o método `_simplismente_conexo` para verificar se o grafo é simplesmente conexo.
#caso contrario, retorna a mensagem "O grafo não é conexo".
# O método `_fortemente_conexo` percorre todos os vértices do grafo a partir de uma busca por profundidade e verifica se é possível alcançar todos os outros vértices a partir de cada vértice. Se algum vértice não for alcançável, o método retorna `False`, indicando que o grafo não é fortemente conexo. Caso contrário, retorna `True`.
# O método `_semi_fortemente_conexo` converte o grafo direcionado em um grafo não direcionado e chama o método `_verificar_conectividade_simples` para verificar se o grafo possui exatamente dois vértices de grau ímpar. Se a condição for atendida, o método retorna `True`, indicando que o grafo é semi-fortemente conexo. Caso contrário, retorna `False`.

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

# O método `verificar_conectividade_naive` verifica a conectividade de um grafo apos a remoção de uma aresta.
# Lista todas as arestas disponiveis utilizando o metodo 'listar_arestas' e solicita ao usuário que escolha uma aresta para remover temporariamente.
# Ele armazena a aresta removida temporariamente, verifica a conectividade do grafo chamando o metodo 'verificar_conectividade' e exibe o resultado.
# Em seguida, pergunta se o usuário deseja restaurar a aresta removida. Se a resposta for afirmativa, a aresta é restaurada, caso contrario, a aresta é removida permanentemente do grafo.

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
        """
        Realiza DFS iterativa a partir de um vértice.
        """
        pilha = [vertice]
        while pilha:
            atual = pilha.pop()
            if atual not in visitados:
                visitados.add(atual)
                # Adicionar vizinhos à pilha
                for aresta in atual.arestas:
                    vizinho = aresta.vertices[1] if aresta.vertices[0] == atual else aresta.vertices[0]
                    if vizinho not in visitados:
                        pilha.append(vizinho)


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
        
        start_time = time.perf_counter()
        
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
            
            end_time = time.perf_counter()
            
            tempo_execucao = (end_time - start_time)

        print(grafo.arestas)
        print()
        print(f"Tempo de execução para gerar o grafo: {tempo_execucao:.4f} segundos")
        return grafo



# O método `gerar_csv` cria um arquivo CSV representando a matriz de incidência ou de adjacência de um grafo, 
# dependendo se ele é direcionado ou não. Ele recebe `self` (objeto do grafo), `nome_arquivo` (nome base do arquivo)
#  e `direcionado` (indica se o grafo é direcionado). 
# Se o grafo for **não direcionado**, o nome do arquivo é ajustado com a extensão ".csv". 
# A matriz de incidência é exibida no console e o arquivo é aberto para escrita em UTF-8. 
# A primeira linha do CSV contém os rótulos dos vértices separados por ponto e vírgula. 
# Em seguida, a matriz de adjacência não direcionada é obtida e processada linha a linha: 
# para cada vértice, seu rótulo e os valores das conexões são escritos no arquivo. 
# Após processar a matriz, o arquivo é fechado, e uma mensagem de sucesso é exibida. 
# Em caso de erro, uma mensagem é exibida no console.
# Para **grafos direcionados**, o processo é semelhante, mas utiliza as versões direcionadas da 
# matriz de incidência e de adjacência. O método adapta a escrita conforme o tipo do grafo e exporta os
#  dados no formato CSV, sempre tratando adequadamente rótulos e valores. Ele também informa o sucesso ou 
# erro do processo no console.
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
        else:
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


# O método `ler_grafo_from_csv` tem como objetivo carregar um grafo a partir de um arquivo CSV.
# Ele começa imprimindo uma mensagem indicando o início do processo de leitura. Em seguida,
# tenta abrir o arquivo especificado (`nomeCsv`) no modo de leitura, utilizando a codificação UTF-8 para
# garantir compatibilidade com caracteres especiais. Caso ocorra algum erro durante a leitura,
# a execução será desviada para o bloco `except`, onde uma mensagem de erro será exibida.
# Inicialmente, dois arrays auxiliares são criados: `array_de_vertices` e `array_de_arestas`.
# O primeiro armazenará os vértices do grafo, enquanto o segundo armazenará as arestas.
# O método utiliza um loop `for` com `enumerate` para iterar sobre as linhas do arquivo CSV, onde a
# variável `counter` representa o índice da linha, e `line` contém o conteúdo da linha atual.
# Na primeira iteração (`counter == 0`), a linha correspondente é tratada como a lista de vértices
#  do grafo. O primeiro caractere da linha, geralmente um ponto-e-vírgula, é removido com `line[1:]`, e
# o último caractere (um possível caractere de nova linha) é removido com `line[:-1]`. A linha resultante é
#  dividida em um array de vértices utilizando o método `split(";")`. Esse array é armazenado em
# `array_de_vertices`. Em seguida, cada vértice é adicionado ao grafo utilizando o método `self.adicionar_vertice`.
# Para as linhas subsequentes (`counter > 0`), o método interpreta os dados como a matriz de adjacência do grafo.
# Novamente, os primeiros e últimos caracteres são removidos, e a linha resultante é dividida em um array de
# arestas. Este array é adicionado a `array_de_arestas`, que acumula as informações de adjacência.
# Após carregar os dados de vértices e arestas, o método inicia um processo de construção do grafo
# com base na matriz de adjacência. Ele utiliza dois loops aninhados para iterar sobre cada combinação de
# vértices (`k` e `j`), representados pelos índices de `array_de_vertices`. Se os índices forem iguais (`k == j`)
# ou se o valor correspondente na matriz de adjacência (`array_de_arestas[k][j]`) for `'0'`, a
# iteração atual é ignorada utilizando o comando `continue`. Caso contrário, é criada uma aresta
# entre os dois vértices, utilizando o método `self.adicionar_aresta`. O rótulo da aresta é gerado
# dinamicamente como `"A" + str(counter)`, e um contador é incrementado para garantir que cada aresta
# tenha um rótulo único.
# Por fim, se todo o processo for concluído sem erros, uma mensagem de sucesso é exibida.
# Caso contrário, qualquer exceção capturada será exibida no console, detalhando o erro ocorrido
# durante a exportação do grafo.
    def ler_grafo_from_csv(self, nomeCsv):
        print("Iniciando a leitura")
        try:
            # abre o arquivo em modo de leitura
            file = open(nomeCsv, 'r', encoding="utf-8")

            array_de_vertices = []
            array_de_arestas = []
            for counter, line in enumerate(file):
                if counter == 0:
                    # remove the first character of the string which is a ";"
                    new_line = line[1:]
                    # remove the last character of the string which is "\n"
                    new_line1 = new_line[:-1]
                    # split and create a new array with vertex labels
                    array_de_vertices = new_line1.split(";")

                    # print(array_de_vertices)

                    for v in array_de_vertices:
                        self.adicionar_vertice(v)
                else:
                    # remove the first character of the string which is a ";"
                    new_line = line[3:]
                    # remove the last character of the string which is "\n"
                    new_line1 = new_line[:-1]
                    # split and create a new array with edge labels
                    array_arestas = new_line1.split(";")
                    array_de_arestas.append(array_arestas)

            counter = 0
            for k, vertice1 in enumerate(array_de_vertices):
                for j, vertice2 in enumerate(array_de_vertices):
                    if k == j or array_de_arestas[k][j] == '0':
                        continue
                    rotulo = "A"+str(counter)
                    self.adicionar_aresta(
                        rotulo, 0, self.vertices[k], self.vertices[j])
                    counter += 1

            a = 0
            while a < len(self.arestas):
                aresta1 = self.arestas[a]
                b = a + 1
                while b < len(self.arestas):
                    aresta2 = self.arestas[b]
                    if aresta1.vertices[0] == aresta2.vertices[1] and aresta1.vertices[1] == aresta2.vertices[0]:
                        del self.arestas[b]
                    else:
                        b += 1
                a += 1
        

            print("Grafo carregado com sucesso!!!")
        except Exception as e:
            print(f"Ocorreu um erro na exportação do grafo: {e}")



def encontrar_pontes_naive(self):
    """
    Identifica e retorna as arestas que são pontes no grafo.
    """
    def contar_componentes():
        """
        Conta o número de componentes conectados no grafo.
        """
        visited = set()
        componentes = 0

        def dfs(v):
            visited.add(v)
            for vizinho in self.obter_vizinhos(v.rotulo):
                vizinho_vertice = next(vert for vert in self.vertices if vert.rotulo == vizinho)
                if vizinho_vertice not in visited:
                    dfs(vizinho_vertice)

        for vertice in self.vertices:
            if vertice not in visited:
                componentes += 1
                dfs(vertice)

        return componentes

    # Componentes conectados inicialmente
    componentes_iniciais = contar_componentes()

    pontes = []

    for aresta in self.arestas[:]:
        # Remover a aresta temporariamente
        self.remover_aresta(aresta)

        # Contar componentes conectados após a remoção
        componentes_apos_remocao = contar_componentes()

        # Restaurar a aresta
        self.adicionar_aresta(
            aresta.rotulo, aresta.peso, aresta.vertices[0], aresta.vertices[1]
        )

        # Se o número de componentes aumentou, é uma ponte
        if componentes_apos_remocao > componentes_iniciais:
            pontes.append(aresta.rotulo)

    if not pontes:
        return "O grafo não possui arestas que são pontes."
    return f"As pontes no grafo são: {', '.join(pontes)}"
