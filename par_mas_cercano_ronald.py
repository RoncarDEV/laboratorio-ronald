import math
import time
import operator


def distancia(punto1, punto2):
    """
    Calcula la distancia euclidiana entre dos puntos.

    Parameters
    ----------
    punto1 : tuple
        Una tupla representando el primer punto (x, y).
    punto2 : tuple
        Una tupla representando el segundo punto (x, y).

    Returns
    -------
    float
        La distancia euclidiana entre los dos puntos.

    Notes
    -----
    Esta función utiliza la fórmula de la distancia euclidiana.

    References
    ----------
    .. [1] https://es.wikipedia.org/wiki/Distancia_euclidiana

    Examples
    --------
    >>> distancia((0, 0), (3, 4))
    5.0
    """
    return math.sqrt((punto2[0] - punto1[0]) ** 2 + (punto2[1] - punto1[1]) ** 2)

def fuerza_bruta(lista_pares):
    """
    Encuentra el par más cercano usando fuerza bruta.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de tuplas donde cada tupla representa un punto (x, y).

    Returns
    -------
    pares_cercanos : list of tuple
        Los dos puntos más cercanos.
    dis_minima : float
        La distancia mínima entre los dos puntos más cercanos.

    Examples
    --------
    >>> fuerza_bruta([(0, 0), (1, 1), (2, 2)])
    ([(0, 0), (1, 1)], 1.4142135623730951)
    """
    num_pares = len(lista_pares)
    dis_minima = math.inf
    pares_cercanos = []

    for i in range(num_pares):
        for j in range(i + 1, num_pares):
            dis_temporal = distancia(lista_pares[i], lista_pares[j])
            if dis_temporal < dis_minima:
                dis_minima = dis_temporal
                pares_cercanos = [lista_pares[i], lista_pares[j]]
    return pares_cercanos, dis_minima

def ordenar_lista(lista_pares, coordenada):
    """
    Ordena una lista de pares según la coordenada especificada.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de tuplas donde cada tupla representa un punto (x, y).
    coordenada : int
        Coordenada por la cual ordenar (0 para x, 1 para y).

    Returns
    -------
    list of tuple
        Lista ordenada de tuplas.

    Examples
    --------
    >>> ordenar_lista([(1, 3), (4, 2), (2, 1)], 0)
    [(1, 3), (2, 1), (4, 2)]
    """
    return sorted(lista_pares, key=operator.itemgetter(coordenada))

def par_mas_cercano_linea(lista_x, lista_y, dist):
    """
    Busca el par más cercano cruzando la línea que los divide.

    Parameters
    ----------
    lista_x : list of tuple
        Lista de tuplas ordenadas por coordenada x.
    lista_y : list of tuple
        Lista de tuplas ordenadas por coordenada y.
    dist : float
        Distancia mínima actual.

    Returns
    -------
    pares : list of tuple
        Los dos puntos más cercanos cruzando la línea divisoria.
    min_dist : float
        La distancia mínima entre los dos puntos más cercanos cruzando la línea divisoria.

    Notes
    -----
    Este método se utiliza como parte del algoritmo divide y conquista para encontrar el par más cercano.

    Examples
    --------
    >>> lista_x = [(1, 1), (2, 2), (3, 3)]
    >>> lista_y = [(1, 1), (2, 2), (3, 3)]
    >>> par_mas_cercano_linea(lista_x, lista_y, 1.0)
    ([], 1.0)
    """
    num_pares = len(lista_x)
    mitad = num_pares // 2
    punto_medio_x = lista_x[mitad][0]

    sub_lista_y = [punto1 for punto1 in lista_y if punto_medio_x - dist <= punto1[0] <= punto_medio_x + dist]
    min_dist = dist
    pares = []

    for i in range(len(sub_lista_y) - 1):
        for j in range(i + 1, min(i + 7, len(sub_lista_y))):
            punto1, punto2 = sub_lista_y[i], sub_lista_y[j]
            dist_pares = distancia(punto1, punto2)
            if dist_pares < min_dist:
                min_dist = dist_pares
                pares = [punto1, punto2]

    return pares, min_dist

