# ui/menu.py
# Maneja toda la interfaz de consola del sistema.
# Muestra menús, recibe entradas del usuario y presenta resultados.

from algoritmos.dijkstra import dijkstra, explicar_ruta
from algoritmos.mst import prim, explicar_mst


# ─────────────────────────────────────────────────────────────────────
# UTILIDADES DE CONSOLA
# ─────────────────────────────────────────────────────────────────────

def limpiar():
    """Imprime líneas en blanco para simular limpieza de pantalla."""
    print("\n" * 2)


def titulo(texto):
    """Imprime un título destacado."""
    print("\n" + "═" * 60)
    print(f"   {texto}")
    print("═" * 60)


def separador():
    print("─" * 60)


# ─────────────────────────────────────────────────────────────────────
# MOSTRAR LISTA DE LUGARES
# ─────────────────────────────────────────────────────────────────────

def mostrar_lugares(grafo):
    """
    Imprime la lista numerada de todos los lugares del campus.
    El usuario escoge origen y destino por ID.
    """
    titulo("LUGARES DEL CAMPUS UdeM")
    for id_nodo, nombre in grafo.nombres.items():
        print(f"  [{id_nodo:>2}]  {nombre}")
    separador()


# ─────────────────────────────────────────────────────────────────────
# PEDIR ORIGEN Y DESTINO
# ─────────────────────────────────────────────────────────────────────

def pedir_nodo(grafo, mensaje):
    """
    Pide al usuario que ingrese un ID de nodo válido.
    Repite hasta que el usuario ingrese un valor correcto.
    """
    while True:
        try:
            valor = int(input(f"\n  {mensaje}: "))
            if valor in grafo.nombres:
                return valor
            else:
                print(f"  ⚠️  ID inválido. Ingresa un número entre "
                      f"0 y {grafo.num_vertices - 1}.")
        except ValueError:
            print("  ⚠️  Debes ingresar un número entero.")


# ─────────────────────────────────────────────────────────────────────
# MENÚ DE CRITERIOS DE BÚSQUEDA
# ─────────────────────────────────────────────────────────────────────

def mostrar_criterios():
    """Muestra las opciones de criterio de búsqueda para Dijkstra."""
    titulo("CRITERIO DE BÚSQUEDA")
    print("  [1]  📏  Ruta más corta por distancia")
    print("  [2]  ⏱️   Ruta más rápida por tiempo")
    print("  [3]  🚦  Ruta con menor congestión")
    print("  [4]  ♿  Ruta accesible para movilidad reducida")
    separador()


def pedir_criterio():
    """
    Pide al usuario que seleccione un criterio.
    Retorna el string que usa el sistema internamente.
    """
    MAPA_CRITERIOS = {
        "1": "distancia",
        "2": "tiempo",
        "3": "congestion",
        "4": "accesible"
    }
    while True:
        opcion = input("  Selecciona una opción [1-4]: ").strip()
        if opcion in MAPA_CRITERIOS:
            return MAPA_CRITERIOS[opcion]
        print("  ⚠️  Opción inválida. Ingresa 1, 2, 3 o 4.")


# ─────────────────────────────────────────────────────────────────────
# MOSTRAR RESULTADO DE DIJKSTRA
# ─────────────────────────────────────────────────────────────────────

