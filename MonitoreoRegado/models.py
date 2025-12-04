from datetime import datetime, time
from typing import List, Optional
import reflex as rx
from sqlmodel import Field, Relationship, SQLModel

class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str = Field(unique=True)
    
    usuarios: List["Usuario"] = Relationship(back_populates="rol")
    
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rol_id: Optional[int] = Field(default=None, foreign_key="rol.id")
    rol: Optional[Rol] = Relationship(back_populates="usuarios")
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    
    invernaderos: List["Invernadero"] = Relationship(back_populates="usuario")
    reportes: List["Reporte"] = Relationship(back_populates="usuario")
    Acciones: List["HistorialAcciones"] = Relationship(back_populates="usuario")

class TipoPlanta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: Optional[str] = None
    
    plantas: List["Planta"] = Relationship(back_populates="tipo_planta")
    
class Planta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo_planta_id: Optional[int] = Field(default=None, foreign_key="tipoplanta.id")
    tipo_planta: Optional[TipoPlanta] = Relationship(back_populates="plantas")
    temp_min: float
    temp_max: float
    hum_min: float
    hum_max: float
    estado: Optional[bool] = None
    
    invernadero: Optional["Invernadero"] = Relationship(back_populates="planta")
    
class Invernadero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    planta_id: Optional[int] = Field(default=None, foreign_key="planta.id")
    planta: Optional[Planta] = Relationship(back_populates="invernadero")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="invernaderos")
    Registro_Lectura: datetime = Field(default_factory=datetime.now)
    Humedad: float= Field(default=0.0)
    Temperatura: float= Field(default=0.0)
    Nivel_Agua: float= Field(default=0.0)
    Riego_Activo: bool = False
    is_active: bool = True
    eliminado: bool = False
    
    reporte_historico: List["Reporte"] = Relationship(back_populates="invernadero")
    accion: List["HistorialAcciones"] = Relationship(back_populates="invernadero")
    fijar_calendario: List["Calendario"] = Relationship(back_populates="invernadero")
    sensor: List["Sensor"] = Relationship(back_populates="invernadero")

class TipoReporte(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: Optional[str] = None
    
    reportes: List["Reporte"] = Relationship(back_populates="tipo_reporte")

class Reporte(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo_reporte_id: Optional[int] = Field(default=None, foreign_key="tiporeporte.id")
    tipo_reporte: Optional[TipoReporte] = Relationship(back_populates="reportes")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="reportes")
    invernadero_id: Optional[int] = Field(default=None, foreign_key="invernadero.id")
    invernadero: Optional[Invernadero] = Relationship(back_populates="reporte_historico")
    Fecha_Generacion: datetime = Field(default_factory=datetime.now)
    Rango_Fecha_Inicio: Optional[datetime] = None
    Rango_Fecha_Fin: Optional[datetime] = None
    Detalles: Optional[str] = None
    
class Acciones(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: Optional[str] = None
    
    historial_acciones: List["HistorialAcciones"] = Relationship(back_populates="accion")

class HistorialAcciones(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invernadero_id: Optional[int] = Field(default=None, foreign_key="invernadero.id")
    invernadero: Optional[Invernadero] = Relationship(back_populates="accion")
    fecha_hora: datetime = Field(default_factory=datetime.now)
    accion_id: Optional[int] = Field(default=None, foreign_key="acciones.id")
    accion: Optional[Acciones] = Relationship(back_populates="historial_acciones")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="Acciones")

class Semana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_dia: str
    
    calendarios: List["Calendario"] = Relationship(back_populates="semana")
    
class Calendario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invernadero_id: Optional[int] = Field(default=None, foreign_key="invernadero.id")
    invernadero: Optional[Invernadero] = Relationship(back_populates="fijar_calendario")
    semana_id: Optional[int] = Field(default=None, foreign_key="semana.id")
    semana: Optional[Semana] = Relationship(back_populates="calendarios")
    hora_inicial: Optional[time] = None
    hora_final: Optional[time] = None
    is_active: bool = True
    ultima_confirmacion: Optional[datetime] = None
    
class Sensor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invernadero_id: Optional[int] = Field(default=None, foreign_key="invernadero.id")
    invernadero: Optional[Invernadero] = Relationship(back_populates="sensor")
    fecha_hora: datetime = Field(default_factory=datetime.now)
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    nivel_agua: Optional[float] = None
    
def inicializar_datos():
    from sqlmodel import Session, select
    import reflex as rx
    
    with rx.session() as session:
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for dia in dias_semana:
            existe = session.exec(select(Semana).where(Semana.nombre_dia == dia)).first()
            if not existe:
                semana = Semana(nombre_dia=dia)
                session.add(semana)
                print(f"Día insertado: {dia}")
        
        acciones = ["Riego Automático", "Generar Reporte"]
        for accion in acciones:
            existe = session.exec(select(Acciones).where(Acciones.descripcion == accion)).first()
            if not existe:
                accion = Acciones(descripcion=accion)
                session.add(accion)
                print(f"Acción insertada: {accion}")
        
        session.commit()
        print("Datos inicializados correctamente")
