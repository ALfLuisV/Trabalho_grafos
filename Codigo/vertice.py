# vertice.py
class Vertice:
    def __init__(self, rotulo: str, peso: int):
        self.rotulo = rotulo      # Identificador do vértice (rótulo)
        self.peso = peso          # Peso do vértice
        self.arestas = []         # Lista de arestas conectadas a este vértice
   
    def adicionar_aresta(self, aresta):
        self.arestas.append(aresta)

    def __str__(self):
        return f"Vértice {self.rotulo} (Peso: {self.peso})"

def listar_vertices(vertices):
    """Função para exibir todos os vértices disponíveis com índices."""
    for i, vertice in enumerate(vertices):
        print(f"{i}: {vertice}")

def alterar_vertice(vertices):
    """Permite alterar o rótulo e o peso de um vértice selecionado."""
    listar_vertices(vertices)
    try:
        idx = int(input("Digite o índice do vértice que deseja alterar: "))
        vertice = vertices[idx]

        novo_rotulo = input(f"Novo rótulo para o vértice {vertice.rotulo} (deixe vazio para manter): ")
        if novo_rotulo:
            vertice.rotulo = novo_rotulo

        novo_peso = input(f"Novo peso para o vértice {vertice.peso} (deixe vazio para manter): ")
        if novo_peso:
            vertice.peso = int(novo_peso)
        
        print(f"Vértice atualizado: {vertice}")
    except (ValueError, IndexError):
        print("Erro: índice inválido ou entrada incorreta.")
