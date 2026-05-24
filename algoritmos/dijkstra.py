# algoritmos/dijkstra.py
# Implementación de Dijkstra adaptado para el campus UdeM.
# Soporta 4 criterios de búsqueda y filtra caminos no disponibles.

import heapq  # Cola de prioridad (min-heap) — estructura clave de Dijkstra


def dijkstra(grafo, origen, destino, criterio):
    """
    Calcula la ruta óptima entre dos nodos usando el algoritmo de Dijkstra.

    Parámetros:
        grafo    → instancia de CampusGraph
        origen   → ID del nodo de inicio
        destino  → ID del nodo de llegada
        criterio → "distancia" | "tiempo" | "congestion" | "accesible"

    Retorna un diccionario con:
        {
          "encontrada": True/False,
          "ruta":       [id0, id1, id2, ...],
          "costo":      valor total del criterio,
          "detalle":    [ {de, hacia, peso}, ... ]  ← cada tramo de la ruta
        }
    """

    # ── ¿El criterio requiere solo caminos accesibles? ────────────────
    solo_accesibles = (criterio == "accesible")

    # ── Inicialización ────────────────────────────────────────────────
    # distancias[i] = costo mínimo conocido para llegar al nodo i
    # Arrancamos con infinito para todos los nodos excepto el origen
    INF = float("inf")
    distancias = {nodo: INF for nodo in grafo.obtener_todos_los_nodos()}
    distancias[origen] = 0

    # anteriores[i] = nodo previo en la ruta óptima hacia i
    # Nos sirve para reconstruir el camino al final
    anteriores = {nodo: None for nodo in grafo.obtener_todos_los_nodos()}

    # Cola de prioridad: tuplas (costo_acumulado, nodo_actual)
    # heapq siempre saca el elemento con menor costo primero
    cola = [(0, origen)]

    # Conjunto de nodos ya procesados (visitados)
    visitados = set()

    # ── Algoritmo principal ───────────────────────────────────────────
    while cola:
        costo_actual, nodo_actual = heapq.heappop(cola)

        # Si ya procesamos este nodo, lo saltamos
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        # Si llegamos al destino, podemos parar (optimización)
        if nodo_actual == destino:
            break

        # Explorar vecinos del nodo actual
        # obtener_vecinos ya filtra bloqueados/mantenimiento y accesibles
        vecinos = grafo.obtener_vecinos(nodo_actual, solo_accesibles)

        for camino in vecinos:
            vecino = camino["destino"]

            if vecino in visitados:
                continue

            # Calcular el nuevo costo acumulado hasta este vecino
            peso = grafo.obtener_peso(camino, criterio)
            nuevo_costo = costo_actual + peso

            # Si encontramos un camino mejor, actualizamos
            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                anteriores[vecino] = nodo_actual
                heapq.heappush(cola, (nuevo_costo, vecino))

    # ── Reconstruir la ruta ───────────────────────────────────────────
    if distancias[destino] == INF:
        # No se encontró ruta posible
        return {"encontrada": False, "ruta": [], "costo": INF, "detalle": []}

    # Recorrer hacia atrás desde destino hasta origen
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = anteriores[nodo]
    ruta.reverse()  # Voltear para que vaya de origen → destino

    # Construir detalle tramo por tramo
    detalle = _construir_detalle(grafo, ruta, criterio, solo_accesibles)

    return {
        "encontrada": True,
        "ruta":       ruta,
        "costo":      distancias[destino],
        "detalle":    detalle
    }


def _construir_detalle(grafo, ruta, criterio, solo_accesibles):
    """
    Construye la lista de tramos de la ruta con info de cada camino.
    Ej: Entrada Principal → Bloque A | 120m | 2min | Cong:8
    """
    detalle = []
    for i in range(len(ruta) - 1):
        nodo_de    = ruta[i]
        nodo_hacia = ruta[i + 1]

        # Buscar el camino exacto entre estos dos nodos
        vecinos = grafo.obtener_vecinos(nodo_de, solo_accesibles)
        for camino in vecinos:
            if camino["destino"] == nodo_hacia:
                detalle.append({
                    "de":         grafo.obtener_nombre(nodo_de),
                    "hacia":      grafo.obtener_nombre(nodo_hacia),
                    "distancia":  camino["distancia"],
                    "tiempo":     camino["tiempo"],
                    "congestion": camino["congestion"],
                    "accesible":  camino["accesible"],
                    "peso":       grafo.obtener_peso(camino, criterio)
                })
                break
    return detalle


def explicar_ruta(resultado, criterio, grafo):
    """
    Genera una explicación en texto de por qué se eligió esta ruta.
    Cumple el requisito: 'mostrar explicación básica de por qué
    esa ruta fue seleccionada'.
    """
    if not resultado["encontrada"]:
        return "❌ No se encontró una ruta válida con los criterios seleccionados."

    # Textos descriptivos por criterio
    descripciones = {
        "distancia":  ("distancia total en metros",   "metros",  "más corta"),
        "tiempo":     ("tiempo total en minutos",      "minutos", "más rápida"),
        "congestion": ("nivel de congestión acumulado","puntos",  "menos congestionada"),
        "accesible":  ("distancia total (ruta accesible)", "metros", "más corta accesible"),
    }
    desc, unidad, adj = descripciones[criterio]

    nodos_str = " → ".join(
        [grafo.obtener_nombre(n) for n in resultado["ruta"]]
    )

    explicacion = (
        f"\n💡 EXPLICACIÓN DE LA RUTA SELECCIONADA\n"
        f"{'─' * 50}\n"
        f"Se eligió la ruta {adj} según el criterio de {desc}.\n"
        f"De todas las rutas posibles entre el origen y el destino,\n"
        f"esta es la que acumula el menor valor de {desc}.\n\n"
        f"Caminos bloqueados o en mantenimiento fueron ignorados\n"
        f"automáticamente durante la búsqueda.\n"
    )

    if criterio == "accesible":
        explicacion += (
            f"Además, solo se consideraron caminos con acceso\n"
            f"para personas con movilidad reducida (♿).\n"
        )

    explicacion += (
        f"\nRuta encontrada:\n  {nodos_str}\n"
        f"Costo total: {resultado['costo']} {unidad}\n"
    )

    return explicacion