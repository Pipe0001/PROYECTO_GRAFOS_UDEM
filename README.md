# 🗺️ Sistema de Navegación — Campus UdeM
## Práctica de Grafos — Estructuras de Datos

Sistema de navegación del campus universitario UdeM implementado
en Python, que permite calcular rutas eficientes entre lugares
usando algoritmos de grafos.

---

## 📋 Descripción del Proyecto

El campus está modelado como un **grafo dirigido con pesos múltiples**
donde cada lugar es un vértice y cada camino es una arista con 5 atributos:

- 📏 Distancia en metros
- ⏱️ Tiempo estimado en minutos
- 🚦 Nivel de congestión (1 al 10)
- ♿ Accesibilidad para movilidad reducida
- 🚧 Estado: disponible, bloqueado o en mantenimiento

### Funcionalidades
- **Dijkstra con 4 criterios**: distancia, tiempo, congestión y accesibilidad
- **Árbol de Expansión Mínima (Prim)**: recorrido completo para visitantes
- Filtrado automático de caminos bloqueados o en mantenimiento

---

## 🏗️ Estructura del Proyecto

proyecto_grafos_udem/
├── main.py                  → Punto de entrada
├── README.md
├── grafo/
│   ├── campus_graph.py      → Clase del grafo (lista de adyacencia)
│   └── data.py              → Datos del campus (15 nodos, 55 aristas)
├── algoritmos/
│   ├── dijkstra.py          → Dijkstra con múltiples criterios
│   └── mst.py               → Árbol de Expansión Mínima (Prim)
└── ui/
└── menu.py              → Interfaz de consola


---

## ▶️ Cómo ejecutar el proyecto

### Requisitos
- Python 3.8 o superior
- No requiere librerías externas

### Pasos
```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd proyecto_grafos_udem

# 2. Ejecutar el sistema
python main.py
```

### Opciones del menú
| Opción | Descripción |
|--------|-------------|
| 1 | Buscar ruta entre dos lugares |
| 2 | Recorrido completo para visitantes (MST) |
| 3 | Ver mapa completo del campus |
| 4 | Salir |

---

## 📐 Supuestos asumidos

1. **Grafo dirigido**: cada camino se define en ambas direcciones
   de forma independiente, pudiendo tener atributos diferentes.

2. **Caminos no disponibles**: los caminos con estado `bloqueado`
   o `en_mantenimiento` son ignorados completamente por todos
   los algoritmos.

3. **Criterio accesible**: para rutas de movilidad reducida,
   se optimiza la distancia pero solo usando caminos accesibles.

4. **MST sin restricciones**: el recorrido para visitantes no
   aplica filtro de accesibilidad, tal como indica el enunciado.

5. **Pesos positivos**: todos los pesos (distancia, tiempo,
   congestión) son valores positivos, condición requerida
   por Dijkstra.

6. **Grafo conexo**: se asume que el campus es navegable,
   es decir, existe al menos un camino disponible entre
   cualquier par de nodos.

---


---

## 📚 Algoritmos implementados

### Dijkstra
Algoritmo de camino más corto con complejidad **O((V + E) log V)**
usando cola de prioridad (min-heap). Adaptado para soportar
múltiples criterios de peso mediante el método `obtener_peso()`.

### Prim (MST)
Algoritmo de árbol de expansión mínima con complejidad
**O(E log V)**. Conecta los 15 nodos del campus con la
menor distancia total posible (1790 metros).
