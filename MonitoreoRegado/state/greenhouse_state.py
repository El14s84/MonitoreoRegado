import reflex as rx
from sqlmodel import select
from MonitoreoRegado.models import Invernadero, Planta, TipoPlanta, Usuario
from typing import List, Dict

class GreenhouseState(rx.State):
    invernaderos: List[Dict] = []
    mostrar_dialogo: bool = False
    mensaje: str = ""
    mostrar_dialogo_eliminar: bool = False
    invernadero_por_eliminar: int | None = None
    
    def set_mostrar_dialogo(self, value: bool):
        self.mostrar_dialogo = value
        
    def set_mensaje(self, value: str):
        self.mensaje = value
    
    def set_mostrar_dialogo_eliminar(self, value: bool):
        self.mostrar_dialogo_eliminar = value
        if not value:
            self.invernadero_por_eliminar = None
        
    def set_invernaderos(self, value: List[Dict]):
        self.invernaderos = value
    
    def abrir_dialogo(self):
        self.mostrar_dialogo = True
        
    def cerrar_dialogo(self):
        self.mostrar_dialogo = False
        self.mensaje = ""
        
    def abrir_dialogo_eliminar(self, invernadero_id: int):
        self.invernadero_por_eliminar = invernadero_id
        self.mostrar_dialogo_eliminar = True
    
    def cerrar_dialogo_eliminar(self):
        self.mostrar_dialogo_eliminar = False
        self.invernadero_por_eliminar = None
        
    def confirmar_eliminacion(self):
        if self.invernadero_por_eliminar is None:
            print("No hay invernadero seleccionado para eliminar.")
            return
        
        try:
            with rx.session() as db:
                invernadero = db.exec(
                    select(Invernadero).where(Invernadero.id == self.invernadero_por_eliminar)
                ).first()
            
                if invernadero:
                    invernadero.eliminado = True
                    invernadero.is_active = False
                    db.commit()
                    print(f"Invernadero {self.invernadero_por_eliminar} eliminado.")
                    self.mensaje = "Invernadero eliminado."
                else:
                    print(f"Invernadero {self.invernadero_por_eliminar} no encontrado.")
                    self.mensaje = "Invernadero no encontrado."
        except Exception as e:
            print(f"Error al eliminar invernadero: {e}")
            self.mensaje = f"Error al eliminar invernadero: {str(e)}"
        
        self.cerrar_dialogo_eliminar()
        self.cargar_invernaderos()
    
    def cargar_invernaderos(self):
        try:
            with rx.session() as db:
                invernaderos_db = db.exec(
                    select(Invernadero).where(Invernadero.eliminado == False)
                ).all()
                print(f"Invernaderos encontrados: {len(invernaderos_db)}")
                
                self.invernaderos = []
                
                for inv in invernaderos_db:
                    if inv.planta_id:
                        planta = db.exec(
                            select(Planta).where(Planta.id == inv.planta_id)
                        ).first()
                        
                        if planta and planta.tipo_planta_id:
                            tipo_planta = db.exec(
                                select(TipoPlanta).where(TipoPlanta.id == planta.tipo_planta_id)
                            ).first()
                            
                            if tipo_planta:
                                self.invernaderos.append({
                                    "id": inv.id,
                                    "nombre_planta": tipo_planta.nombre,
                                    "nombre_usuario": "Mi Planta",
                                    "is_active": inv.is_active,
                                    "temperatura": inv.Temperatura,
                                    "humedad": inv.Humedad,
                                    "nivel_agua": inv.Nivel_Agua,
                                    "temp_min": planta.temp_min,
                                    "temp_max": planta.temp_max,
                                    "hum_min": planta.hum_min,
                                    "hum_max": planta.hum_max
                                })
                                print(f"Invernadero cargado: {inv.id} - {tipo_planta.nombre}")
                            else:
                                print(f"TipoPlanta no encontrado para planta {planta.id}")
                        else:
                            print(f"Planta no encontrada o sin tipo para invernadero {inv.id}")
                    else:
                        print(f"Invernadero {inv.id} sin planta_id")
                
                print(f"Total invernaderos cargados: {len(self.invernaderos)}")
        except Exception as e:
            print(f"Error al cargar invernaderos: {e}")
            import traceback
            traceback.print_exc()
            self.invernaderos = []
    
    def toque_invernadero(self, invernadero_id: int):
        try:
            with rx.session() as db:
                invernadero = db.exec(
                    select(Invernadero).where(Invernadero.id == invernadero_id)
                ).first()
                
                if not invernadero:
                    self.mensaje = "Invernadero no encontrado."
                    return
                
                if not invernadero.is_active:
                    otros_activos = db.exec(
                        select(Invernadero).where(Invernadero.id != invernadero_id)
                    ).all()
                    
                    for otro in otros_activos:
                        otro.is_active = False
                    
                    invernadero.is_active = True
                    self.mensaje = "Invernadero activado."
                else:
                    invernadero.is_active = False
                    self.mensaje = "Invernadero desactivado."
                
                db.commit()
                
                print(f"Toque invernadero {invernadero_id}: is_active={invernadero.is_active}")
                
        except Exception as e:
            self.mensaje = f"Error al cambiar estado: {str(e)}"
            print(f"Error en toggle_invernadero: {e}")
            import traceback
            traceback.print_exc()
        
        self.cargar_invernaderos() 
    
    @rx.var       
    def tiene_invernadero_activo(self) -> bool:
        return any(inv.get("is_active", False) for inv in self.invernaderos)
    
    @rx.var
    def obtener_invernadero_activo_id(self) -> int:
        for inv in self.invernaderos:
            if inv.get("is_active", False):
                return inv["id"]
        return 0
    
    def on_mount(self):
        self.cargar_invernaderos()