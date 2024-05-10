from sys import maxsize
from itertools import permutations

# Função para calcular a distância total da rota
def calculate_distance(route, graph):
    distance = 0
    for i in range(len(route) - 1):
        distance += graph[route[i]][route[i+1]]
    return distance

# Função para encontrar a rota mais curta
def travelling_salesman(graph, v):
    # Todas as permutações dos vértices (exceto o primeiro)
    perm = permutations(v[1:])

    min_path = maxsize
    min_route = None

    for i in perm:
        # Adiciona o primeiro vértice no início e no fim
        route = (v[0],) + i + (v[0],)

        current_path = calculate_distance(route, graph)

        # Atualiza a rota mínima se a rota atual for menor
        if current_path < min_path:
            min_path = current_path
            min_route = route

    return min_route, min_path

# Exemplo de uso
if __name__ == "__main__":
    # Matriz de adjacência do grafo
    graph = [[0, 10, 15, 20],
             [10, 0, 35, 25],
             [15, 35, 0, 30],
             [20, 25, 30, 0]]
    v = [0, 1, 2, 3]
    route, distance = travelling_salesman(graph, v)
    print("A rota mais curta é:", route)
    print("A distância total é:", distance)