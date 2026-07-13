import folium
import os

def criar_mapa(pontos, percurso, titulo="Percurso TSP", nome_ficheiro="percurso.html"):
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
