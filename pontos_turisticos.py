"""
Trabalho Final (Parte II) - Heurísticas
O Problema do Caixeiro Viajante em Contextos Reais

Implementação da heurística do vizinho mais próximo (Nearest Neighbor)
para otimização de percursos turísticos em Portugal.

Autores:
    - Rodrigo Andrade (aluno28503)
    - Eric Cardoso (aluno20518)
"""

import math
import random
import folium
import os
import sys

# Garantir codificação UTF-8 na consola (Windows)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# =============================================================================
# 1. Representação dos Pontos Turísticos
# =============================================================================

pontos_turisticos = [
    {"id": 0,  "nome": "Santarém (ponto de partida)",                    "lat": 39.236, "lon": -8.687},
    {"id": 1,  "nome": "Mosteiro dos Jerónimos (UNESCO)",                "lat": 38.697, "lon": -9.205},
    {"id": 2,  "nome": "Torre de Belém (UNESCO)",                        "lat": 38.691, "lon": -9.216},
    {"id": 3,  "nome": "Centro Histórico de Sintra (UNESCO)",            "lat": 38.797, "lon": -9.390},
    {"id": 4,  "nome": "Palácio Nacional da Pena",                       "lat": 38.787, "lon": -9.390},
    {"id": 5,  "nome": "Convento de Cristo (UNESCO)",                    "lat": 39.603, "lon": -8.414},
    {"id": 6,  "nome": "Mosteiro da Batalha (UNESCO)",                   "lat": 39.659, "lon": -8.825},
    {"id": 7,  "nome": "Mosteiro de Alcobaça (UNESCO)",                  "lat": 39.548, "lon": -8.979},
    {"id": 8,  "nome": "Universidade de Coimbra (UNESCO)",               "lat": 40.208, "lon": -8.423},
    {"id": 9,  "nome": "Centro Histórico do Porto (UNESCO)",             "lat": 41.142, "lon": -8.615},
    {"id": 10, "nome": "Ponte D. Luís I",                                "lat": 41.140, "lon": -8.609},
    {"id": 11, "nome": "Centro Histórico de Guimarães (UNESCO)",         "lat": 41.444, "lon": -8.296},
    {"id": 12, "nome": "Castelo de Guimarães",                           "lat": 41.447, "lon": -8.290},
    {"id": 13, "nome": "Bom Jesus do Monte (UNESCO)",                    "lat": 41.554, "lon": -8.379},
    {"id": 14, "nome": "Palácio Nacional de Mafra (UNESCO)",             "lat": 38.937, "lon": -9.327},
    {"id": 15, "nome": "Centro Histórico de Évora (UNESCO)",             "lat": 38.571, "lon": -7.909},
    {"id": 16, "nome": "Templo Romano de Évora",                         "lat": 38.573, "lon": -7.909},
    {"id": 17, "nome": "Centro Histórico de Elvas (UNESCO)",             "lat": 38.879, "lon": -7.162},
    {"id": 18, "nome": "Castelo de Óbidos",                              "lat": 39.360, "lon": -9.156},
    {"id": 19, "nome": "Castelo de São Jorge",                           "lat": 38.713, "lon": -9.133},
    {"id": 20, "nome": "Museu Nacional de Arte Antiga",                  "lat": 38.707, "lon": -9.170},
    {"id": 21, "nome": "Museu Nacional do Azulejo",                      "lat": 38.728, "lon": -9.115},
    {"id": 22, "nome": "Museu Nacional dos Coches",                      "lat": 38.699, "lon": -9.201},
    {"id": 23, "nome": "Fundação de Serralves",                          "lat": 41.159, "lon": -8.659},
    {"id": 24, "nome": "Castelo de Bragança",                            "lat": 41.806, "lon": -6.757},
    {"id": 25, "nome": "Castelo de Marvão",                              "lat": 39.393, "lon": -7.378},
    {"id": 26, "nome": "Castelo de Almourol",                            "lat": 39.463, "lon": -8.347},
    {"id": 27, "nome": "Museu do Douro (UNESCO Alto Douro)",             "lat": 41.163, "lon": -7.789},
    {"id": 28, "nome": "Parque Arqueológico do Vale do Côa (UNESCO)",    "lat": 41.079, "lon": -7.154},
    {"id": 29, "nome": "Sé Velha de Coimbra",                            "lat": 40.210, "lon": -8.426},
]


