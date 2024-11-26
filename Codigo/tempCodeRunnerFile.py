def carregar_grafo_json(nome_arquivo: str) -> Grafo:
#     try:
#         with open(nome_arquivo, 'r') as f:
#             dados = json.load(f)
        
#         grafo = Grafo(direcionado=dados["direcionado"])
        
#         vertices = {}
#         for vertice_data in dados["vertices"]:
#             vertice = grafo.adicionar_vertice(vertice_data["rotulo"], vertice_data["peso"])
#             vertices[vertice_data["rotulo"]] = vertice
        
#         for aresta_data in dados["arestas"]:
#             origem = vertices[aresta_data["origem"]]
#             destino = vertices[aresta_data["destino"]]
#             grafo.adicionar_aresta(aresta_data["rotulo"], aresta_data["peso"], origem, destino)
        
#         print("Grafo carregado com sucesso a partir do arquivo JSON.")
#         return grafo
    
#     except FileNotFoundError:
#         print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
#     except KeyError as e:
#         print(f"Erro: Chave {e} ausente no arquivo JSON.")
#     except json.JSONDecodeError:
#         print("Erro: O arquivo JSON está malformado.")

#     return None
