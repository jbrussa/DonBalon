from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import (
    cancha_controller,
    reserva_controller,
    cliente_controller,
    tipo_cancha_controller,
    estado_controller,
    horario_controller,
    servicio_controller,
    turno_controller,
    cancha_servicio_controller,
    equipo_controller,
    metodo_pago_controller,
    pago_controller,
    reserva_detalle_controller,
    tipo_pago_controller,
    torneo_controller,
)

# Crear la aplicación FastAPI
app = FastAPI(
    title="DonBalon API",
    description="API REST para el sistema de gestión de canchas deportivas DonBalon",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(cancha_controller.router)
app.include_router(reserva_controller.router)
app.include_router(cliente_controller.router)
app.include_router(tipo_cancha_controller.router)
app.include_router(estado_controller.router)
app.include_router(horario_controller.router)
app.include_router(servicio_controller.router)
app.include_router(turno_controller.router)
app.include_router(cancha_servicio_controller.router)
app.include_router(equipo_controller.router)
app.include_router(metodo_pago_controller.router)
app.include_router(pago_controller.router)
app.include_router(reserva_detalle_controller.router)
app.include_router(tipo_pago_controller.router)
app.include_router(torneo_controller.router)


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz de la API"""
    return {
        "message": "Bienvenido a DonBalon API",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
