import json
from grafo import Grafo
from vertice import listar_vertices
from aresta import listar_arestas
from algoritmo import kosaraju


def mostrar_menu():
    print("\nMenu de Opções:")
    print("0. Carregar grafo a partir de arquivo JSON")
    print("1. Criar grafo aleatorio baseado em seu numero de vertices")
    print("2. Adicionar vértice")
    print("3. Adicionar aresta")
    print("4. Exibir grafo")
    print("5. Alterar vértice")
    print("6. Alterar aresta")
    print("7. Deletar vértice")
    print("8. Deletar aresta")
    print("9. Checar adjacência entre vértices")
    print("10. Checar adjacência entre arestas")
    print("11. Checagem da existência de arestas")
    print("12. Checagem da quantidade de vértices e arestas")
    print("13. Checagem de grafo vazio e completo")
    print("14. Checagem de articulações (por busca em profundidade)")
    print("15. Exibir matriz de adjacencia:")
    print("16. Exibir matriz de incidencia")
    print("17. Verificar conectividade")
    print("18. Verificar conectividade (naive)")
    print("19. Exibir lista de adjacência")
    print("20. Sair")
    return input("Escolha uma opção: ")

def criar_vertices_iniciais(grafo):
    try:
        num_vertices = int(input("Quantos vértices deseja criar? "))
        if num_vertices < 1:
            print("Erro: o número de vértices deve ser pelo menos 1.")
            return

        for i in range(num_vertices):
            rotulo = f"V{i+1}"
            peso_str = input(f"Digite o peso para o vértice {
                             rotulo} (ou deixe em branco para padrão 0): ")
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
        print(f"Aresta {rotulo} entre {vertice1.rotulo} e {
              vertice2.rotulo} adicionada com sucesso.")

    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
        
    input("Pressione Enter para continuar...")

def alterar_vertice_do_grafo(grafo: Grafo):
    listar_vertices(grafo.vertices)
    try:
        idx = int(input("Digite o índice do vértice que deseja alterar: "))
        vertice = grafo.vertices[idx]
        novo_rotulo = input(f"Digite o novo rótulo para o vértice {
                            vertice.rotulo}: ")
        novo_peso_str = input(f"Digite o novo peso para o vértice {
                              vertice.rotulo} (ou deixe em branco para manter o peso atual {vertice.peso}): ")
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
        novo_peso_str = input(f"Digite o novo peso para a aresta {
                              aresta.rotulo} (ou deixe em branco para manter o peso atual {aresta.peso}): ")
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
            print(f"Os vértices {grafo.vertices[idx1].rotulo} e {
                  grafo.vertices[idx2].rotulo} são adjacentes.")
        else:
            print(f"Os vértices {grafo.vertices[idx1].rotulo} e {
                  grafo.vertices[idx2].rotulo} não são adjacentes.")
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
            print(f"As arestas {grafo.arestas[idx1].rotulo} e {
                  grafo.arestas[idx2].rotulo} são adjacentes.")
        else:
            print(f"As arestas {grafo.arestas[idx1].rotulo} e {
                  grafo.arestas[idx2].rotulo} não são adjacentes.")
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
    if (grafo.direcionado is False):
        print(grafo.exibir_matriz_adjacenciaND())
    else:
        print(grafo.exibir_matriz_adjacenciaD())
        
    input("Pressione Enter para continuar...")

def exibir_matriz_inci(grafo: Grafo):
    """Exibe a matriz de incidencia do grafo"""
    if (grafo.direcionado is False):
        print(grafo.exibir_matriz_incidenciaND())
    else:
        print(grafo.exibir_matriz_incidenciaD())
    
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
        print(f"Componente {
            i + 1}: {[vertice.rotulo for vertice in componente]}")
        
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

def main():
    # direcionado = input(
    #     "O grafo é direcionado? (s/n): ").strip().lower() == 's'
    # grafo = Grafo(direcionado=direcionado)
    # criar_vertices_iniciais(grafo)

    while True:
        opcao = mostrar_menu()
        match opcao:
            case '0': 
                nome_arquivo = input("Digite o nome do arquivo JSON (ex: grafo.json): ")
                grafo = carregar_grafo_json(nome_arquivo) 
            case '1': 
                grafo = Grafo(direcionado=False)
                grafo = grafo.criarGrafo()
                salvar = input("Deseja salvar o grafo em um arquivo JSON? (s/n): ").strip().lower() == 's'
                if salvar:
                    nome_arquivo = input("Digite o nome do arquivo JSON para salvar o grafo (ex: novo_grafo.json): ")
                    salvar_grafo_json(grafo, nome_arquivo)
            case '2': adicionar_vertice_ao_grafo(grafo)
            case '3': adicionar_aresta_ao_grafo(grafo)
            case '4': print(grafo)
            case '5': alterar_vertice_do_grafo(grafo)
            case '6': alterar_aresta_do_grafo(grafo)
            case '7': deletar_vertice_do_grafo(grafo)
            case '8': deletar_aresta_do_grafo(grafo)
            case '9': checar_adjacencia_vertices(grafo)
            case '10': checar_adjacencia_arestas(grafo)
            case '11': checar_existencia_arestas(grafo)
            case '12': checar_vertices_arestas(grafo)
            case '13': grafo_vazio_completo(grafo)
            case '14': checar_articulacoes(grafo)
            case '15': exibir_matriz_adj(grafo)
            case '16': exibir_matriz_inci(grafo)
            case '17': verificar_conectividade(grafo)
            case '18': verificar_conectividade_naive(grafo)
            case '19': exibir_lista_adjacencia(grafo)
            case '20': break
            case _: print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
