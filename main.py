import sys
import random
from pontos import pontos_turisticos
from tsp import nearest_neighbor, rota_aleatoria, two_opt, analisar_clusters, calcular_matriz_distancias
from mapa import criar_mapa

# Garantir codificação UTF-8 na consola (Windows)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

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

def main():
    print("\n" + "=" * 70)
    print("  TRABALHO FINAL - HEURÍSTICAS")
    print("  O Problema do Caixeiro Viajante em Contextos Reais")
    print("=" * 70)

    # A) Executar a heurística do vizinho mais próximo
    print("\n>> A executar heuristica do Vizinho Mais Proximo...")
    percurso_nn, dist_nn = nearest_neighbor(pontos_turisticos, start=0)
    imprimir_percurso(pontos_turisticos, percurso_nn, dist_nn, "PERCURSO - VIZINHO MAIS PRÓXIMO")

    # B) Gerar soluções aleatórias para comparação
    print(">> A gerar solucoes aleatorias para comparacao...")
    random.seed(42)
    num_aleatorias = 10
    distancias_aleatorias = []
    melhor_percurso_aleat = None

    for i in range(num_aleatorias):
        perc_aleat, dist_aleat = rota_aleatoria(pontos_turisticos, start=0)
        distancias_aleatorias.append(dist_aleat)
        # Guardar o melhor percurso aleatório para desenhar no mapa
        if melhor_percurso_aleat is None or dist_aleat < min(distancias_aleatorias[:-1] + [float('inf')]):
            melhor_percurso_aleat = perc_aleat

    media_aleatoria = sum(distancias_aleatorias) / len(distancias_aleatorias)
    melhor_aleatoria = min(distancias_aleatorias)

    print(">> A criar mapa interativo (Rota Aleatória)...")
    criar_mapa(pontos_turisticos, melhor_percurso_aleat,
               titulo=f"Melhor Rota Aleatória ({melhor_aleatoria:.0f} km)",
               nome_ficheiro="mapa_aleatorio.html")

    # C) Aplicar melhoria 2-opt
    print(">> A aplicar melhoria 2-opt ao percurso NN...")
    percurso_2opt, dist_2opt = two_opt(pontos_turisticos, percurso_nn)
    imprimir_percurso(pontos_turisticos, percurso_2opt, dist_2opt, "PERCURSO - VIZINHO MAIS PRÓXIMO + 2-OPT")

    # D) Análise de clusters
    print(">> Analise de clusters de pontos proximos (< 10 km):")
    clusters = analisar_clusters(pontos_turisticos)
    for idx_c, cluster in enumerate(clusters):
        nomes = [pontos_turisticos[i]["nome"] for i in cluster]
        print(f"  Cluster {idx_c + 1}: {', '.join(nomes)}")
    print()

    # E) Criar mapas interativos
    print(">> A criar mapa interativo (2-opt)...")
    criar_mapa(pontos_turisticos, percurso_2opt,
               titulo=f"Percurso TSP ({dist_2opt:.0f} km)",
               nome_ficheiro="percurso.html")

    # F) Resumo comparativo
    print(f"\n{'=' * 70}")
    print("  RESUMO COMPARATIVO")
    print(f"{'=' * 70}")
    print(f"  {'Metodo':<35} {'Distancia (km)':>15}")
    print(f"  {'-' * 50}")
    print(f"  {'Vizinho Mais Proximo':<35} {dist_nn:>15.2f}")
    print(f"  {'NN + 2-opt':<35} {dist_2opt:>15.2f}")
    print(f"  {'Aleatoria (media de 10)':<35} {media_aleatoria:>15.2f}")
    print(f"  {'Aleatoria (melhor de 10)':<35} {melhor_aleatoria:>15.2f}")
    print(f"  {'-' * 50}")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    main()
