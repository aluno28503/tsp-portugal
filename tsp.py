import random
from haversine import haversine

def calcular_matriz_distancias(pontos):
    n = len(pontos)
    matriz = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(pontos[i]["lat"], pontos[i]["lon"],
                          pontos[j]["lat"], pontos[j]["lon"])
            matriz[i][j] = d
            matriz[j][i] = d

    return matriz

def nearest_neighbor(pontos, start=0):
    n = len(pontos)
    matriz = calcular_matriz_distancias(pontos)

    visitados = [False] * n
    percurso = [start]
    visitados[start] = True
    distancia_total = 0.0

    atual = start

    for _ in range(n - 1):
        menor_dist = float('inf')
        proximo = -1

        for j in range(n):
            if not visitados[j] and matriz[atual][j] < menor_dist:
                menor_dist = matriz[atual][j]
                proximo = j

        percurso.append(proximo)
        visitados[proximo] = True
        distancia_total += menor_dist
        atual = proximo

    distancia_total += matriz[atual][start]
    percurso.append(start)

    return percurso, distancia_total

def rota_aleatoria(pontos, start=0):
    matriz = calcular_matriz_distancias(pontos)
    n = len(pontos)

    outros = [i for i in range(n) if i != start]
    random.shuffle(outros)

    percurso = [start] + outros + [start]
    distancia_total = 0.0

    for i in range(len(percurso) - 1):
        distancia_total += matriz[percurso[i]][percurso[i + 1]]

    return percurso, distancia_total

def two_opt(pontos, percurso_inicial):
    matriz = calcular_matriz_distancias(pontos)

    def calcular_distancia_percurso(percurso):
        total = 0.0
        for i in range(len(percurso) - 1):
            total += matriz[percurso[i]][percurso[i + 1]]
        return total

    melhor = list(percurso_inicial[:-1])
    melhor_dist = calcular_distancia_percurso(percurso_inicial)
    melhorou = True

    while melhorou:
        melhorou = False
        for i in range(1, len(melhor) - 1):
            for j in range(i + 1, len(melhor)):
                novo = melhor[:i] + melhor[i:j + 1][::-1] + melhor[j + 1:]
                novo_percurso = novo + [novo[0]]
                nova_dist = calcular_distancia_percurso(novo_percurso)

                if nova_dist < melhor_dist - 1e-10:
                    melhor = novo
                    melhor_dist = nova_dist
                    melhorou = True

    melhor_percurso = melhor + [melhor[0]]
    return melhor_percurso, melhor_dist

def analisar_clusters(pontos, matriz=None):
    if matriz is None:
        matriz = calcular_matriz_distancias(pontos)

    limiar_km = 10.0
    n = len(pontos)
    visitado = [False] * n
    clusters = []

    for i in range(n):
        if visitado[i]:
            continue
        cluster = [i]
        visitado[i] = True
        for j in range(i + 1, n):
            if not visitado[j] and matriz[i][j] < limiar_km:
                cluster.append(j)
                visitado[j] = True
        if len(cluster) > 1:
            clusters.append(cluster)

    return clusters
