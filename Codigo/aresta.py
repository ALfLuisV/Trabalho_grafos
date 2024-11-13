# aresta.py
from vertice import Vertice

class Aresta:
    def __init__(self, rotulo: str, peso: int, vertice1: Vertice, vertice2: Vertice):
        self.rotulo = rotulo      # Identificador da aresta (rótulo)
        self.peso = peso          # Peso da aresta
        self.vertices = (vertice1, vertice2)  # Aresta conecta dois vértices
   
    def __str__(self):
        return f"Aresta {self.rotulo}: de {self.vertices[0].rotulo} para {self.vertices[1].rotulo} com peso {self.peso}"

def listar_arestas(arestas):
    """Função para exibir todas as arestas disponíveis com índices."""
    for i, aresta in enumerate(arestas):
        print(f"{i}: {aresta}")

def alterar_aresta(arestas):
    """Permite alterar o rótulo e o peso de uma aresta selecionada."""
    listar_arestas(arestas)
    try:
        idx = int(input("Digite o índice da aresta que deseja alterar: "))
        aresta = arestas[idx]

        novo_rotulo = input(f"Novo rótulo para a aresta {aresta.rotulo} (deixe vazio para manter): ")
        if novo_rotulo:
            aresta.rotulo = novo_rotulo

        novo_peso = input(f"Novo peso para a aresta {aresta.peso} (deixe vazio para manter): ")
        if novo_peso:
            aresta.peso = int(novo_peso)
        
        print(f"Aresta atualizada: {aresta}")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