# =============================================================================
# 2. Função Haversine
# =============================================================================

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Raio médio da Terra em km

    # Converter graus para radianos
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Fórmula de Haversine
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    d = 2 * R * math.asin(math.sqrt(a))

    return d


# =============================================================================
# 3. Matriz de Distâncias
# =============================================================================

def calcular_matriz_distancias(pontos):
    """
    Calcula a matriz de distâncias entre todos os pares de pontos turísticos.

    Retorna:
        Lista de listas (matriz NxN) com as distâncias em km.
    """
    n = len(pontos)
    matriz = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(pontos[i]["lat"], pontos[i]["lon"],
                          pontos[j]["lat"], pontos[j]["lon"])
            matriz[i][j] = d
            matriz[j][i] = d

    return matriz


# =============================================================================
# 4. Heurística do Vizinho Mais Próximo (Nearest Neighbor)
# =============================================================================

def nearest_neighbor(pontos, start=0):
    """
    Implementa a heurística do vizinho mais próximo para o TSP.

    Parâmetros:
        pontos - lista de dicionários com os pontos turísticos
        start  - índice do ponto de partida (default: 0 = Santarém)

    Retorna:
        percurso       - lista ordenada dos índices dos pontos visitados
        distancia_total - distância total do percurso em km
    """
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

    # Regressar ao ponto inicial
    distancia_total += matriz[atual][start]
    percurso.append(start)

    return percurso, distancia_total


# =============================================================================
# 5. Solução Aleatória (para comparação)
# =============================================================================

def rota_aleatoria(pontos, start=0):
    """
    Gera uma rota aleatória que começa e termina no ponto de partida.

    Retorna:
        percurso        - lista dos índices visitados
        distancia_total - distância total em km
    """
    matriz = calcular_matriz_distancias(pontos)
    n = len(pontos)

    # Criar lista de todos os índices exceto o de partida
    outros = [i for i in range(n) if i != start]
    random.shuffle(outros)

    percurso = [start] + outros + [start]
    distancia_total = 0.0

    for i in range(len(percurso) - 1):
        distancia_total += matriz[percurso[i]][percurso[i + 1]]

    return percurso, distancia_total


# =============================================================================
# 6. Melhoria 2-opt
# =============================================================================

def two_opt(pontos, percurso_inicial):
    """
    Aplica a heurística de melhoria 2-opt ao percurso inicial.

    A ideia é inverter segmentos do percurso para tentar reduzir
    a distância total, repetindo até não haver mais melhorias.

    Retorna:
        melhor_percurso  - percurso melhorado
        melhor_distancia - distância total do percurso melhorado
    """
    matriz = calcular_matriz_distancias(pontos)

    def calcular_distancia_percurso(percurso):
        total = 0.0
        for i in range(len(percurso) - 1):
            total += matriz[percurso[i]][percurso[i + 1]]
        return total

    # Trabalhar com o percurso sem o regresso ao início
    melhor = list(percurso_inicial[:-1])
    melhor_dist = calcular_distancia_percurso(percurso_inicial)
    melhorou = True

    while melhorou:
        melhorou = False
        for i in range(1, len(melhor) - 1):
            for j in range(i + 1, len(melhor)):
                # Inverter o segmento entre i e j
                novo = melhor[:i] + melhor[i:j + 1][::-1] + melhor[j + 1:]
                novo_percurso = novo + [novo[0]]
                nova_dist = calcular_distancia_percurso(novo_percurso)

                if nova_dist < melhor_dist - 1e-10:
                    melhor = novo
                    melhor_dist = nova_dist
                    melhorou = True

    melhor_percurso = melhor + [melhor[0]]
    return melhor_percurso, melhor_dist


