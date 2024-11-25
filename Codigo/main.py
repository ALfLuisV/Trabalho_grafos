import json
from grafo import Grafo
from vertice import listar_vertices
from aresta import listar_arestas
from algoritmo import kosaraju
from algoritmo import fleury
from algoritmo import fleury_com_tarjan
import os
import time

from algoritmo import encontrar_pontes_tarjan
from grafo import encontrar_pontes

def mostrar_menu():
    print("\nMenu de Opções:")
    print("0. Carregar grafo a partir de arquivo JSON")
    print("1. Carregar grafo a partir de arquivo CSV")
    print("2. Criar grafo aleatório baseado em seu número de vértices")
    print("3. Adicionar vértice")
    print("4. Adicionar aresta")
    print("5. Exibir grafo")
    print("6. Alterar vértice")
    print("7. Alterar aresta")
    print("8. Deletar vértice")
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
    print("21. Verificar componentes fortemente conectos com Kosaraju")
    print("22. Encontrar pontes (Tarjan)")
    print("23. Exportar CSV")
    print("24. Executar Fleury")
    print("25. Executar Fleury com Tarjan")
    print("26. Sair")
    return input("Escolha uma opção: ")

def criar_vertices_iniciais(grafo):
    try:
        num_vertices = int(input("Quantos vértices deseja criar? "))
        if num_vertices < 1:
            print("Erro: o número de vértices deve ser pelo menos 1.")
            return

        for i in range(num_vertices):
            rotulo = f"V{i+1}"
            peso_str = input(f"Digite o peso para o vértice {rotulo} (ou deixe em branco para padrão 0): ")
            peso = int(peso_str) if peso_str else 0
            grafo.adicionar_vertice(rotulo, peso)
            print(f"Vértice {rotulo} criado com sucesso.")
    except ValueError:
        print("Erro: o número de vértices deve ser um número inteiro.")
    
    input("Pressione Enter para continuar...")

def adicionar_vertice_ao_grafo(grafo: Grafo):
    rotulo = input("Digite o rótulo do vértice: ")
    peso_str = input(
        "Digite o peso do vértice (ou deixe em branco para padrão 0): ")
    peso = int(peso_str) if peso_str else 0
    grafo.adicionar_vertice(rotulo, peso)
    print(f"Vértice {rotulo} adicionado com sucesso.")
    input("Pressione Enter para continuar...")

