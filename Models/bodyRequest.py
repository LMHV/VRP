from pydantic import BaseModel


class BodyRequest(BaseModel):
    matriz_distancia: list
    cant_vehiculos: int
