import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância real (em km) entre dois pontos na superfície terrestre
    usando a fórmula de Haversine.
    """
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