def adicionar_aresta_ao_grafo(grafo: Grafo):
    if len(grafo.vertices) < 2:
        print("Erro: é necessário ter pelo menos dois vértices para adicionar uma aresta.")
        return

    rotulo = input("Digite o rótulo da aresta: ")
    peso_str = input(
        "Digite o peso da aresta (ou deixe em branco para padrão 0): ")
    peso = int(peso_str) if peso_str else 0

    try:
        print("\nEscolha o primeiro vértice:")
        listar_vertices(grafo.vertices)
        idx1 = int(input("Digite o índice do primeiro vértice: "))
        vertice1 = grafo.vertices[idx1]

        print("\nEscolha o segundo vértice:")
        listar_vertices(grafo.vertices)
        idx2 = int(input("Digite o índice do segundo vértice: "))
        vertice2 = grafo.vertices[idx2]

        grafo.adicionar_aresta(rotulo, peso, vertice1, vertice2)
        print(f"Aresta {rotulo} entre {vertice1.rotulo} e {vertice2.rotulo} adicionada com sucesso.")

    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def alterar_vertice_do_grafo(grafo: Grafo):
    listar_vertices(grafo.vertices)
    try:
        idx = int(input("Digite o índice do vértice que deseja alterar: "))
        vertice = grafo.vertices[idx]
        novo_rotulo = input(f"Digite o novo rótulo para o vértice {vertice.rotulo}: ")
        novo_peso_str = input(f"Digite o novo peso para o vértice {vertice.rotulo} (ou deixe em branco para manter o peso atual {vertice.peso}): ")
        novo_peso = int(novo_peso_str) if novo_peso_str else vertice.peso
        grafo.alterar_vertice(vertice, novo_rotulo, novo_peso)
        print(f"Vértice {vertice.rotulo} atualizado com sucesso.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def alterar_aresta_do_grafo(grafo: Grafo):
    listar_arestas(grafo.arestas)
    try:
        idx = int(input("Digite o índice da aresta que deseja alterar: "))
        aresta = grafo.arestas[idx]
        novo_rotulo = input(
            f"Digite o novo rótulo para a aresta {aresta.rotulo}: ")
        novo_peso_str = input(f"Digite o novo peso para a aresta {aresta.rotulo} (ou deixe em branco para manter o peso atual {aresta.peso}): ")
        novo_peso = int(novo_peso_str) if novo_peso_str else aresta.peso
        grafo.alterar_aresta(aresta, novo_rotulo, novo_peso)
        print(f"Aresta {aresta.rotulo} atualizada com sucesso.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def deletar_vertice_do_grafo(grafo: Grafo):
    listar_vertices(grafo.vertices)
    try:
        idx = int(input("Digite o índice do vértice que deseja deletar: "))
        vertice = grafo.vertices[idx]
        grafo.remover_vertice(vertice)
        print(
            f"Vértice {vertice.rotulo} e suas arestas foram deletados com sucesso.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def deletar_aresta_do_grafo(grafo: Grafo):
    listar_arestas(grafo.arestas)
    try:
        idx = int(input("Digite o índice da aresta que deseja deletar: "))
        aresta = grafo.arestas[idx]
        grafo.remover_aresta(aresta)
        print(f"Aresta {aresta.rotulo} foi deletada com sucesso.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def checar_adjacencia_vertices(grafo: Grafo):
    listar_vertices(grafo.vertices)
    try:
        idx1 = int(input("Digite o índice do primeiro vértice: "))
        idx2 = int(input("Digite o índice do segundo vértice: "))
        adjacente = grafo.checar_adjacencia_vertices(
            grafo.vertices[idx1], grafo.vertices[idx2])
        if adjacente:
            print(f"Os vértices {grafo.vertices[idx1].rotulo} e {grafo.vertices[idx2].rotulo} são adjacentes.")
        else:
            print(f"Os vértices {grafo.vertices[idx1].rotulo} e {grafo.vertices[idx2].rotulo} não são adjacentes.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def checar_adjacencia_arestas(grafo: Grafo):
    listar_arestas(grafo.arestas)
    try:
        idx1 = int(input("Digite o índice da primeira aresta: "))
        idx2 = int(input("Digite o índice da segunda aresta: "))
        adjacente = grafo.checar_adjacencia_arestas(
            grafo.arestas[idx1], grafo.arestas[idx2])
        if adjacente:
            print(f"As arestas {grafo.arestas[idx1].rotulo} e {grafo.arestas[idx2].rotulo} são adjacentes.")
        else:
            print(f"As arestas {grafo.arestas[idx1].rotulo} e {grafo.arestas[idx2].rotulo} não são adjacentes.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def checar_existencia_arestas(grafo: Grafo):
    print(grafo.checar_arestas())
    input("Pressione Enter para continuar...")

def checar_vertices_arestas(grafo: Grafo):
    print(grafo.verificar_arestas())
    input("Pressione Enter para continuar...")
    
# Checagem de existencia de articulaões
def checar_articulacoes(grafo: Grafo):
    print(grafo.checar_articulacoes())
    input("Pressione Enter para continuar...")

def grafo_vazio_completo(grafo: Grafo):
    # Exibe o rótulo de cada vértice para uma visualização mais clara
    print(grafo.checar_grafo())
    input("Pressione Enter para continuar...")
    

def exibir_matriz_adj(grafo: Grafo):
    """Exibe o grafo em forma de matriz de adjacencia"""
    if(grafo.direcionado is False):
        matrizND = grafo.exibir_matriz_adjacenciaND()
        string = '  '
        for v in grafo.vertices:
            string = string + v.rotulo + ' '
        print(string)
        for e, row in enumerate(matrizND):
            print(grafo.vertices[e].rotulo + " " + " ".join(map(str, row)))
    else:
        matrizD = grafo.exibir_matriz_adjacenciaD()
        string = '  '
        for v in grafo.vertices:
            string = string + v.rotulo + ' '
        print(string)
        for e, row in enumerate(matrizD):
            print(grafo.vertices[e].rotulo + " " + " ".join(map(str, row)))
    input("Pressione Enter para continuar...")

def exibir_matriz_inci(grafo: Grafo):
    """Exibe a matriz de incidencia do grafo"""

    if(grafo.direcionado is False):
        matrizND = grafo.exibir_matriz_incidenciaND()
        string = '  '
        for v in grafo.arestas:
            string = string + v.rotulo + ' '
        print(string)
        for e, row in enumerate(matrizND):
            print(grafo.vertices[e].rotulo + " " + " ".join(map(str, row)))

    else:
        matrizD = grafo.exibir_matriz_incidenciaD()
        string = '  '
        for v in grafo.arestas:
            string = string + v.rotulo + ' '
        print(string)
        for e, row in enumerate(matrizD):
            print(grafo.vertices[e].rotulo + " " + " ".join(map(str, row)))
    
    input("Pressione Enter para continuar...")

def verificar_conectividade(grafo: Grafo):
    print(grafo.verificar_conectividade())
    input("Pressione Enter para continuar...")
    
def verificar_conectividade_naive(grafo: Grafo):
    print(grafo.verificar_conectividade_naive())

def exibir_lista_adjacencia(grafo: Grafo):
    """Exibe a lista de adjacência do grafo, considerando se ele é direcionado ou não."""
    lista_adjacencia = {}

    for vertice in grafo.vertices:
        lista_adjacencia[vertice.rotulo] = []

    for aresta in grafo.arestas:
        origem, destino = aresta.vertices

        # Adicionar adjacência para grafos direcionados e não direcionados
        lista_adjacencia[origem.rotulo].append(destino.rotulo)
        if not grafo.direcionado:
            lista_adjacencia[destino.rotulo].append(origem.rotulo)

    # Exibição da lista de adjacência
    print("\nLista de Adjacência:")
    for vertice, adjacentes in lista_adjacencia.items():
        adjacentes_str = ", ".join(adjacentes)
        print(f"{vertice}: {adjacentes_str}")
        
    input("Pressione Enter para continuar...")

def verificar_componentes_fortemente_conexos(grafo: Grafo):
    componentes = kosaraju(grafo)
    print("Componentes fortemente conectados:")
    for i, componente in enumerate(componentes):
        print(f"Componente {i + 1}: {[vertice.rotulo for vertice in componente]}")
        
def carregar_grafo_json(nome_arquivo: str) -> Grafo:
    try:
        with open(nome_arquivo, 'r') as f:
            dados = json.load(f)
        
        grafo = Grafo(direcionado=dados["direcionado"])
        
        vertices = {}
        for vertice_data in dados["vertices"]:
            vertice = grafo.adicionar_vertice(vertice_data["rotulo"], vertice_data["peso"])
            vertices[vertice_data["rotulo"]] = vertice
        
        for aresta_data in dados["arestas"]:
            origem = vertices[aresta_data["origem"]]
            destino = vertices[aresta_data["destino"]]
            grafo.adicionar_aresta(aresta_data["rotulo"], aresta_data["peso"], origem, destino)
        
        print("Grafo carregado com sucesso a partir do arquivo JSON.")
        return grafo
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except KeyError as e:
        print(f"Erro: Chave {e} ausente no arquivo JSON.")
    except json.JSONDecodeError:
        print("Erro: O arquivo JSON está malformado.")

    return None

def salvar_grafo_json(grafo, nome_arquivo):
    grafo_dict = {
        "vertices": [{"rotulo": v.rotulo, "peso": v.peso} for v in grafo.vertices],
        "arestas": [{"rotulo": a.rotulo, "peso": a.peso, "vertice1": a.vertices[0].rotulo, "vertice2": a.vertices[1].rotulo} for a in grafo.arestas],
        "direcionado": grafo.direcionado
    }
    with open(nome_arquivo, 'w') as f:
        json.dump(grafo_dict, f, indent=4)

def verificar_componentes_fortemente_conexos(grafo: Grafo):
    componentes = kosaraju(grafo)
    print("Componentes fortemente conectados:")
    for i, componente in enumerate(componentes):
        print(f"Componente {i + 1}: {[vertice.rotulo for vertice in componente]}")
        
def carregar_grafo_json(nome_arquivo: str) -> Grafo:
    try:
        with open(nome_arquivo, 'r') as f:
            dados = json.load(f)
        
        grafo = Grafo(direcionado=dados["direcionado"])
        
        vertices = {}
        for vertice_data in dados["vertices"]:
            vertice = grafo.adicionar_vertice(vertice_data["rotulo"], vertice_data["peso"])
            vertices[vertice_data["rotulo"]] = vertice
        
        for aresta_data in dados["arestas"]:
            origem = vertices[aresta_data["origem"]]
            destino = vertices[aresta_data["destino"]]
            grafo.adicionar_aresta(aresta_data["rotulo"], aresta_data["peso"], origem, destino)
        
        print("Grafo carregado com sucesso a partir do arquivo JSON.")
        return grafo
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except KeyError as e:
        print(f"Erro: Chave {e} ausente no arquivo JSON.")
    except json.JSONDecodeError:
        print("Erro: O arquivo JSON está malformado.")

    return None

def executar_fleury(grafo: Grafo):
    """
    Executa o algoritmo de Fleury em um grafo e salva o resultado em um arquivo com nome incremental.
    Parâmetros:
        grafo: Instância de Grafo.
    """
    if not grafo:
        print("Erro: Nenhum grafo carregado ou criado. Crie ou carregue um grafo primeiro.")
        return

    # Criar diretório para salvar o arquivo de saída
    pasta_resultados = "resultados"
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Medir tempo de execução
    inicio_tempo = time.time()
    auxGrafo = grafo
    resultado = fleury(auxGrafo)
    tempo_execucao = time.time() - inicio_tempo

    # Criar o conteúdo do arquivo
    if isinstance(resultado, list):
        conteudo = "Ciclo Euleriano encontrado:\n" + " -> ".join(resultado) + "\n"
    else:
        conteudo = f"Erro durante a execução: {resultado}\n"

    conteudo += f"\nTempo de execução: {tempo_execucao:.4f} segundos\n"

    # Verificar se o arquivo já existe e criar um novo nome incremental
    arquivo_saida = os.path.join(pasta_resultados, "resultado_fleury.txt")
    contador = 1
    while os.path.exists(arquivo_saida):
        arquivo_saida = os.path.join(pasta_resultados, f"resultado_fleury_{contador}.txt")
        contador += 1

    # Escrever o resultado em um arquivo
    with open(arquivo_saida, "w") as arquivo:
        arquivo.write(conteudo)

    print(f"Resultado salvo em '{arquivo_saida}'")


def executar_fleury_tarjan(grafo: Grafo):
    """
    Executa o algoritmo de Fleury usando Tarjan para detectar pontes e salva o resultado em um arquivo.
    Parâmetros:
        grafo: Instância de Grafo.
    """
    if not grafo:
        print("Erro: Nenhum grafo carregado ou criado. Crie ou carregue um grafo primeiro.")
        return

    # Criar diretório para salvar o arquivo de saída
    pasta_resultados = "resultados"
    if not os.path.exists(pasta_resultados):
        os.makedirs(pasta_resultados)

    # Medir tempo de execução
    inicio_tempo = time.time()
    auxGrafo = grafo
    resultado = fleury_com_tarjan(auxGrafo)
    tempo_execucao = time.time() - inicio_tempo

    # Criar o conteúdo do arquivo
    if isinstance(resultado, list):
        conteudo = "Caminho Euleriano encontrado (usando Tarjan):\n" + " -> ".join(resultado) + "\n"
    else:
        conteudo = f"Erro durante a execução: {resultado}\n"

    conteudo += f"\nTempo de execução: {tempo_execucao:.4f} segundos\n"

    # Verificar se o arquivo já existe e criar um novo nome incremental
    arquivo_saida = os.path.join(pasta_resultados, "resultado_fleury_tarjan.txt")
    contador = 1
    while os.path.exists(arquivo_saida):
        arquivo_saida = os.path.join(pasta_resultados, f"resultado_fleury_tarjan_{contador}.txt")
        contador += 1

    # Escrever o resultado em um arquivo
    with open(arquivo_saida, "w") as arquivo:
        arquivo.write(conteudo)

    print(f"Resultado salvo em '{arquivo_saida}'")

    
def ajustar_grafo_grau_2(grafo):
    """
    Ajusta um grafo para que todos os vértices tenham grau 2, conectando 
    vértices sequencialmente (1 com 2, 2 com 3, ...).
    Parâmetros:
        grafo: Instância de Grafo.
    """
    if len(grafo.vertices) < 2:
        print("Erro: O grafo deve ter pelo menos dois vértices.")
        return

    # Limpar as arestas existentes
    grafo.arestas.clear()
    for vertice in grafo.vertices:
        vertice.arestas.clear()

    # Adicionar arestas sequenciais
    for i in range(len(grafo.vertices) - 1):
        vertice_atual = grafo.vertices[i]
        proximo_vertice = grafo.vertices[i + 1]
        rotulo_aresta = f"A{i+1}"
        grafo.adicionar_aresta(rotulo_aresta, 0, vertice_atual, proximo_vertice)

    # Conectar o último vértice ao primeiro para formar um ciclo
    if len(grafo.vertices) > 2:
        rotulo_aresta = f"A{len(grafo.vertices)}"
        grafo.adicionar_aresta(rotulo_aresta, 0, grafo.vertices[-1], grafo.vertices[0])

    print("Grafo ajustado com sucesso para que todos os vértices tenham grau 2.")
    print(grafo)
def exportar_csv(grafo: Grafo):
    nome = input('Insira o nome do arquivo (ex: "Grafo1"):')
    grafo.gerar_csv(nome, grafo.direcionado)

def ler_from_csv(grafo: Grafo):
    grafo.ler_grafo_from_csv()

def main():
    grafo = None  # Inicializar a variável do grafo

    while True:
        opcao = mostrar_menu()
        match opcao:
            case '0': 
                nome_arquivo = input("Digite o nome do arquivo JSON (ex: grafo.json): ")
                grafo = carregar_grafo_json(nome_arquivo) 
            case '1': 
                direcionado = input("O grafo é direcionado? (s/n): ").strip().lower() == 's'
                grafo = Grafo(direcionado)
                file_name = input('Insira o nome do arquivo(não informe a extensão ".csv"):')
                file_name = file_name + ".csv"
                grafo.ler_grafo_from_csv(file_name)
                
            case '2': 
                grafo = Grafo(direcionado=False)
                
                grafo = grafo.criarGrafo()
                salvar = input("Deseja salvar o grafo em um arquivo JSON? (s/n): ").strip().lower() == 's'
                if salvar:
                    nome_arquivo = input("Digite o nome do arquivo JSON para salvar o grafo (ex: novo_grafo.json): ")
                    salvar_grafo_json(grafo, nome_arquivo)
            case '3': adicionar_vertice_ao_grafo(grafo)
            case '4': adicionar_aresta_ao_grafo(grafo)
            case '5': print(grafo)
            case '6': alterar_vertice_do_grafo(grafo)
            case '7': alterar_aresta_do_grafo(grafo)
            case '8': deletar_vertice_do_grafo(grafo)
            case '9': deletar_aresta_do_grafo(grafo)
            case '10': checar_adjacencia_vertices(grafo)
            case '11': checar_adjacencia_arestas(grafo)
            case '12': checar_existencia_arestas(grafo)
            case '13': checar_vertices_arestas(grafo)
            case '14': grafo_vazio_completo(grafo)
            case '15': checar_articulacoes(grafo)
            case '16': exibir_matriz_adj(grafo)
            case '17': exibir_matriz_inci(grafo)
            case '18': verificar_conectividade(grafo)
            case '19': verificar_conectividade_naive(grafo)
            case '20': exibir_lista_adjacencia(grafo)
            case '21': verificar_componentes_fortemente_conexos(grafo)
            case '22':
                pontes = encontrar_pontes_tarjan(grafo)
                print("Pontes encontradas:", pontes)
            case '23': exportar_csv(grafo)
            case '24': executar_fleury(grafo)
            case '25': executar_fleury_tarjan(grafo)
            case '26': break
            case '98': print(encontrar_pontes(grafo))
            case '99': ajustar_grafo_grau_2(grafo)
            case _: print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
