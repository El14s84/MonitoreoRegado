import reflex as rx
import asyncio
from datetime import datetime, timedelta, time as dt_time
from sqlmodel import select, Session
from typing import List, Optional
from MonitoreoRegado.models import (
    Calendario,
    Invernadero,
    HistorialAcciones,
    Semana,
    Acciones
)
from MonitoreoRegado.state.arduino_state import ArduinoState
from MonitoreoRegado.state.auth_state import AuthState
from pydantic import BaseModel

class ProgramacionData(BaseModel):
    id: int
    invernadero_id: int
    invernadero_nombre: str
    dia_semana: str
    hora_inicial: str
    hora_final: str
    necesita_confirmacion: bool
    ultima_confirmacion: Optional[str] = None

class CalendarState(rx.State):
    form_abierto: bool = False
    editando_id: Optional[int] = None
    
    invernadero_seleccionado: str = "0"
    semana_seleccionada: str = "0"
    hora_inicial: str = "08:00"
    hora_final: str = "09:00"
    
    programaciones: List[ProgramacionData] = []
    
    mostrar_notificacion: bool = False
    mensaje_notificacion: str = ""
    notificacion_invernadero_id: int = 0
    notificacion_calendario_id: int = 0
    
    _verificacion_activa: bool = False
    
    mensaje_error: str = ""
    
    lista_invernadero: List[dict] = []
    lista_dias_semana: List[dict] = []
    
    def set_invernadero_seleccionado(self, value: str):
        self.invernadero_seleccionado = value
    
    def set_semana_seleccionada(self, value: str):
        self.semana_seleccionada = value
    
    def set_hora_inicial(self, value: str):
        self.hora_inicial = value
    
    def set_hora_final(self, value: str):
        self.hora_final = value
    
    def set_form_abierto(self, value: bool):
        self.form_abierto = value
    
    def abrir_formulario(self):
        self.form_abierto = True
        self.editando_id = None
        self.limpiar_formulario()
        self.mensaje_error = ""
        self.cargar_listas()
    
    def cerrar_formulario(self):
        self.form_abierto = False
        self.limpiar_formulario()
        self.mensaje_error = ""
    
    def limpiar_formulario(self):
        self.invernadero_seleccionado = "0"
        self.semana_seleccionada = "0"
        self.hora_inicial = "08:00"
        self.hora_final = "09:00"
        
    def cargar_programaciones(self):
        try:
            with rx.session() as session:
                calendario = session.exec(
                    select(Calendario)
                    .where(Calendario.is_active == True)
                ).all()
                
                self.programaciones = []
                for cal in calendario:
                    necesita_confirmacion = self._verificar_necesita_confirmacion(cal)
                    
                    ultima_conf_str = None
                    if cal.ultima_confirmacion:
                        ultima_conf_str = cal.ultima_confirmacion.strftime("%d/%m/%Y %H:%M")
                    
                    prog = ProgramacionData(
                        id=cal.id,
                        invernadero_id=cal.invernadero_id,
                        invernadero_nombre=f"Invernadero {cal.invernadero_id}",
                        dia_semana=cal.semana.nombre_dia if cal.semana else "N/A",
                        hora_inicial=cal.hora_inicial.strftime("%H:%M") if cal.hora_inicial else "N/A",
                        hora_final=cal.hora_final.strftime("%H:%M") if cal.hora_final else "N/A",
                        necesita_confirmacion=necesita_confirmacion,
                        ultima_confirmacion=ultima_conf_str
                    )
                    
                    self.programaciones.append(prog)
        except Exception as e:
            print(f"Error al cargar programaciones: {e}")
            
    def cargar_listas(self):
        self.obtener_invernaderos_activos()
        self.obtener_dias_semana()
    
    def obtener_dias_semana(self) -> List[dict]:
        try:
            with rx.session() as session:
                dias_semana = session.exec(select(Semana)).all()
                self.lista_dias_semana = [
                    {"id": dia.id, "nombre": dia.nombre_dia} 
                    for dia in dias_semana
                ]
        except Exception as e:
            print(f"Error al obtener días de la semana: {e}")
            return []
        
    def obtener_invernaderos_activos(self) -> List[dict]:
        try:
            with rx.session() as session:
                invernaderos = session.exec(
                    select(Invernadero)
                    .where(Invernadero.is_active == True)
                ).all()
                self.lista_invernadero = [
                    {"id": inv.id, "nombre": f"Invernadero {inv.id}"} 
                    for inv in invernaderos
                ]
        except Exception as e:
            print(f"Error al obtener invernaderos activos: {e}")
            return []
        
    def _verificar_necesita_confirmacion(self, calendario: Calendario):
        if not calendario.ultima_confirmacion:
            return False
        
        ahora = datetime.now()
        diferencia = ahora - calendario.ultima_confirmacion
        
        return diferencia.days >= 7
    
    def guardar_programacion(self):
        try:
            with rx.session() as session:
                if self.invernadero_seleccionado == "0":
                    self.mensaje_error = "Debe seleccionar un invernadero."
                    return
                
                inv_id = int(self.invernadero_seleccionado)
                inv = session.get(Invernadero, inv_id)
                
                if not inv or not inv.is_active:
                    self.mensaje_error = "Invernadero no encontrado."
                    return
                
                if self.semana_seleccionada == "0":
                    self.mensaje_error = "Debe seleccionar una semana."
                    return
                
                sem_id = int(self.semana_seleccionada)
                
                try:
                    hora_ini = datetime.strptime(self.hora_inicial, "%H:%M").time()
                    hora_fin = datetime.strptime(self.hora_final, "%H:%M").time()
                except ValueError:
                    self.mensaje_error = "Formato de hora incorrecto."
                    return
                
                if hora_ini >= hora_fin:
                    self.mensaje_error = "La hora final debe ser posterior a la hora inicial."
                    return
                
                if self.editando_id:
                    calendario = session.get(Calendario, self.editando_id)
                    if calendario:
                        calendario.invernadero_id = self.inv_id
                        calendario.semana_id = self.sem_id
                        calendario.hora_inicial = hora_ini
                        calendario.hora_final = hora_fin
                        session.add(calendario)
                    else:
                        pass
                    
                if not self.editando_id:
                    nuevo_calendario = Calendario(
                        invernadero_id=self.invernadero_seleccionado,
                        semana_id=self.semana_seleccionada,
                        hora_inicial=hora_ini,
                        hora_final=hora_fin,
                        is_active=True,
                        ultima_confirmacion=None
                    )
                    session.add(nuevo_calendario)
                    
                session.commit()
                print("Programación guardada correctamente")
                    
                self.cerrar_formulario()
                self.cargar_programaciones()
        except Exception as e:
            print(f"Error al guardar programación: {e}")
            self.mensaje_error = "Error al guardar programación."
            
    def editar_programacion(self, calendario_id: int):
        try:
            with rx.session() as session:
                calendario = session.get(Calendario, calendario_id)
                if calendario:
                    self.editando_id = calendario_id
                    self.invernadero_seleccionado = str(calendario.invernadero_id or 0)
                    self.semana_seleccionada = str(calendario.semana_id or 0)
                    self.hora_inicial = calendario.hora_inicial.strftime("%H:%M") if calendario.hora_inicial else "08:00"
                    self.hora_final = calendario.hora_final.strftime("%H:%M") if calendario.hora_final else "09:00"
                    self.form_abierto = True
                    self.mensaje_error = ""
        except Exception as e:
            print(f"Error al editar programación: {e}")
            
    def eliminar_programacion(self, calendario_id: int):
        try:
            with rx.session() as session:
                calendario = session.get(Calendario, calendario_id)
                if calendario:
                    calendario.is_active = False
                    session.add(calendario)
                    session.commit()
                    print("Programación eliminada correctamente")
                    self.cargar_programaciones()
        except Exception as e:
            print(f"Error al eliminar programación: {e}")
    
    def confirmar_programacion(self, calendario_id: int):
        try:
            with rx.session() as session:
                calendario = session.get(Calendario, calendario_id)
                if not calendario:
                    return
                
                calendario.ultima_confirmacion = datetime.now()
                session.add(calendario)
                
                accion = session.exec(
                    select(Acciones)
                    .where(Acciones.descripcion=="Riego Automático")
                ).first()
                
                if not accion:
                    print("No se encontró la acción 'Riego Automático'")
                    return
                    
                historial = HistorialAcciones(
                    invernadero_id=calendario.invernadero_id,
                    fecha_hora=datetime.now(),
                    accion_id=accion.id,
                    usuario_id=AuthState.usuario_id
                )
                session.add(historial)
                session.commit()
                
                self.mostrar_notificacion = False
                self.cargar_programaciones()
        except Exception as e:
            print(f"Error al confirmar programación: {e}")
    
    async def iniciar_verificacion(self):
        if self._verificacion_activa:
            return
        
        self._verificacion_activa = True
        yield CalendarState.bucle_verificacion()
        
    async def bucle_verificacion(self):
        if not self._verificacion_activa:
            return
        
        try:
            ahora = datetime.now()
            dia_actual = ahora.weekday()
            hora_actual = ahora.time()
            
            with rx.session() as session:
                calendarios = session.exec(
                    select(Calendario)
                    .where(Calendario.is_active == True)
                    .where(Calendario.semana_id == dia_actual + 1)
                ).all()
                
                for calendario in calendarios:
                    if not calendario.hora_inicial or not calendario.hora_final:
                        continue
                    
                    if calendario.hora_inicial <= hora_actual <= calendario.hora_final:
                        if not calendario.ultima_confirmacion or \
                            (ahora - calendario.ultima_confirmacion).days >= 7:
                                self._activar_riego_calendario(calendario)
                    elif hora_actual > calendario.hora_final:
                        self._desactivar_riego_calendario(calendario)
        except Exception as e:
            print(f"Error en la verificación: {e}")
        
        await asyncio.sleep(30)
        yield CalendarState.bucle_verificacion()
    
    def _activar_riego_calendario(self, calendario: Calendario):
        try:
            arduino_state = self.get_state(ArduinoState)
            if arduino_state:
                arduino_state.activar_riego_programado(calendario.invernadero_id)

            self.mostrar_notificacion = True
            self.mensaje_notificacion = f"Riego programado para el invernadero {calendario.invernadero_id}"
            self.notificacion_invernadero_id = calendario.invernadero_id
            self.notificacion_calendario_id = calendario.id
            
            self.cargar_programaciones()
        except Exception as e:
            print(f"Error al activar riego programado: {e}")
    
    def _desactivar_riego_calendario(self, calendario: Calendario):
        try:
            arduino_state = self.get_state(ArduinoState)
            if arduino_state:
                arduino_state.desactivar_riego_programado(calendario.invernadero_id)
        except Exception as e:
            print(f"Error al desactivar riego programado: {e}")
    
    def cerrar_notificacion(self):
        self.mostrar_notificacion = False