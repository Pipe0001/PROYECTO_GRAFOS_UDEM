# algoritmos/mst.py
# Algoritmo de Prim para el Árbol de Expansión Mínima (MST).
# Encuentra el recorrido que conecta todos los lugares del campus
# con la menor distancia total, sin restricciones de movilidad.

import heapq  # Cola de prioridad (min-heap)


def prim(grafo, inicio=0):
    """
    Construye el Árbol de Expansión Mínima del campus usando Prim.
    Criterio fijo: menor distancia (requisito del proyecto para visitantes).
    Sin filtro de accesibilidad (visitantes sin restricciones).

    Parámetros:
        grafo  → instancia de CampusGraph
        inicio → ID del nodo desde donde arranca el recorrido (default: 0)

    Retorna un diccionario con:
        {
          "encontrado":     True/False,
          "aristas_mst":    [ {de, hacia, distancia}, ... ],
          "costo_total":    suma de distancias del MST,
          "nodos_visitados": [id0, id1, ...]  ← orden de visita
        }
    """

    todos_los_nodos = set(grafo.obtener_todos_los_nodos())
    visitados       = set()        # Nodos ya incluidos en el MST
    aristas_mst     = []           # Aristas elegidas para el MST
    nodos_visitados = [inicio]     # Orden en que se visitan los nodos
    costo_total     = 0

    # Cola de prioridad: (distancia, nodo_origen, nodo_destino)
    visitados.add(inicio)

    # Agregar a la cola todos los vecinos del nodo inicial
    cola = []
    for camino in grafo.obtener_vecinos(inicio, solo_accesibles=False):
        heapq.heappush(cola, (
            camino["distancia"],
            inicio,
            camino["destino"]
        ))

    # ── Algoritmo de Prim ─────────────────────────────────────────────
    while cola and len(visitados) < len(todos_los_nodos):
        distancia, nodo_de, nodo_hacia = heapq.heappop(cola)

        # Si el destino ya está en el MST, ignorar (evita ciclos)
        if nodo_hacia in visitados:
            continue

        # Agregar este nodo al MST
        visitados.add(nodo_hacia)
        nodos_visitados.append(nodo_hacia)
        costo_total += distancia

        # Registrar la arista elegida
        aristas_mst.append({
            "de":        nodo_de,
            "hacia":     nodo_hacia,
            "distancia": distancia,
            "de_nombre":    grafo.obtener_nombre(nodo_de),
            "hacia_nombre": grafo.obtener_nombre(nodo_hacia)
        })

        # Agregar a la cola los vecinos del nuevo nodo
        for camino in grafo.obtener_vecinos(nodo_hacia, solo_accesibles=False):
            if camino["destino"] not in visitados:
                heapq.heappush(cola, (
                    camino["distancia"],
                    nodo_hacia,
                    camino["destino"]
                ))

    # ── Verificar que se conectaron todos los nodos ───────────────────
    if len(visitados) < len(todos_los_nodos):
        nodos_faltantes = todos_los_nodos - visitados
        return {
            "encontrado":      False,
            "aristas_mst":     aristas_mst,
            "costo_total":     costo_total,
            "nodos_visitados": nodos_visitados,
            "nodos_faltantes": nodos_faltantes
        }

    return {
        "encontrado":      True,
        "aristas_mst":     aristas_mst,
        "costo_total":     costo_total,
        "nodos_visitados": nodos_visitados
    }


def explicar_mst(resultado, grafo):
    """
    Genera la explicación del recorrido para visitantes.
    Muestra cada conexión del árbol y el costo total.
    """
    if not resultado["encontrado"]:
        faltantes = resultado.get("nodos_faltantes", set())
        nombres = [grafo.obtener_nombre(n) for n in faltantes]
        return (
            f"⚠️  El MST no pudo conectar todos los nodos.\n"
            f"Nodos no alcanzados: {', '.join(nombres)}\n"
            f"Verifica que el grafo sea conexo."
        )

    lineas = [
        "\n🌳 RECORRIDO PARA VISITANTES — Árbol de Expansión Mínima",
        "─" * 55,
        "Conecta todos los lugares del campus con la menor",
        "distancia total posible (algoritmo de Prim).",
        "─" * 55,
        f"  Nodo inicial: {grafo.obtener_nombre(resultado['nodos_visitados'][0])}",
        "",
        "  Conexiones del árbol:"
    ]

    for i, arista in enumerate(resultado["aristas_mst"]):
        conector = "├──" if i < len(resultado["aristas_mst"]) - 1 else "└──"
        lineas.append(
            f"  {conector} {arista['de_nombre']:<30} → "
            f"{arista['hacia_nombre']:<30} | {arista['distancia']}m"
        )

    lineas += [
        "",
        "─" * 55,
        f"  📍 Orden de visita:",
    ]

    orden = " → ".join([
        grafo.obtener_nombre(n) for n in resultado["nodos_visitados"]
    ])
    # Partir en líneas de máximo 60 chars para que se vea bien en consola
    palabras = orden.split(" → ")
    linea_actual = "  "
    for p in palabras:
        if len(linea_actual) + len(p) > 58:
            lineas.append(linea_actual.rstrip(" →"))
            linea_actual = "    → " + p + " → "
        else:
            linea_actual += p + " → "
    lineas.append(linea_actual.rstrip(" →"))

    lineas += [
        "",
        f"  💰 Distancia total del recorrido: {resultado['costo_total']} metros",
        f"  🏫 Lugares conectados: {len(resultado['nodos_visitados'])} de {grafo.num_vertices}",
        "─" * 55,
    ]

    return "\n".join(lineas)