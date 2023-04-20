from fastapi import FastAPI
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from problema_google import *
from Models.bodyRequest import *
from Models.bodyResponse import *

# Entry point a la API
app = FastAPI()

"""
@app.get('/coordenadas')
async def root():
    return {'example': 'Hola', 'data': 1}
"""


@app.post("/resolve")
async def resolve_problem(body: BodyRequest):

    # Crea los datos del problema
    data = create_model(body)

    # Crea el administrador de nodos con toda la data ingresada
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Crea el enrutador el cual se encarga de hacer los calculos
    routing = pywrapcp.RoutingModel(manager)

    # Retorna la distancia entre los dos nodos.
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Definir costo de cada arco
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Añadir restrcción de distancia
    dimension_name = 'Distance'
    routing.AddDimension(transit_callback_index, 0,
                         50000, True, dimension_name)  # Restriccion de 50km recorribles por cada auto
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    # Coeficiente de costo en 100, segun entendi de la documentacion, si está en 100 es como que no hay perdida de eficienca de los kilometros recorridos, es decir, puede recorrer todos los kilometros que se le pusieron como restriccion.
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Configura la estrategia de búsqueda heurística
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)  # Calcula la distancia con la estrategia de arcos mas cortos.

    # Resuelve el problema
    # Resuelve el problema con los parametros colocados arriba
    solution = routing.SolveWithParameters(search_parameters)

    # Imprime la solución
    if solution:
        newData = print_solution(data, manager, routing, solution)
    else:
        print('No se encontró solución')

    return BodyResponse(rutasVehiculos=newData[0], distanciaTotal=newData[1], distanciaRutas=newData[2])
