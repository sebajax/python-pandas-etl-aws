"""
pydantic schemas definition for process
"""
from pydantic import BaseModel, Field


class BatchProcessSchema(BaseModel):
    Cod: str = Field(min_length=1)
    Fecha: int = Field(gt=0)
    Tipo: str = Field(min_length=1)
    Marca: str = Field(min_length=1)
    Modelo: str | None = None
    Version: str | None = None
    Puertas: str | None = None
    Combustible: str | None = None
    Transmision: str | None = None
    Marchas: str | None = None
    Traccion: str | None = None
    Pais: str | None = None
    Tasacion: float = Field(gt=0)
    Permiso: float = Field(gt=0)
