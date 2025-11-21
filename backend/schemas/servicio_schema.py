from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ServicioBase(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=200, description="Descripción del servicio")
    costoxservicio: Decimal = Field(..., description="Costo del servicio")


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=200)
    costoxservicio: Optional[Decimal] = None


class ServicioResponse(ServicioBase):
    id_servicio: int

    class Config:
        from_attributes = True
