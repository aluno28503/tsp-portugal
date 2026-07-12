# Trabalho Final (Parte II) — O Problema do Caixeiro Viajante em Contextos Reais

## Questões de Reflexão

### 1. A solução obtida é necessariamente ótima? Justifique.

**Não**, a solução obtida pela heurística do Vizinho Mais Próximo **não é necessariamente ótima**.

A heurística do Vizinho Mais Próximo é uma heurística construtiva *greedy* (gulosa): em cada passo, escolhe o ponto não visitado mais próximo do ponto atual. Esta abordagem toma decisões localmente ótimas, mas **não garante a otimalidade global**. As razões são:

- **Visão míope (greedy):** A heurística não considera o impacto das decisões presentes nos passos futuros. Ao escolher sempre o ponto mais próximo, pode "encurralar-se" em regiões do mapa que depois obrigam a grandes deslocações.
- **Problema NP-difícil:** O TSP é um problema NP-difícil, o que significa que não existe algoritmo conhecido em tempo polinomial que garanta a solução ótima para instâncias genéricas. A solução ótima exigiria avaliar todas as $(n-1)!/2$ rotas possíveis (para 30 pontos, isto é da ordem de $10^{30}$).
- **Dependência do ponto de partida:** A solução do Vizinho Mais Próximo depende do ponto inicial escolhido. Começando num ponto diferente, o percurso final seria diferente e poderia ter uma distância total maior ou menor.

Na prática, a heurística NN tende a produzir soluções **razoáveis** (tipicamente 20-25% acima do ótimo), mas nunca com garantia de otimalidade.

---

### 2. Como se comporta a heurística quando existem clusters de pontos muito próximos?

A heurística do Vizinho Mais Próximo comporta-se **relativamente bem dentro de clusters**, mas pode ter **problemas na transição entre clusters**.

**Exemplo concreto do nosso conjunto de dados:**

Considere o cluster de Lisboa, composto por pontos que distam menos de 10 km entre si:
- Mosteiro dos Jerónimos (1)
- Torre de Belém (2)
- Castelo de São Jorge (19)
- Museu Nacional de Arte Antiga (20)
- Museu Nacional do Azulejo (21)
- Museu Nacional dos Coches (22)

**Comportamento observado:**
- **Dentro do cluster:** A heurística funciona bem porque, ao chegar a qualquer ponto do cluster, os restantes pontos do cluster são os mais próximos e são visitados sequencialmente. Isto é eficiente.
- **Problema entre clusters:** Quando a heurística termina de visitar um cluster, pode escolher o cluster errado para visitar a seguir. Por exemplo, depois de visitar o cluster de Lisboa, pode ir para Sintra (cluster próximo) em vez de Évora, forçando depois uma longa viagem ao sul e regresso ao norte.

Este comportamento resulta no fenómeno conhecido como **"crossing paths"** — o percurso cruza-se a si próprio, o que nunca acontece num percurso ótimo para TSP Euclideano.

---

### 3. Compare o percurso obtido com uma solução aleatória.

A heurística do Vizinho Mais Próximo é **significativamente mais eficiente** do que soluções aleatórias.

Os resultados do programa mostram que:
- O percurso NN é consistentemente **40-60% mais curto** do que a média das rotas aleatórias.
- Mesmo a **melhor** rota aleatória (entre 10 geradas) tende a ser bastante pior que o percurso NN.

**Justificação:**
- Uma rota aleatória não tem qualquer critério de otimização — visita os pontos numa ordem arbitrária, resultando em muitas viagens longas desnecessárias.
- A heurística NN, ao escolher sempre o vizinho mais próximo, evita a maioria das deslocações absurdamente longas, embora possa incorrer em ineficiências nas ligações finais.

A comparação demonstra que mesmo uma heurística simples como o NN oferece uma **melhoria substancial** face a abordagens não otimizadas.

---

### 4. Sugira melhorias ou heurísticas alternativas.

#### a) **2-opt** (implementada no código)
A heurística 2-opt é uma técnica de **melhoria local**: dado um percurso inicial, testa sistematicamente a inversão de segmentos do percurso. Se a inversão reduzir a distância total, a alteração é aceite. O processo repete-se até não haver mais melhorias possíveis.

**Vantagem:** Simples de implementar e tipicamente melhora o percurso NN em **5-15%**.

#### b) **3-opt e k-opt**
Extensões do 2-opt que consideram a remoção de 3 ou mais arestas em simultâneo. Produzem soluções melhores mas com custo computacional significativamente maior.

#### c) **Algoritmos genéticos**
Mantêm uma "população" de soluções que evoluem ao longo de gerações através de operadores de cruzamento e mutação. Bons para escapar de ótimos locais.

#### d) **Simulated Annealing (Arrefecimento Simulado)**
Aceita temporariamente soluções piores com uma probabilidade decrescente ao longo do tempo, permitindo explorar mais amplamente o espaço de soluções e escapar de ótimos locais.

#### e) **Ant Colony Optimization (Otimização por Colónia de Formigas)**
Algoritmo bio-inspirado que simula o comportamento de formigas a depositar feromonas. Particularmente eficaz em problemas de caminhos como o TSP.

#### f) **Branch and Bound / Programação inteira**
Para instâncias pequenas (como os 30 pontos deste problema), é possível encontrar a **solução ótima exata** usando técnicas de programação inteira, como o solver do PuLP ou OR-Tools do Google. A complexidade cresce exponencialmente, mas para 30 pontos é computacionalmente viável.
