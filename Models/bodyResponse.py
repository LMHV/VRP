from pydantic import BaseModel


class BodyResponse(BaseModel):
    rutasVehiculos: list
    distanciaTotal: float
    distanciaRutas: list
