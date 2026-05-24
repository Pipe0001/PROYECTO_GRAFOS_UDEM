from grafo.campus_graph import CampusGraph
from algoritmos.mst import prim, explicar_mst

g = CampusGraph()

resultado = prim(g, inicio=0)
print(explicar_mst(resultado, g))