def par_mas_cercano_rec(lista_x, lista_y):
    """
    Funcion recursiva que encuentra el par más cercano en la lista.

    Parameters
    ----------
    lista_x : list of tuple
        Lista de tuplas ordenadas por coordenada x.
    lista_y : list of tuple
        Lista de tuplas ordenadas por coordenada y.

    Returns
    -------
    pares : list of tuple
        Los dos puntos más cercanos.
    dist : float
        La distancia mínima entre los dos puntos más cercanos.

    Notes
    -----
    Este método implementa el algoritmo divide y conquista.

    Examples
    --------
    >>> lista_x = [(1, 1), (2, 2), (3, 3)]
    >>> lista_y = [(1, 1), (2, 2), (3, 3)]
    >>> par_mas_cercano_rec(lista_x, lista_y)
    ([(1, 1), (2, 2)], 1.4142135623730951)
    """
    num_pares = len(lista_x)
    if num_pares <= 3:
        return fuerza_bruta(lista_x)

    mitad = num_pares // 2
    lista_izq_x = lista_x[:mitad]
    lista_der_x = lista_x[mitad:]

    punto_medio_x = lista_x[mitad][0]
    lista_izq_y = [punto1 for punto1 in lista_y if punto1[0] <= punto_medio_x]
    lista_der_y = [punto1 for punto1 in lista_y if punto1[0] > punto_medio_x]
    pares_izq, dist_izq = par_mas_cercano_rec(lista_izq_x, lista_izq_y)
    pares_der, dist_der = par_mas_cercano_rec(lista_der_x, lista_der_y)    
    if dist_izq <= dist_der:
        dist = dist_izq
        pares = pares_izq
    else:
        dist = dist_der
        pares = pares_der
    pares_lin, dist_lin = par_mas_cercano_linea(lista_x, lista_y, dist)    
    if dist <= dist_lin:
        return pares, dist
    return pares_lin, dist_lin

def par_mas_cercano(lista_pares):
    """
    Encuentra el par más cercano en una lista de pares.

    Parameters
    ----------
    lista_pares : list of tuple
        Lista de tuplas donde cada tupla representa un punto (x, y).

    Returns
    -------
    pares : list of tuple
        Los dos puntos más cercanos.
    dist : float
        La distancia mínima entre los dos puntos más cercanos.

    Examples
    --------
    >>> lista_pares = [(1, 1), (2, 2), (3, 3)]
    >>> par_mas_cercano(lista_pares)
    ([(1, 1), (2, 2)], 1.4142135623730951)
    """
    lista_x = ordenar_lista(lista_pares, 0)
    lista_y = ordenar_lista(lista_x, 1)
    pares, dist = par_mas_cercano_rec(lista_x, lista_y)
    return pares, dist

# Lectura de datos
CARGAR_ARCHIVO = "datos_1000.txt"
with open(CARGAR_ARCHIVO, encoding='utf-8') as datos:
    x = datos.readline().split(",")
    y = datos.readline().split(",")

lista = [(int(x[i]), int(y[i])) for i in range(len(x))]

# Obtiene el par más cercano y la distancia. 
inicio1 = time.time()
pares, dist = par_mas_cercano(lista)
fin1 = time.time()    
inicio2 = time.time()
pares2, dist2 = fuerza_bruta(lista)
fin2 = time.time()

print(f"Los pares más cercanos son {pares[0]} y {pares[1]}.")
print(f"La distancia entre ellos es {dist:.3f}")
print(f"El tiempo de ejecución con la estrategia divide y conquista fue de {fin1 - inicio1:.3f} s.")
print(" ")
print(f"Los pares más cercanos son {pares2[0]} y {pares2[1]}.")
print(f"La distancia entre ellos es {dist2:.3f}")
print(f"El tiempo de búsqueda por fuerza bruta fue de {fin2 - inicio2:.3f} s.")
