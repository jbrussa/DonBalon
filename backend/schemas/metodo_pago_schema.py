from pydantic import BaseModel, Field
from typing import Optional


class MetodoPagoBase(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=200, description="Descripción del método de pago")


class MetodoPagoCreate(MetodoPagoBase):
    pass


class MetodoPagoUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=200)


class MetodoPagoResponse(MetodoPagoBase):
    id_metodo_pago: int

    class Config:
        from_attributes = True
