from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from Models.bodyRequest import *


def create_model(body: BodyRequest):
    """Crea los datos del problema."""

    data = {}
    # Define la matriz de distancia
    data['distance_matrix'] = body.matriz_distancia

    """
    [
        [0, 3678, 5377, 6513],
        [3791, 0, 4607, 3758],
        [5592, 5522, 0, 2058],
        [6674, 4130, 2058, 0]
    ]
    """
    # Define la cantidad de vehículos
    data['num_vehicles'] = body.cant_vehiculos
    # Define la posición del depósito
    data['depot'] = 0

    return data


def print_solution(data, manager, routing, solution):
    """Imprime la solución en la consola."""
    total_route_distance = 0  # Calculamos la distancia total recorrida por los vehiculos
    rutas = []
    distanciaRutas = []

    for vehicle_id in range(data['num_vehicles']):

        index = routing.Start(vehicle_id)  # Calcular la ruta
        plan_output = 'Ruta del vehículo {}:\n'.format(vehicle_id)
        route_distance = 0  # Calcula distancia recorrida por cada vehiculo
        destinosVehiculos = []

        while not routing.IsEnd(index):
            destinosVehiculos.append(manager.IndexToNode(index))
            # Coloca los indices en el string que se va a imprimir
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index  # El indice actual ahora para a ser el previo
            # Calcula el siguiente indice a imprimir
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)  # Suma a distancia recorrida desde el indice previo al actual

        destinosVehiculos.append(0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distancia de la ruta: {}m\n'.format(route_distance)

        print(destinosVehiculos)
        print(plan_output)
        # Suma distancia del vehiculo actual a la distancia total
        total_route_distance += route_distance
        rutas.append(destinosVehiculos)
        distanciaRutas.append(route_distance)

    print(rutas)
    print('Distancia total de todos los vehículos: {}m'.format(total_route_distance))
    return (rutas, total_route_distance, distanciaRutas)