def mostrar_resultado_dijkstra(resultado, criterio, grafo):
    """
    Imprime el resultado completo de una búsqueda Dijkstra:
    - Tramos de la ruta con sus atributos
    - Costo total
    - Explicación de por qué se eligió esta ruta
    """
    if not resultado["encontrada"]:
        print("\n  ❌ No se encontró una ruta válida.")
        print("  Puede que todos los caminos estén bloqueados,")
        print("  en mantenimiento, o no sean accesibles.\n")
        return

    titulo("RUTA ENCONTRADA")

    # Etiquetas por criterio
    ETIQUETAS = {
        "distancia":  ("📏 Distancia", "m"),
        "tiempo":     ("⏱️  Tiempo",    "min"),
        "congestion": ("🚦 Congestión", "pts"),
        "accesible":  ("♿ Distancia accesible", "m"),
    }
    etiqueta, unidad = ETIQUETAS[criterio]

    # Mostrar cada tramo
    print(f"\n  {'DESDE':<30} {'HACIA':<30} {etiqueta}")
    separador()

    for tramo in resultado["detalle"]:
        print(
            f"  {tramo['de']:<30} "
            f"{tramo['hacia']:<30} "
            f"{tramo['peso']} {unidad}"
        )

    separador()
    print(f"  💰 Costo total: {resultado['costo']} {unidad}")

    # Ruta resumida
    ruta_str = " → ".join([grafo.obtener_nombre(n) for n in resultado["ruta"]])
    print(f"\n  📍 Ruta: {ruta_str}")

    # Explicación
    print(explicar_ruta(resultado, criterio, grafo))


# ─────────────────────────────────────────────────────────────────────
# FLUJO COMPLETO: BUSCAR RUTA
# ─────────────────────────────────────────────────────────────────────

def flujo_buscar_ruta(grafo):
    """
    Maneja el flujo completo cuando el usuario quiere buscar una ruta:
    1. Mostrar lugares
    2. Pedir origen y destino
    3. Pedir criterio
    4. Ejecutar Dijkstra
    5. Mostrar resultado
    """
    mostrar_lugares(grafo)
    origen  = pedir_nodo(grafo, "Ingresa el ID del lugar de ORIGEN")

    # Validar que destino sea diferente al origen
    while True:
        destino = pedir_nodo(grafo, "Ingresa el ID del lugar de DESTINO")
        if destino != origen:
            break
        print("  ⚠️  El destino debe ser diferente al origen.")

    mostrar_criterios()
    criterio = pedir_criterio()

    print("\n  🔍 Calculando ruta óptima...")
    resultado = dijkstra(grafo, origen, destino, criterio)
    mostrar_resultado_dijkstra(resultado, criterio, grafo)


# ─────────────────────────────────────────────────────────────────────
# FLUJO COMPLETO: RECORRIDO VISITANTES (MST)
# ─────────────────────────────────────────────────────────────────────

def flujo_recorrido_visitantes(grafo):
    """
    Maneja el flujo del recorrido para visitantes usando MST (Prim).
    Pregunta desde qué lugar quieren iniciar el recorrido.
    """
    titulo("RECORRIDO PARA VISITANTES")
    print("  Visita todos los lugares del campus con la menor")
    print("  distancia total posible.\n")

    mostrar_lugares(grafo)
    inicio = pedir_nodo(grafo, "Ingresa el ID del lugar de INICIO del recorrido")

    print("\n  🌳 Calculando recorrido óptimo...")
    resultado = prim(grafo, inicio)
    print(explicar_mst(resultado, grafo))


# ─────────────────────────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────────────

def menu_principal(grafo):
    """
    Bucle principal del programa.
    Muestra el menú y despacha al flujo correspondiente.
    """
    while True:
        limpiar()
        titulo("SISTEMA DE NAVEGACIÓN — CAMPUS UdeM")
        print("  [1]  🗺️   Buscar ruta entre dos lugares")
        print("  [2]  🌳  Recorrido completo para visitantes (MST)")
        print("  [3]  📋  Ver mapa completo del campus")
        print("  [4]  🚪  Salir")
        separador()

        opcion = input("  Selecciona una opción [1-4]: ").strip()

        if opcion == "1":
            flujo_buscar_ruta(grafo)
            input("\n  Presiona ENTER para volver al menú...")

        elif opcion == "2":
            flujo_recorrido_visitantes(grafo)
            input("\n  Presiona ENTER para volver al menú...")

        elif opcion == "3":
            grafo.mostrar_grafo()
            input("\n  Presiona ENTER para volver al menú...")

        elif opcion == "4":
            titulo("¡Hasta luego!")
            print("  Sistema de Navegación UdeM cerrado.\n")
            break

        else:
            print("  ⚠️  Opción inválida. Ingresa 1, 2, 3 o 4.")
            input("  Presiona ENTER para continuar...")