# grafo/campus_graph.py
# Clase principal del grafo del campus UdeM.
# Construye la estructura de datos (lista de adyacencia)
# y expone métodos para consultarla.

from grafo.data import VERTICES, ARISTAS


class CampusGraph:
    """
    Representa el campus como un grafo dirigido con pesos múltiples.
    Usa lista de adyacencia: cada nodo guarda una lista de sus vecinos.
    """

    def __init__(self):
        # ── Número total de vértices ──────────────────────────────────
        self.num_vertices = len(VERTICES)

        # ── Nombres de los vértices (id → nombre) ────────────────────
        self.nombres = VERTICES  # Ej: {0: "Entrada Principal", ...}

        # ── Lista de adyacencia ───────────────────────────────────────
        # Estructura: { id_nodo: [ {vecino, distancia, tiempo,
        #                           congestion, accesible, estado}, ... ] }
        self.adyacencia = {i: [] for i in range(self.num_vertices)}

        # Construir el grafo con los datos del campus
        self._construir_grafo()

    # ─────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN
    # ─────────────────────────────────────────────────────────────────

    def _construir_grafo(self):
        """
        Lee cada arista de ARISTAS y la agrega a la lista de adyacencia.
        Cada arista se guarda como un diccionario con todos sus atributos.
        """
        for arista in ARISTAS:
            origen, destino, distancia, tiempo, congestion, accesible, estado = arista

            # Crear el objeto que representa este camino
            camino = {
                "destino":    destino,
                "distancia":  distancia,   # metros
                "tiempo":     tiempo,      # minutos
                "congestion": congestion,  # 1 (baja) – 10 (alta)
                "accesible":  accesible,   # True / False
                "estado":     estado       # "disponible", "bloqueado", "en_mantenimiento"
            }

            # Agregar a la lista de adyacencia del nodo origen
            self.adyacencia[origen].append(camino)

    # ─────────────────────────────────────────────────────────────────
    # CONSULTAS
    # ─────────────────────────────────────────────────────────────────

    def obtener_vecinos(self, nodo, solo_accesibles=False):
        """
        Retorna los vecinos de un nodo filtrando:
          - SIEMPRE: caminos bloqueados o en mantenimiento (nunca se usan)
          - OPCIONAL: caminos no accesibles (cuando solo_accesibles=True)

        Parámetros:
            nodo            → ID del nodo del que queremos los vecinos
            solo_accesibles → Si True, solo retorna caminos accesibles

        Retorna:
            Lista de diccionarios con los caminos válidos
        """
        vecinos = []
        for camino in self.adyacencia[nodo]:

            # Filtro 1: ignorar caminos bloqueados o en mantenimiento
            if camino["estado"] in ("bloqueado", "en_mantenimiento"):
                continue

            # Filtro 2: si se requiere accesibilidad, ignorar no accesibles
            if solo_accesibles and not camino["accesible"]:
                continue

            vecinos.append(camino)
        return vecinos

    def obtener_nombre(self, id_nodo):
        """Retorna el nombre legible de un nodo por su ID."""
        return self.nombres.get(id_nodo, f"Nodo {id_nodo}")

    def obtener_todos_los_nodos(self):
        """Retorna la lista de todos los IDs de nodos del grafo."""
        return list(self.nombres.keys())

    def obtener_peso(self, camino, criterio):
        """
        Retorna el peso de un camino según el criterio seleccionado.
        Esto permite que Dijkstra sea genérico y funcione con
        cualquiera de los 4 criterios sin cambiar su lógica interna.

        Criterios:
            "distancia"  → peso = distancia en metros
            "tiempo"     → peso = tiempo en minutos
            "congestion" → peso = nivel de congestión (1-10)
            "accesible"  → peso = distancia (solo rutas accesibles,
                           el filtro ya fue aplicado en obtener_vecinos)
        """
        if criterio == "distancia":
            return camino["distancia"]
        elif criterio == "tiempo":
            return camino["tiempo"]
        elif criterio == "congestion":
            return camino["congestion"]
        elif criterio == "accesible":
            return camino["distancia"]  # Para accesibles, optimizamos distancia
        else:
            raise ValueError(f"Criterio desconocido: {criterio}")

    # ─────────────────────────────────────────────────────────────────
    # VISUALIZACIÓN
    # ─────────────────────────────────────────────────────────────────

    def mostrar_grafo(self):
        """
        Imprime en consola toda la lista de adyacencia del grafo,
        mostrando cada nodo y sus caminos con todos los atributos.
        Útil para verificar que el grafo se construyó correctamente.
        """
        print("\n" + "═" * 60)
        print("   GRAFO DEL CAMPUS UdeM — Lista de Adyacencia")
        print("═" * 60)

        for nodo, caminos in self.adyacencia.items():
            print(f"\n📍 {self.obtener_nombre(nodo)} (ID: {nodo})")

            if not caminos:
                print("   └── Sin conexiones")
                continue

            for i, c in enumerate(caminos):
                conector = "├──" if i < len(caminos) - 1 else "└──"
                accesible_str = "♿ Sí" if c["accesible"] else "✖ No"
                estado_icono = {
                    "disponible":      "✅",
                    "bloqueado":       "🔴",
                    "en_mantenimiento":"🟡"
                }.get(c["estado"], "❓")

                print(
                    f"   {conector} → {self.obtener_nombre(c['destino']):<30} "
                    f"| {c['distancia']:>4}m "
                    f"| {c['tiempo']:>2}min "
                    f"| Cong:{c['congestion']:>2} "
                    f"| {accesible_str} "
                    f"| {estado_icono} {c['estado']}"
                )

        print("\n" + "═" * 60)
        print(f"  Total: {self.num_vertices} vértices | {len(ARISTAS)} aristas")
        print("═" * 60 + "\n")