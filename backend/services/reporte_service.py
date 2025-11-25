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
from repositories.pago_repository import PagoRepository
from repositories.horario_repository import HorarioRepository
from repositories.metodo_pago_repository import MetodoPagoRepository
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table
from reportlab.platypus import Image as RLImage
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
        self.pago_repo = PagoRepository(db_path, connection)
        self.horario_repo = HorarioRepository(db_path, connection)
        self.metodo_pago_repo = MetodoPagoRepository(db_path, connection)
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
        img = RLImage(image_path)
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

    def obtener_confirmacion_reserva(self, id_reserva: int) -> dict:
        """Obtiene un resumen completo de la confirmación de una reserva.
        
        Args:
            id_reserva: ID de la reserva a confirmar
            
        Returns:
            dict con toda la información de la reserva para mostrar al usuario
        """
        # Obtener reserva
        reserva = self.reserva_repo.get_by_id(id_reserva)
        if not reserva:
            raise ValueError(f"Reserva con ID {id_reserva} no encontrada")
        
        # Obtener cliente
        cliente = self.cliente_repo.get_by_id(reserva.id_cliente)
        
        # Obtener pago
        pagos = self.pago_repo.get_all()
        pago = next((p for p in pagos if p.id_reserva == id_reserva), None)
        metodo_pago = None
        if pago:
            metodo_pago = self.metodo_pago_repo.get_by_id(pago.id_metodo_pago)
        
        # Obtener detalles de la reserva
        detalles = self.detalle_repo.get_by_reserva(id_reserva)
        items_detalle = []
        
        for detalle in detalles:
            turno = self.turno_repo.get_by_id(detalle.id_turno)
            if turno:
                cancha = self.cancha_repo.get_by_id(turno.id_cancha)
                horario = self.horario_repo.get_by_id(turno.id_horario)
                
                items_detalle.append({
                    "id_detalle": detalle.id_detalle,
                    "cancha_nombre": cancha.nombre if cancha else "N/A",
                    "fecha": str(turno.fecha),
                    "horario": f"{horario.hora_inicio} - {horario.hora_fin}" if horario else "N/A",
                    "precio": str(detalle.precio_total_item)
                })
        
        # Construir respuesta
        return {
            "id_reserva": reserva.id_reserva,
            "fecha_reserva": str(reserva.fecha_reserva),
            "estado": reserva.estado_nombre,
            "monto_total": str(reserva.monto_total),
            "cliente": {
                "nombre": f"{cliente.nombre} {cliente.apellido}" if cliente else "N/A",
                "mail": cliente.mail if cliente else "N/A",
                "telefono": cliente.telefono if cliente else "N/A"
            },
            "metodo_pago": metodo_pago.descripcion if metodo_pago else "N/A",
            "fecha_pago": str(pago.fecha_pago) if pago else str(reserva.fecha_reserva),
            "items": items_detalle
        }

    def generar_facturacion_mensual(self, output_path: str, anio: int = None):
        """Genera un PDF con la facturación mensual comparativa.
        
        Args:
            output_path: Ruta del PDF de salida.
            anio: Año específico para filtrar (opcional). Si no se provee, usa el año actual.
        """
        from datetime import datetime
        
        if anio is None:
            anio = datetime.now().year
        
        # Obtener facturación por mes (solo reservas Pagadas o Finalizadas)
        sql = (
            "SELECT strftime('%Y-%m', r.fecha_reserva) as mes, "
            "SUM(r.monto_total) as facturacion, "
            "COUNT(r.id_reserva) as cantidad_reservas "
            "FROM Reserva r "
            "WHERE (LOWER(r.estado_reserva) = 'pagada' OR LOWER(r.estado_reserva) = 'finalizada') "
            "AND strftime('%Y', r.fecha_reserva) = ? "
            "GROUP BY mes ORDER BY mes"
        )
        
        try:
            rows = self.base_repo.conn.execute(sql, (str(anio),)).fetchall()
            rows = [dict(row) for row in rows]
        except Exception as e:
            # Si hay error en la consulta, generar PDF con mensaje de error
            styles = getSampleStyleSheet()
            titulo = f"Facturación Mensual - Año {anio}"
            elements = [Paragraph(titulo, styles["Heading2"]), Spacer(1, 12)]
            elements.append(Paragraph(f"Error al consultar datos: {str(e)}", styles["Normal"]))
            self._build_pdf(output_path, titulo, elements)
            return
        
        styles = getSampleStyleSheet()
        titulo = f"Facturación Mensual - Año {anio}"
        elements = [Paragraph(titulo, styles["Heading2"]), Spacer(1, 12)]
        
        # Verificar si hay datos
        if not rows or len(rows) == 0:
            elements.append(Paragraph(f"No hay datos de facturación para el año {anio}.", styles["Normal"]))
            self._build_pdf(output_path, titulo, elements)
            return
        
        meses = [r["mes"] for r in rows]
        facturacion = [float(r["facturacion"]) for r in rows]
        
        # Tabla resumen
        table_data = [["Mes", "Facturación ($)", "Cantidad Reservas"]]
        total_facturacion = 0
        total_reservas = 0
        
        for r in rows:
            table_data.append([
                r["mes"],
                f"${float(r['facturacion']):.2f}",
                str(r["cantidad_reservas"])
            ])
            total_facturacion += float(r["facturacion"])
            total_reservas += r["cantidad_reservas"]
        
        table_data.append(["TOTAL", f"${total_facturacion:.2f}", str(total_reservas)])
        elements.append(self._make_table(table_data))
        elements.append(Spacer(1, 12))
        
        # Gráfico comparativo
        try:
            import matplotlib.pyplot as plt
            
            page_width_pts, _ = A4
            usable_width_pts = page_width_pts - 2 * 36
            target_width_pts = usable_width_pts * 0.60  # Reducido de 0.75 a 0.60
            
            fig_width_in = target_width_pts / 72
            fig_height_in = 3  # Reducido de 4 a 3
            
            fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))
            
            # Gráfico de barras
            x = list(range(len(meses)))
            ax.bar(x, facturacion, color="tab:green", alpha=0.7)
            ax.set_title("Facturación Mensual Comparativa")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Facturación ($)")
            ax.set_xticks(x)
            ax.set_xticklabels(meses, rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)
            
            # Línea de tendencia
            if len(facturacion) > 1:
                import numpy as np
                z = np.polyfit(x, facturacion, 1)
                p = np.poly1d(z)
                ax.plot(x, p(x), "r--", alpha=0.6, label="Tendencia")
                ax.legend()
            
            plt.tight_layout()
            
            img_path = self._save_chart_to_png(fig)
            elements.append(self._make_image_element(img_path, width=target_width_pts))
            elements.append(Spacer(1, 12))
            
        except Exception as e:
            elements.append(Paragraph(f"No se pudo generar el gráfico: {str(e)}", styles["Normal"]))
        
        self._build_pdf(output_path, titulo, elements)

    def generar_utilizacion_por_cancha(self, output_path: str, anio: int = None, mes: int = None):
        """Genera un PDF con la utilización comparativa por cancha.
        
        Args:
            output_path: Ruta del PDF de salida.
            anio: Año específico (opcional)
            mes: Mes específico 1-12 (opcional, requiere año)
        """
        from datetime import datetime
        
        if anio is None:
            anio = datetime.now().year
        
        # Construir filtro de fecha para el JOIN
        fecha_condition = "strftime('%Y', t.fecha) = ?"
        params = [str(anio)]
        
        if mes is not None:
            fecha_condition += " AND strftime('%m', t.fecha) = ?"
            params.append(f"{mes:02d}")
        
        # Obtener utilización por cancha
        # Contar turnos ocupados (no disponibles) por cancha
        sql = (
            f"SELECT c.id_cancha, c.nombre, "
            f"COUNT(DISTINCT CASE WHEN LOWER(t.estado_turno) != 'disponible' THEN t.id_turno END) as turnos_ocupados "
            f"FROM Cancha c "
            f"LEFT JOIN Turno t ON c.id_cancha = t.id_cancha AND {fecha_condition} "
            f"GROUP BY c.id_cancha, c.nombre "
            f"ORDER BY turnos_ocupados DESC"
        )
        
        try:
            rows = self.base_repo.conn.execute(sql, params).fetchall()
            rows = [dict(row) for row in rows]
        except Exception as e:
            # Si hay error en la consulta, generar PDF con mensaje de error
            styles = getSampleStyleSheet()
            titulo = f"Utilización por Cancha - Año {anio}"
            if mes is not None:
                meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                titulo += f" - {meses_nombres[mes]}"
            elements = [Paragraph(titulo, styles["Heading2"]), Spacer(1, 12)]
            elements.append(Paragraph(f"Error al consultar datos: {str(e)}", styles["Normal"]))
            self._build_pdf(output_path, titulo, elements)
            return
        
        styles = getSampleStyleSheet()
        titulo = f"Utilización por Cancha - Año {anio}"
        if mes is not None:
            meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            titulo += f" - {meses_nombres[mes]}"
        
        elements = [Paragraph(titulo, styles["Heading2"]), Spacer(1, 12)]
        
        # Verificar si hay datos
        if not rows or len(rows) == 0:
            periodo = f"el año {anio}"
            if mes is not None:
                meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                periodo = f"{meses_nombres[mes]} {anio}"
            elements.append(Paragraph(f"No hay datos de utilización para {periodo}.", styles["Normal"]))
            self._build_pdf(output_path, titulo, elements)
            return
        
        # Calcular total de turnos ocupados
        total_turnos_ocupados = sum(r["turnos_ocupados"] for r in rows)
        
        # Validar que haya turnos ocupados
        if total_turnos_ocupados == 0:
            periodo = f"el año {anio}"
            if mes is not None:
                meses_nombres = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                periodo = f"{meses_nombres[mes]} {anio}"
            elements.append(Paragraph(f"No hay turnos ocupados en {periodo}.", styles["Normal"]))
            self._build_pdf(output_path, titulo, elements)
            return
        
        # Tabla comparativa
        table_data = [["Cancha", "Turnos Ocupados", "% del Total Ocupado"]]
        
        for r in rows:
            ocupados = r["turnos_ocupados"]
            porcentaje = (ocupados / total_turnos_ocupados * 100) if total_turnos_ocupados > 0 else 0
            
            table_data.append([
                r["nombre"],
                str(ocupados),
                f"{porcentaje:.1f}%"
            ])
        
        table_data.append(["TOTAL", str(total_turnos_ocupados), "100.0%"])
        elements.append(self._make_table(table_data))
        elements.append(Spacer(1, 12))
        
        # Gráfico de torta
        try:
            import matplotlib.pyplot as plt
            
            page_width_pts, _ = A4
            usable_width_pts = page_width_pts - 2 * 36
            target_width_pts = usable_width_pts * 0.65
            
            fig_width_in = target_width_pts / 72
            fig_height_in = fig_width_in  # Cuadrado para torta
            
            fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))
            
            # Filtrar canchas con turnos ocupados > 0 para el gráfico
            canchas_con_turnos = [(r["nombre"], r["turnos_ocupados"]) for r in rows if r["turnos_ocupados"] > 0]
            
            if len(canchas_con_turnos) > 0:
                canchas = [c[0] for c in canchas_con_turnos]
                ocupados = [c[1] for c in canchas_con_turnos]
                
                # Colores variados
                colors = plt.cm.Set3(range(len(canchas)))
                
                # Crear gráfico de torta
                wedges, texts, autotexts = ax.pie(
                    ocupados,
                    labels=canchas,
                    autopct='%1.1f%%',
                    colors=colors,
                    startangle=90
                )
                
                # Mejorar legibilidad
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(8)
                
                for text in texts:
                    text.set_fontsize(9)
                
                ax.set_title("Distribución de Turnos Ocupados por Cancha")
                
                plt.tight_layout()
                
                img_path = self._save_chart_to_png(fig)
                elements.append(self._make_image_element(img_path, width=target_width_pts))
                elements.append(Spacer(1, 12))
            else:
                elements.append(Paragraph("No hay turnos ocupados para mostrar en el gráfico.", styles["Normal"]))
            
        except Exception as e:
            elements.append(Paragraph(f"No se pudo generar el gráfico: {str(e)}", styles["Normal"]))
        
        self._build_pdf(output_path, titulo, elements)
