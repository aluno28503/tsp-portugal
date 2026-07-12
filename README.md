# TSP Portugal — Percursos Turísticos

Trabalho Final (Parte II) — Heurísticas: O Problema do Caixeiro Viajante em Contextos Reais.

Implementação em Python da heurística do **Vizinho Mais Próximo** (Nearest Neighbor) para otimização de percursos turísticos em Portugal, incluindo locais UNESCO, castelos e museus.

## Autores

- **Rodrigo Andrade** — aluno28503
- **Eric Cardoso** — aluno20518

## Funcionalidades

- **30 pontos turísticos** reais de Portugal com coordenadas geográficas
- **Fórmula de Haversine** para cálculo de distâncias reais
- **Heurística do Vizinho Mais Próximo** (Nearest Neighbor)
- **Melhoria 2-opt** aplicada ao percurso
- **Comparação com rotas aleatórias**
- **Análise de clusters** de pontos próximos
- **Mapas interativos** com Folium

## Resultados

| Método | Distância (km) |
|---|---:|
| Vizinho Mais Próximo | 1 301 |
| NN + 2-opt | 1 164 |
| Aleatória (média de 10) | 4 645 |

- A heurística NN é **72% melhor** que a média de rotas aleatórias.
- O 2-opt melhora o percurso NN em **10.6%**.

## Como executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python pontos_turisticos.py
```

O programa gera:
- Percurso detalhado na consola com distâncias entre cada par de pontos
- `mapa_vizinho_mais_proximo.html` — mapa interativo do percurso NN
- `mapa_2opt.html` — mapa interativo do percurso melhorado com 2-opt

## Estrutura do projeto

```
├── pontos_turisticos.py    # Código principal
├── analise_reflexao.md     # Respostas às questões de reflexão
├── requirements.txt        # Dependências
└── README.md               # Este ficheiro
```

## Questões de reflexão

As respostas detalhadas às 4 questões de reflexão encontram-se em [`analise_reflexao.md`](analise_reflexao.md):

1. A solução obtida é necessariamente ótima?
2. Como se comporta a heurística com clusters de pontos próximos?
3. Comparação com soluções aleatórias
4. Melhorias e heurísticas alternativas (2-opt, algoritmos genéticos, etc.)