# =============================================================================
# 7. Visualização com Folium
# =============================================================================

def criar_mapa(pontos, percurso, titulo="Percurso TSP", nome_ficheiro="mapa_percurso.html"):
    """
    Cria um mapa interativo simples com Folium mostrando o percurso.
    """
    # Centro do mapa (aproximadamente centro de Portugal continental)
    mapa = folium.Map(location=[39.7, -8.2], zoom_start=7, tiles="OpenStreetMap")

    # Adicionar marcadores simples para cada ponto
    for i, ponto in enumerate(pontos):
        if i in percurso:
            ordem = percurso.index(i)
        else:
            ordem = "?"

        # Apenas um marcador circular simples (ponto)
        cor = "green" if i == percurso[0] else "red"
        tamanho = 8 if i == percurso[0] else 5

        folium.CircleMarker(
            location=[ponto["lat"], ponto["lon"]],
            radius=tamanho,
            color=cor,
            fill=True,
            fill_color=cor,
            fill_opacity=1.0,
            tooltip=f"{ordem}. {ponto['nome']}"
        ).add_to(mapa)

    # Desenhar o percurso (linhas simples a unir os pontos)
    coordenadas_percurso = [
        [pontos[idx]["lat"], pontos[idx]["lon"]]
        for idx in percurso
    ]

    folium.PolyLine(
        coordenadas_percurso,
        color="blue",
        weight=2,
        opacity=0.6
    ).add_to(mapa)

    # Adicionar apenas o título no canto superior direito
    titulo_html = f"""
    <div style="position: fixed; top: 10px; right: 10px; z-index: 1000;
                background-color: white; padding: 10px; border-radius: 5px;
                border: 1px solid black; font-family: Arial; font-weight: bold;">
        {titulo}
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(titulo_html))

    # Guardar o mapa
    mapa.save(nome_ficheiro)
    print(f"Mapa guardado em: {os.path.abspath(nome_ficheiro)}")

    return mapa


# =============================================================================
# 8. Impressão do Percurso
# =============================================================================

def imprimir_percurso(pontos, percurso, distancia_total, titulo="PERCURSO"):
    """Imprime o percurso detalhado com distâncias entre cada par de pontos."""
    print(f"\n{'=' * 70}")
    print(f"  {titulo}")
    print(f"{'=' * 70}")

    matriz = calcular_matriz_distancias(pontos)

    for i in range(len(percurso) - 1):
        origem = percurso[i]
        destino = percurso[i + 1]
        dist = matriz[origem][destino]
        print(f"  {i + 1:2d}. {pontos[origem]['nome']}")
        print(f"      → {dist:.1f} km")

    # Último ponto (regresso)
    print(f"  {len(percurso):2d}. {pontos[percurso[-1]]['nome']} (regresso)")
    print(f"{'=' * 70}")
    print(f"  Distância total: {distancia_total:.2f} km")
    print(f"  Pontos visitados: {len(percurso) - 1} (+ regresso ao início)")
    print(f"{'=' * 70}\n")


# =============================================================================
# 9. Análise de Clusters
# =============================================================================

def analisar_clusters(pontos, matriz=None):
    """
    Identifica clusters de pontos próximos para a análise da heurística.

    Retorna uma lista de clusters (pontos com distância < limiar entre si).
    """
    if matriz is None:
        matriz = calcular_matriz_distancias(pontos)

    limiar_km = 10.0  # Pontos a menos de 10 km consideram-se no mesmo cluster
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


# =============================================================================
# 10. Programa Principal
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("  TRABALHO FINAL - HEURÍSTICAS")
    print("  O Problema do Caixeiro Viajante em Contextos Reais")
    print("  Percursos Turísticos em Portugal")
    print("=" * 70)

    # ------------------------------------------------------------------
    # A) Executar a heurística do vizinho mais próximo
    # ------------------------------------------------------------------
    print("\n>> A executar heuristica do Vizinho Mais Proximo...")
    percurso_nn, dist_nn = nearest_neighbor(pontos_turisticos, start=0)
    imprimir_percurso(pontos_turisticos, percurso_nn, dist_nn,
                      "PERCURSO - VIZINHO MAIS PRÓXIMO")

    # ------------------------------------------------------------------
    # B) Gerar soluções aleatórias para comparação
    # ------------------------------------------------------------------
    print(">> A gerar solucoes aleatorias para comparacao...")
    random.seed(42)
    num_aleatorias = 10
    distancias_aleatorias = []

    for i in range(num_aleatorias):
        _, dist_aleat = rota_aleatoria(pontos_turisticos, start=0)
        distancias_aleatorias.append(dist_aleat)

    media_aleatoria = sum(distancias_aleatorias) / len(distancias_aleatorias)
    melhor_aleatoria = min(distancias_aleatorias)
    pior_aleatoria = max(distancias_aleatorias)

    print(f"\n  Resultados de {num_aleatorias} rotas aleatorias:")
    print(f"    Media:  {media_aleatoria:.2f} km")
    print(f"    Melhor: {melhor_aleatoria:.2f} km")
    print(f"    Pior:   {pior_aleatoria:.2f} km")
    print(f"    NN:     {dist_nn:.2f} km")
    print(f"    Melhoria NN vs media aleatoria: {((media_aleatoria - dist_nn) / media_aleatoria) * 100:.1f}%\n")

    # ------------------------------------------------------------------
    # C) Aplicar melhoria 2-opt
    # ------------------------------------------------------------------
    print(">> A aplicar melhoria 2-opt ao percurso NN...")
    percurso_2opt, dist_2opt = two_opt(pontos_turisticos, percurso_nn)
    imprimir_percurso(pontos_turisticos, percurso_2opt, dist_2opt,
                      "PERCURSO - VIZINHO MAIS PRÓXIMO + 2-OPT")

    melhoria = ((dist_nn - dist_2opt) / dist_nn) * 100
    print(f"  Melhoria 2-opt sobre NN: {melhoria:.1f}%\n")

    # ------------------------------------------------------------------
    # D) Análise de clusters
    # ------------------------------------------------------------------
    print(">> Analise de clusters de pontos proximos (< 10 km):")
    clusters = analisar_clusters(pontos_turisticos)
    for idx_c, cluster in enumerate(clusters):
        nomes = [pontos_turisticos[i]["nome"] for i in cluster]
        print(f"  Cluster {idx_c + 1}: {', '.join(nomes)}")
    print()

    # ------------------------------------------------------------------
    # E) Criar mapas interativos
    # ------------------------------------------------------------------
    print(">> A criar mapas interativos com Folium...")

    criar_mapa(pontos_turisticos, percurso_nn,
               titulo=f"Vizinho Mais Próximo ({dist_nn:.0f} km)",
               nome_ficheiro="mapa_vizinho_mais_proximo.html")

    criar_mapa(pontos_turisticos, percurso_2opt,
               titulo=f"NN + 2-opt ({dist_2opt:.0f} km)",
               nome_ficheiro="mapa_2opt.html")

    # ------------------------------------------------------------------
    # F) Resumo comparativo
    # ------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("  RESUMO COMPARATIVO")
    print(f"{'=' * 70}")
    print(f"  {'Metodo':<35} {'Distancia (km)':>15}")
    print(f"  {'-' * 50}")
    print(f"  {'Vizinho Mais Proximo':<35} {dist_nn:>15.2f}")
    print(f"  {'NN + 2-opt':<35} {dist_2opt:>15.2f}")
    print(f"  {'Aleatoria (media de 10)':<35} {media_aleatoria:>15.2f}")
    print(f"  {'Aleatoria (melhor de 10)':<35} {melhor_aleatoria:>15.2f}")
    print(f"  {'Aleatoria (pior de 10)':<35} {pior_aleatoria:>15.2f}")
    print(f"  {'-' * 50}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
