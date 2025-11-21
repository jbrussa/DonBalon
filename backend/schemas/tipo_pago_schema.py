from pydantic import BaseModel, Field
from typing import Optional


class TipoPagoBase(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=200, description="Descripción del tipo de pago")


class TipoPagoCreate(TipoPagoBase):
    pass


class TipoPagoUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=200)


class TipoPagoResponse(TipoPagoBase):
    id_tipo_pago: int

    class Config:
        from_attributes = True
