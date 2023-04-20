from pydantic import BaseModel


class BodyRequest(BaseModel):
    coordenadas: list
    cant_vehiculos: int
