import os
import sqlite3
import tempfile
from datetime import datetime
from typing import Optional
from repositories.turno_repository import TurnoRepository
from repositories.reserva_detalle_repository import ReservaDetalleRepository
from repositories.reserva_repository import ReservaRepository
from repositories.cancha_repository import CanchaRepository
from repositories.cliente_repository import ClienteRepository
from repositories.base_repository import BaseRepository
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


class ReporteService:
    """Servicio para la generación de reportes en PDF"""
    
    def __init__(self, db_path: Optional[str] = None, connection: Optional[sqlite3.Connection] = None):
        self.turno_repo = TurnoRepository(db_path, connection)
        self.detalle_repo = ReservaDetalleRepository(db_path, connection)
        self.reserva_repo = ReservaRepository(db_path, connection)
        self.cancha_repo = CanchaRepository(db_path, connection)
        self.cliente_repo = ClienteRepository(db_path, connection)
        self.base_repo = BaseRepository(db_path, connection)
    
    @staticmethod
    def _ensure_dir(d: str):
        """Crea el directorio si no existe"""
        if not os.path.exists(d):
            os.makedirs(d)
    
    @staticmethod
    def _save_chart_to_png(fig) -> str:
        """Guarda una figura matplotlib en un archivo PNG temporal y devuelve la ruta."""
        fd, path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        import matplotlib.pyplot as plt
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        return path
    
    @staticmethod
    def _build_pdf(path: str, title: str, elements: list):
        """Construye un PDF en `path` con los elementos Platypus dados."""
        doc = SimpleDocTemplate(path, pagesize=A4)
        styles = getSampleStyleSheet()
        header = Paragraph(title, styles["Title"])
        story = [header, Spacer(1, 12)]
        story.extend(elements)
        doc.build(story)
    
    @staticmethod
    def _make_table(data, col_widths=None):
        """Crea un Table estilizada para reportlab a partir de una lista de filas."""
        table = Table(data, colWidths=col_widths)
        style = [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]
        table.setStyle(style)
        return table
    
    @staticmethod
    def _make_image_element(image_path, width=None, height=None):
        """Crea un elemento Image para reportlab"""
        img = Image(image_path)
        if width:
            img.drawWidth = width
        if height:
            img.drawHeight = height
        try:
            img.hAlign = 'CENTER'
        except Exception:
            pass
        return img
    
    def generar_reservas_por_cliente(self, output_path: str, id_cliente: int):
        """Genera un PDF con las reservas de un cliente específico.

        Args:
            output_path: Ruta del PDF de salida.
            id_cliente: Id del cliente cuyas reservas se desean listar.
        """
        cliente = self.cliente_repo.get_by_id(id_cliente)

        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph(f"Listado de reservas - Cliente id={id_cliente}", styles["Heading2"]))

        if not cliente:
            elements.append(Paragraph("Cliente no encontrado.", styles["Normal"]))
            self._build_pdf(output_path, f"Reservas por Cliente {id_cliente}", elements)
            return

        header = Paragraph(f"Cliente: {cliente.nombre} {cliente.apellido} (id={cliente.id_cliente})", styles["Heading4"])
        elements.append(header)

        reservas = self.reserva_repo.get_by_cliente(cliente.id_cliente)
        if not reservas:
            elements.append(Paragraph("No tiene reservas.", styles["Normal"]))
            elements.append(Spacer(1, 8))
            self._build_pdf(output_path, f"Reservas por Cliente {cliente.nombre} {cliente.apellido}", elements)
            return

        table_data = [["ID Reserva", "Fecha", "Monto", "Estado", "Detalle (Cancha - Fecha - Horario)"]]
        for r in reservas:
            detalles = self.detalle_repo.get_by_reserva(r.id_reserva)
            detalle_texts = []
            for d in detalles:
                turno = self.turno_repo.get_by_id(d.id_turno)
                cancha = self.cancha_repo.get_by_id(turno.id_cancha) if turno else None
                detalle_texts.append(f"{cancha.nombre if cancha else 'N/A'} - {turno.fecha if turno else 'N/A'} - turno:{turno.id_horario if turno else 'N/A'}")
            table_data.append([
                str(r.id_reserva),
                str(r.fecha_reserva),
                str(r.monto_total),
                str(r.estado_nombre),
                "\n".join(detalle_texts),
            ])

        elements.append(self._make_table(table_data))
        elements.append(Spacer(1, 12))

        self._build_pdf(output_path, f"Reservas por Cliente {cliente.nombre} {cliente.apellido}", elements)

    def generar_canchas_mas_utilizadas(self, output_path: str, top_n: int = 10):
        """Genera un PDF con las canchas más utilizadas.
        
        Args:
            output_path: Ruta del PDF de salida.
            top_n: Número de canchas a incluir en el reporte.
        """
        sql = (
            "SELECT t.id_cancha as id_cancha, c.nombre as nombre, COUNT(rd.id_detalle) as usos "
            "FROM ReservaDetalle rd "
            "JOIN Turno t ON rd.id_turno = t.id_turno "
            "JOIN Cancha c ON t.id_cancha = c.id_cancha "
            "GROUP BY t.id_cancha ORDER BY usos DESC"
        )
        rows = self.base_repo.query_all(sql)

        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Canchas más utilizadas", styles["Heading2"]))

        table_data = [["ID Cancha", "Nombre", "Usos"]]
        count = 0
        for r in rows:
            if count >= top_n:
                break
            table_data.append([str(r["id_cancha"]), r["nombre"], str(r["usos"])])
            count += 1

        elements.append(self._make_table(table_data))
        elements.append(Spacer(1, 12))
        self._build_pdf(output_path, "Canchas más utilizadas", elements)

    def generar_utilizacion_mensual(self, output_path: str):
        """Genera un PDF con la utilización mensual de canchas.
        
        Args:
            output_path: Ruta del PDF de salida.
        """
        sql = (
            "SELECT strftime('%Y-%m', t.fecha) as mes, COUNT(rd.id_detalle) as usos "
            "FROM ReservaDetalle rd "
            "JOIN Turno t ON rd.id_turno = t.id_turno "
            "GROUP BY mes ORDER BY mes"
        )
        rows = self.base_repo.query_all(sql)

        meses = [r["mes"] for r in rows]
        usos = [r["usos"] for r in rows]

        styles = getSampleStyleSheet()
        titulo = "Utilización mensual de canchas"
        elements = [Paragraph(titulo, styles["Heading2"]), Spacer(1, 12)]

        # Intentar crear gráfico; si falla, generar una tabla con los datos
        try:
            import matplotlib.pyplot as plt

            # Calcular ancho usable en puntos para A4, dejar márgenes
            page_width_pts, _ = A4
            usable_width_pts = page_width_pts - 2 * 36  # 0.5" margen cada lado

            # Gráfico más pequeño (70% del ancho usable)
            target_width_pts = usable_width_pts * 0.70

            # Crear figura con ancho en pulgadas equivalente
            fig_width_in = target_width_pts / 72
            fig_height_in = 2.5
            fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))
            ax.bar(meses, usos, color="tab:blue")
            ax.set_title(titulo)
            ax.set_xlabel("Mes")
            ax.set_ylabel("Cantidad de usos")
            plt.xticks(rotation=45)

            img_path = self._save_chart_to_png(fig)
            elements.append(Spacer(1, 12))
            elements.append(self._make_image_element(img_path, width=target_width_pts))
            elements.append(Spacer(1, 12))

        except Exception as e:
            # Fallback: tabla con los datos
            elements.append(Paragraph("No se pudo generar el gráfico por un problema con la librería de gráficos.", styles["Normal"]))
            elements.append(Paragraph(f"Error: {str(e)}", styles["Normal"]))
            table_data = [["Mes", "Usos"]]
            for r in rows:
                table_data.append([r["mes"], str(r["usos"])])
            elements.append(self._make_table(table_data))

        self._build_pdf(output_path, titulo, elements)

    def generar_reservas_por_cancha(self, output_path: str, id_cancha: int, fecha_inicio: str, fecha_fin: str):
        """Genera un PDF con las reservas de una cancha en un período.

        Args:
            output_path: Ruta del PDF de salida.
            id_cancha: Id de la cancha.
            fecha_inicio: Fecha inicio en formato YYYY-MM-DD.
            fecha_fin: Fecha fin en formato YYYY-MM-DD.
        """
        inicio = datetime.fromisoformat(fecha_inicio).date()
        fin = datetime.fromisoformat(fecha_fin).date()

        turnos = self.turno_repo.get_by_cancha(id_cancha)
        turnos_periodo = [t for t in turnos if inicio <= datetime.fromisoformat(str(t.fecha)).date() <= fin]

        elements = []
        styles = getSampleStyleSheet()
        cancha = self.cancha_repo.get_by_id(id_cancha)
        nombre_cancha = cancha.nombre if cancha else f"Cancha {id_cancha}"
        elements.append(Paragraph(f"Reservas para {nombre_cancha} desde {fecha_inicio} hasta {fecha_fin}", styles["Heading2"]))

        table_data = [["ID Reserva", "Fecha Turno", "ID Turno", "Cliente", "Monto Item"]]
        for t in turnos_periodo:
            detalles = self.detalle_repo.get_by_turno(t.id_turno)
            for d in detalles:
                reserva = self.reserva_repo.get_by_id(d.id_reserva)
                cliente = self.cliente_repo.get_by_id(reserva.id_cliente) if reserva else None
                table_data.append([
                    str(d.id_reserva),
                    str(t.fecha),
                    str(t.id_turno),
                    f"{cliente.nombre} {cliente.apellido}" if cliente else "N/A",
                    str(d.precio_total_item),
                ])

        elements.append(self._make_table(table_data))
        elements.append(Spacer(1, 12))

        self._build_pdf(output_path, f"Reservas por Cancha {nombre_cancha}", elements)
