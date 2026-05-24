# main.py
# Punto de entrada del sistema de navegación del campus UdeM.
# Inicializa el grafo y lanza el menú principal.

from grafo.campus_graph import CampusGraph
from ui.menu import menu_principal


def main():
    print("\n  Cargando sistema de navegación...")

    # Construir el grafo del campus con todos los datos
    grafo = CampusGraph()

    # Lanzar el menú principal
    menu_principal(grafo)


if __name__ == "__main__":
    main()