from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import FileResponse
from typing import Optional
from datetime import datetime, date
import os
import tempfile
from services.reporte_service import ReporteService
from data.database_connection import DatabaseConnection

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def get_reporte_service():
    """Dependency para obtener instancia de ReporteService"""
    db_conn = DatabaseConnection()
    return ReporteService(connection=db_conn.get_connection())


@router.get("/cliente/{id_cliente}", response_class=FileResponse)
def generar_reporte_cliente(
    id_cliente: int,
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Genera un reporte PDF con todas las reservas de un cliente específico.
    
    - **id_cliente**: ID del cliente
    """
    # Crear archivo temporal para el PDF
    fd, temp_path = tempfile.mkstemp(suffix=".pdf", prefix=f"reservas_cliente_{id_cliente}_")
    os.close(fd)
    
    try:
        service.generar_reservas_por_cliente(temp_path, id_cliente)
        
        return FileResponse(
            path=temp_path,
            filename=f"reservas_cliente_{id_cliente}.pdf",
            media_type="application/pdf",
            background=None  # El archivo se eliminará automáticamente después de enviarlo
        )
    except Exception as e:
        # Limpiar el archivo temporal si hay un error
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el reporte: {str(e)}"
        )


@router.get("/cancha/{id_cancha}", response_class=FileResponse)
def generar_reporte_cancha(
    id_cancha: int,
    fecha_inicio: str = Query(..., description="Fecha inicio en formato YYYY-MM-DD"),
    fecha_fin: str = Query(..., description="Fecha fin en formato YYYY-MM-DD"),
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Genera un reporte PDF con las reservas de una cancha en un período determinado.
    
    - **id_cancha**: ID de la cancha
    - **fecha_inicio**: Fecha de inicio del período (formato YYYY-MM-DD)
    - **fecha_fin**: Fecha de fin del período (formato YYYY-MM-DD)
    """
    # Validar formato de fechas
    try:
        datetime.fromisoformat(fecha_inicio)
        datetime.fromisoformat(fecha_fin)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las fechas deben estar en formato YYYY-MM-DD"
        )
    
    # Crear archivo temporal para el PDF
    fd, temp_path = tempfile.mkstemp(suffix=".pdf", prefix=f"reservas_cancha_{id_cancha}_")
    os.close(fd)
    
    try:
        service.generar_reservas_por_cancha(temp_path, id_cancha, fecha_inicio, fecha_fin)
        
        return FileResponse(
            path=temp_path,
            filename=f"reservas_cancha_{id_cancha}_{fecha_inicio}_{fecha_fin}.pdf",
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el reporte: {str(e)}"
        )


@router.get("/canchas-mas-utilizadas", response_class=FileResponse)
def generar_reporte_canchas_mas_utilizadas(
    top_n: int = Query(10, description="Número de canchas a incluir en el reporte", ge=1, le=100),
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Genera un reporte PDF con las canchas más utilizadas.
    
    - **top_n**: Número de canchas a incluir (por defecto 10, máximo 100)
    """
    # Crear archivo temporal para el PDF
    fd, temp_path = tempfile.mkstemp(suffix=".pdf", prefix="canchas_mas_utilizadas_")
    os.close(fd)
    
    try:
        service.generar_canchas_mas_utilizadas(temp_path, top_n)
        
        return FileResponse(
            path=temp_path,
            filename=f"canchas_mas_utilizadas_top{top_n}.pdf",
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el reporte: {str(e)}"
        )


@router.get("/utilizacion-mensual", response_class=FileResponse)
def generar_reporte_utilizacion_mensual(
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Genera un reporte PDF con la utilización mensual de todas las canchas.
    Incluye un gráfico de barras con la cantidad de reservas por mes.
    """
    # Crear archivo temporal para el PDF
    fd, temp_path = tempfile.mkstemp(suffix=".pdf", prefix="utilizacion_mensual_")
    os.close(fd)
    
    try:
        service.generar_utilizacion_mensual(temp_path)
        
        return FileResponse(
            path=temp_path,
            filename="utilizacion_mensual.pdf",
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el reporte: {str(e)}"
        )


@router.get("/confirmacion/{id_reserva}")
def obtener_confirmacion_reserva(
    id_reserva: int,
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Obtiene un resumen completo de la confirmación de una reserva.
    
    - **id_reserva**: ID de la reserva
    
    Returns:
        JSON con toda la información de la reserva incluyendo cliente, items, pagos, etc.
    """
    try:
        confirmacion = service.obtener_confirmacion_reserva(id_reserva)
        return confirmacion
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener confirmación: {str(e)}"
        )


@router.get("/facturacion-mensual", response_class=FileResponse)
def generar_reporte_facturacion_mensual(
    anio: int = Query(None, description="Año para filtrar (por defecto año actual)"),
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Genera un PDF con la facturación mensual comparativa.
    
    - **anio**: Año específico para filtrar (opcional)
    """
    fd, temp_path = tempfile.mkstemp(suffix=".pdf", prefix="facturacion_mensual_")
    os.close(fd)
    
    try:
        service.generar_facturacion_mensual(temp_path, anio)
        
        anio_str = anio if anio else "actual"
        return FileResponse(
            path=temp_path,
            filename=f"facturacion_mensual_{anio_str}.pdf",
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el reporte: {str(e)}"
        )


@router.get("/utilizacion-por-cancha", response_class=FileResponse)
def generar_reporte_utilizacion_por_cancha(
    anio: int = Query(None, description="Año para filtrar (por defecto año actual)"),
    mes: int = Query(None, description="Mes para filtrar 1-12 (opcional)", ge=1, le=12),
    service: ReporteService = Depends(get_reporte_service)
):
    """
    Genera un PDF con la utilización comparativa por cancha.
    
    - **anio**: Año específico (opcional)
    - **mes**: Mes específico 1-12 (opcional, requiere año)
    """
    if mes is not None and anio is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Si especifica un mes, debe especificar también el año"
        )
    
    fd, temp_path = tempfile.mkstemp(suffix=".pdf", prefix="utilizacion_por_cancha_")
    os.close(fd)
    
    try:
        service.generar_utilizacion_por_cancha(temp_path, anio, mes)
        
        filename = "utilizacion_por_cancha"
        if anio:
            filename += f"_{anio}"
        if mes:
            filename += f"_{mes:02d}"
        filename += ".pdf"
        
        return FileResponse(
            path=temp_path,
            filename=filename,
            media_type="application/pdf",
            background=None
        )
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar el reporte: {str(e)}"
        )
