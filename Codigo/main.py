import json
from grafo import Grafo
from vertice import listar_vertices
from aresta import listar_arestas
from algoritmo import kosaraju


def mostrar_menu():
    print("\nMenu de Opções:")
    print("0. Carregar grafo a partir de arquivo JSON")
    print("1. Adicionar vértice")
    print("2. Adicionar aresta")
    print("3. Exibir grafo")
    print("4. Alterar vértice")
    print("5. Alterar aresta")
    print("6. Deletar vértice")
    print("7. Deletar aresta")
    print("8. Checar adjacência entre vértices")
    print("9. Checar adjacência entre arestas")
    print("10. Checagem da existência de arestas")
    print("11. Checagem da quantidade de vértices e arestas")
    print("12. Checagem de grafo vazio e completo")
    print("13. Exibir matriz de adjacencia:")
    print("14. Exibir matriz de incidencia")
    print("15. Verificar conectividade")
    print("16. Verificar componentes fortemente conectos com Kosaraju")
    print("17. Sair")
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

def adicionar_vertice_ao_grafo(grafo: Grafo):
    rotulo = input("Digite o rótulo do vértice: ")
    peso_str = input(
        "Digite o peso do vértice (ou deixe em branco para padrão 0): ")
    peso = int(peso_str) if peso_str else 0
    grafo.adicionar_vertice(rotulo, peso)
    print(f"Vértice {rotulo} adicionado com sucesso.")

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

def deletar_aresta_do_grafo(grafo: Grafo):
    listar_arestas(grafo.arestas)
    try:
        idx = int(input("Digite o índice da aresta que deseja deletar: "))
        aresta = grafo.arestas[idx]
        grafo.remover_aresta(aresta)
        print(f"Aresta {aresta.rotulo} foi deletada com sucesso.")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")

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

def checar_existencia_arestas(grafo: Grafo):
    print(grafo.checar_arestas())

def checar_vertices_arestas(grafo: Grafo):
    print(grafo.verificar_arestas())

def grafo_vazio_completo(grafo: Grafo):
    # Exibe o rótulo de cada vértice para uma visualização mais clara
    print(grafo.checar_grafo())

def exibir_matriz_adj(grafo: Grafo):
    """Exibe o grafo em forma de matriz de adjacencia"""
    if (grafo.direcionado is False):
        print(grafo.exibir_matriz_adjacenciaND())
    else:
        print(grafo.exibir_matriz_adjacenciaD())

def exibir_matriz_inci(grafo: Grafo):
    """Exibe a matriz de incidencia do grafo"""
    if (grafo.direcionado is False):
        print(grafo.exibir_matriz_incidenciaND())
    else:
        print(grafo.exibir_matriz_incidenciaD())

def verificar_conectividade(grafo: Grafo):
    print(grafo.verificar_conectividade_nd())

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
            case '1': adicionar_vertice_ao_grafo(grafo)
            case '2': adicionar_aresta_ao_grafo(grafo)
            case '3': print(grafo)
            case '4': alterar_vertice_do_grafo(grafo)
            case '5': alterar_aresta_do_grafo(grafo)
            case '6': deletar_vertice_do_grafo(grafo)
            case '7': deletar_aresta_do_grafo(grafo)
            case '8': checar_adjacencia_vertices(grafo)
            case '9': checar_adjacencia_arestas(grafo)
            case '10': checar_existencia_arestas(grafo)
            case '11': checar_vertices_arestas(grafo)
            case '12': grafo_vazio_completo(grafo)
            case '13': exibir_matriz_adj(grafo)
            case '14': exibir_matriz_inci(grafo)
            case '15': verificar_conectividade(grafo)
            case '16': verificar_componentes_fortemente_conexos(grafo)
            case '17': break
            case _: print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
