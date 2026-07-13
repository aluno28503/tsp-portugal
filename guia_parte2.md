# Guia Completo — Trabalho Final Parte II
## O Problema do Caixeiro Viajante (TSP) em Portugal

Este guia foi criado para te ajudar a perceber exatamente como o teu projeto está organizado e como funciona cada algoritmo. Assim, se o professor te fizer perguntas, tens aqui todas as respostas!

---

## 🗂️ A Organização do Projeto (Modularização)

Dividimos o código gigante em **6 ficheiros mais pequenos**. Isto mostra ao professor que sabes organizar código como um programador profissional:

1. **`pontos.py`**: Apenas guarda a tabela de dados (a lista de 30 pontos turísticos, com as respetivas latitudes e longitudes).
2. **`haversine.py`**: Tem a fórmula matemática para calcular distâncias reais em quilómetros com base nas coordenadas da Terra.
3. **`tsp.py`**: O "cérebro" do projeto. Aqui estão os algoritmos que calculam a melhor rota (Vizinho Mais Próximo e 2-opt).
4. **`mapa.py`**: Responsável por desenhar o mapa interativo usando a biblioteca gráfica *Folium*.
5. **`main.py`**: O ficheiro maestro. É o único que precisas de executar. Ele importa as peças todas dos outros ficheiros e faz o programa funcionar do início ao fim.
6. **`Respostas.txt`**: Um resumo escrito com as distâncias finais e conclusões do trabalho.

---

## 🧮 A Fórmula de Haversine

Para sabermos a distância entre dois locais (ex: Santarém e Sintra), não podemos usar uma simples régua porque a Terra é redonda. 
A fórmula de **Haversine** (que implementámos no `haversine.py`) resolve isto usando trigonometria. Recebe as latitudes e longitudes de dois pontos e, assumindo que o raio da Terra é 6371 km, devolve a distância exata "em linha reta" por cima da superfície da Terra.

---

## 🤖 Os Algoritmos Usados

O **TSP** (Problema do Caixeiro Viajante) tenta encontrar o caminho mais curto para visitar todos os pontos e voltar ao início. No nosso caso, visitar 30 locais turísticos a começar e acabar em Santarém.

### 1. Vizinho Mais Próximo (Nearest Neighbor - NN)
É a heurística mais básica e instintiva.
- **Como funciona:** Começa em Santarém. O algoritmo pergunta "Qual é o local mais próximo que ainda não visitei?". Vai para lá. E repete o processo até acabar.
- **Resultado:** Deu-nos uma rota de **1301 km**.
- **O Problema:** Como ele não planeia o futuro, chega ao fim e sobram-lhe pontos muito distantes uns dos outros (ex: Bragança e Évora). Isto obriga-o a dar grandes saltos cruzados no mapa.

### 2. Melhoria 2-opt
O 2-opt é um corretor. Ele não constrói um percurso do zero, pega no percurso do Vizinho Mais Próximo e "passa-o a ferro".
- **Como funciona:** O algoritmo varre o mapa à procura de linhas que se cruzem (em forma de "X"). Quando encontra um cruzamento, ele inverte a ordem de visitação nesse segmento para "desatar o nó", fazendo com que as linhas deixem de se cruzar.
- **Resultado:** Conseguiu baixar a distância para **1163 km**! Uma melhoria brutal de quase 11%, formando um percurso "redondo" à volta de Portugal.

### 3. Solução Aleatória (Apenas para Comparação)
Para provar ao professor que a nossa inteligência artificial é boa, pusemos o computador a gerar 10 rotas completamente aleatórias ("ao calhas").
- **Resultado:** A média das rotas aleatórias foi **4644 km**. Isto prova que a nossa solução de 1163 km é incrivelmente eficiente (poupámos mais de 3000 km!).

---

## 🔍 Análise de Clusters

Um "Cluster" é apenas um agrupamento de pontos que estão muito colados uns aos outros.
No nosso código (no ficheiro `tsp.py`), mandámos o programa encontrar pontos que estivessem a **menos de 10 km de distância**.
- **Para que serve?** Se fôssemos uma empresa de turismo, podíamos vender "pacotes" (ex: Pacote Sintra, Pacote Lisboa, Pacote Guimarães) porque sabemos que esses monumentos se podem visitar todos a pé no mesmo dia, já que pertencem ao mesmo cluster.

---

## 🗺️ O Mapa Interativo (Folium)

No fim de fazer os cálculos, o `main.py` chama a biblioteca *Folium*.
Esta biblioteca pega nas coordenadas GPS e constrói um ficheiro chamado `percurso.html`.
- O ponto de partida (Santarém) fica marcado com uma bolinha **Verde**.
- Todos os outros locais a visitar têm uma bolinha **Vermelha**.
- O percurso otimizado é desenhado com uma linha Azul que une todos os pontos sem fazer grandes cruzamentos, graças ao nosso amigo 2-opt!
