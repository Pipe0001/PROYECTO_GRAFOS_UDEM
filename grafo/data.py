# grafo/data.py
# Define los datos del campus UdeM:
# - Los vértices (lugares del campus)
# - Las aristas (caminos entre lugares) con sus 5 atributos

# ─────────────────────────────────────────
# VÉRTICES — Lugares del campus (15 en total)
# Cada lugar tiene un ID (número) y un nombre
# ─────────────────────────────────────────
VERTICES = {
    0:  "Entrada Principal",
    1:  "Bloque A (Aulas)",
    2:  "Bloque B (Aulas)",
    3:  "Bloque C (Aulas)",
    4:  "Laboratorios",
    5:  "Biblioteca",
    6:  "Cafetería",
    7:  "Parqueadero Norte",
    8:  "Parqueadero Sur",
    9:  "Teatro",
    10: "Enfermería",
    11: "Zona Deportiva",
    12: "Oficinas Administrativas",
    13: "Capilla",
    14: "Bienestar Universitario",
}

# ─────────────────────────────────────────
# ARISTAS — Caminos entre lugares
# Formato de cada arista (tupla):
#   (origen, destino, distancia_m, tiempo_min, congestion, accesible, estado)
#
# Atributos:
#   origen        → ID del vértice de inicio
#   destino       → ID del vértice de llegada
#   distancia_m   → Distancia en metros (peso numérico)
#   tiempo_min    → Tiempo en minutos (peso numérico)
#   congestion    → Nivel de congestión del 1 (baja) al 10 (alta)
#   accesible     → True si permite movilidad reducida, False si no
#   estado        → "disponible", "bloqueado" o "en_mantenimiento"
# ─────────────────────────────────────────
ARISTAS = [
    # (origen, destino, distancia, tiempo, congestion, accesible, estado)

    # Desde Entrada Principal (0)
    (0, 1,  120, 2, 8, True,  "disponible"),        # → Bloque A
    (0, 7,  200, 3, 4, True,  "disponible"),        # → Parqueadero Norte
    (0, 12, 150, 2, 5, True,  "disponible"),        # → Oficinas Administrativas

    # Desde Bloque A (1)
    (1, 0,  120, 2, 8, True,  "disponible"),        # → Entrada Principal
    (1, 2,   80, 1, 6, True,  "disponible"),        # → Bloque B
    (1, 5,  200, 3, 3, True,  "disponible"),        # → Biblioteca
    (1, 6,  180, 3, 7, True,  "disponible"),        # → Cafetería
    (1, 10,  90, 2, 2, True,  "disponible"),        # → Enfermería

    # Desde Bloque B (2)
    (2, 1,   80, 1, 6, True,  "disponible"),        # → Bloque A
    (2, 3,   70, 1, 4, False, "disponible"),        # → Bloque C (sin rampa)
    (2, 4,  130, 2, 5, True,  "disponible"),        # → Laboratorios
    (2, 6,  160, 2, 6, True,  "en_mantenimiento"), # → Cafetería (en mantenimiento)

    # Desde Bloque C (3)
    (3, 2,   70, 1, 4, False, "disponible"),        # → Bloque B
    (3, 4,  100, 2, 3, False, "disponible"),        # → Laboratorios
    (3, 9,  250, 4, 2, False, "disponible"),        # → Teatro
    (3, 11, 300, 5, 2, False, "disponible"),        # → Zona Deportiva

    # Desde Laboratorios (4)
    (4, 2,  130, 2, 5, True,  "disponible"),        # → Bloque B
    (4, 3,  100, 2, 3, False, "disponible"),        # → Bloque C
    (4, 5,  170, 3, 4, True,  "disponible"),        # → Biblioteca
    (4, 14, 220, 3, 2, True,  "disponible"),        # → Bienestar

    # Desde Biblioteca (5)
    (5, 1,  200, 3, 3, True,  "disponible"),        # → Bloque A
    (5, 4,  170, 3, 4, True,  "disponible"),        # → Laboratorios
    (5, 6,  140, 2, 5, True,  "disponible"),        # → Cafetería
    (5, 12, 180, 3, 3, True,  "disponible"),        # → Oficinas Admón.

    # Desde Cafetería (6)
    (6, 1,  180, 3, 7, True,  "disponible"),        # → Bloque A
    (6, 5,  140, 2, 5, True,  "disponible"),        # → Biblioteca
    (6, 9,  200, 3, 6, True,  "disponible"),        # → Teatro
    (6, 11, 250, 4, 5, True,  "disponible"),        # → Zona Deportiva
    (6, 14, 130, 2, 4, True,  "disponible"),        # → Bienestar

    # Desde Parqueadero Norte (7)
    (7, 0,  200, 3, 4, True,  "disponible"),        # → Entrada Principal
    (7, 8,  350, 5, 2, True,  "bloqueado"),         # → Parqueadero Sur (bloqueado)
    (7, 12, 180, 3, 3, True,  "disponible"),        # → Oficinas Admón.

    # Desde Parqueadero Sur (8)
    (8, 7,  350, 5, 2, True,  "bloqueado"),         # → Parqueadero Norte (bloqueado)
    (8, 11, 150, 2, 2, False, "disponible"),        # → Zona Deportiva
    (8, 13, 200, 3, 1, True,  "disponible"),        # → Capilla

    # Desde Teatro (9)
    (9, 3,  250, 4, 2, False, "disponible"),        # → Bloque C
    (9, 6,  200, 3, 6, True,  "disponible"),        # → Cafetería
    (9, 13, 120, 2, 1, True,  "disponible"),        # → Capilla

    # Desde Enfermería (10)
    (10, 1,  90, 2, 2, True,  "disponible"),        # → Bloque A
    (10, 12,110, 2, 3, True,  "disponible"),        # → Oficinas Admón.
    (10, 14,140, 2, 2, True,  "disponible"),        # → Bienestar

    # Desde Zona Deportiva (11)
    (11, 3,  300, 5, 2, False, "disponible"),       # → Bloque C
    (11, 6,  250, 4, 5, True,  "disponible"),       # → Cafetería
    (11, 8,  150, 2, 2, False, "disponible"),       # → Parqueadero Sur

    # Desde Oficinas Administrativas (12)
    (12, 0,  150, 2, 5, True,  "disponible"),       # → Entrada Principal
    (12, 5,  180, 3, 3, True,  "disponible"),       # → Biblioteca
    (12, 7,  180, 3, 3, True,  "disponible"),       # → Parqueadero Norte
    (12, 10, 110, 2, 3, True,  "disponible"),       # → Enfermería

    # Desde Capilla (13)
    (13, 8,  200, 3, 1, True,  "disponible"),       # → Parqueadero Sur
    (13, 9,  120, 2, 1, True,  "disponible"),       # → Teatro
    (13, 14, 160, 2, 1, True,  "disponible"),       # → Bienestar

    # Desde Bienestar Universitario (14)
    (14, 4,  220, 3, 2, True,  "disponible"),       # → Laboratorios
    (14, 6,  130, 2, 4, True,  "disponible"),       # → Cafetería
    (14, 10, 140, 2, 2, True,  "disponible"),       # → Enfermería
    (14, 13, 160, 2, 1, True,  "disponible"),       # → Capilla
]