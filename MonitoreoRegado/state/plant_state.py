import reflex as rx
from sqlmodel import select
from MonitoreoRegado.models import  Planta, TipoPlanta, Invernadero
from MonitoreoRegado.state.auth_state import AuthState
from MonitoreoRegado.state.greenhouse_state import GreenhouseState

PLANTAS_DISPONIBLES = {
    "Orquídea": {
        "temp_min": 18.0,
        "temp_max": 24.0,
        "hum_min": 70.0,
        "hum_max": 80.0
    },
    "Tomate Cherry": {
        "temp_min": 20.0,
        "temp_max": 25.0,
        "hum_min": 60.0,
        "hum_max": 70.0
    },
    "Lechuga Romana": {
        "temp_min": 16.0,
        "temp_max": 22.0,
        "hum_min": 50.0,
        "hum_max": 60.0
    },
    "Fresa": {
        "temp_min": 18.0,
        "temp_max": 24.0,
        "hum_min": 60.0,
        "hum_max": 70.0
    },
    "Albahaca": {
        "temp_min": 20.0,
        "temp_max": 30.0,
        "hum_min": 50.0,
        "hum_max": 60.0
    },
}

class PlantState(rx.State):
    # Campos del formulario
    nombre_planta: str = ""
    tipo_planta_seleccionado: str = ""
    temp_min: float = 0.0
    temp_max: float = 0.0
    hum_min: float = 0.0
    hum_max: float = 0.0
    estado: bool = True
    
    # Mensajes y estado
    mensaje: str = ""
    is_loading: bool = False
    
    tipos_planta: list[str] = []
    
    @rx.var
    def plantas_disponibles(self) -> list[str]:
        return list(PLANTAS_DISPONIBLES.keys())

    def set_nombre_planta(self, value: str):
        self.nombre_planta = value

    def set_tipo_planta_seleccionado(self, value: str):
        self.tipo_planta_seleccionado = value
        self.cargar_datos_planta()

    def set_temp_min(self, value: str):
        try:
            self.temp_min = float(value)
        except (ValueError, TypeError):
            pass

    def set_temp_max(self, value: str):
        try:
            self.temp_max = float(value)
        except (ValueError, TypeError):
            pass

    def set_hum_min(self, value: str):
        try:
            self.hum_min = float(value)
        except (ValueError, TypeError):
            pass

    def set_hum_max(self, value: str):
        try:
            self.hum_max = float(value)
        except (ValueError, TypeError):
            pass

    def set_estado(self, value: bool):
        self.estado = value
    
    def cargar_tipos_planta(self):
        try:
            with rx.session() as db:
                tipos = db.exec(select(TipoPlanta.nombre)).all()
                self.tipos_planta = list(tipos)
        except Exception as e:
            print(f"Error al cargar tipos de planta: {e}")
    
    
    def cargar_datos_planta(self):
        if self.tipo_planta_seleccionado in PLANTAS_DISPONIBLES:
            datos = PLANTAS_DISPONIBLES[self.tipo_planta_seleccionado]
            self.temp_min = datos["temp_min"]
            self.temp_max = datos["temp_max"]
            self.hum_min = datos["hum_min"]
            self.hum_max = datos["hum_max"]
            self.estado = True
            if not self.nombre_planta:
                self.nombre_planta = self.tipo_planta_seleccionado
    
    def guardar_planta(self):
        self.is_loading = True
        self.mensaje = ""
        
        from MonitoreoRegado.state.auth_state import AuthState
        try:
            auth_state = self.get_state(AuthState)
            usuario_id = getattr(auth_state, 'usuario_id', None)
            print(f"Usuario ID obtenido: {usuario_id}")
        except Exception as e:
            print(f"Error obteniendo usuario_id: {e}")
            usuario_id = None
        
        try:
            if not self.tipo_planta_seleccionado:
                self.mensaje = "Por favor selecciona un tipo de planta"
                self.is_loading = False
                return
            
            if not self.nombre_planta:
                self.mensaje = "Por favor ingresa un nombre para la planta"
                self.is_loading = False
                return
            
            if not self.nombre_planta or not self.tipo_planta_seleccionado:
                self.mensaje = "Por favor completa todos los campos obligatorios"
                self.is_loading = False
                return
            
            if self.temp_min >= self.temp_max:
                self.mensaje = "La temperatura mínima debe ser menor que la máxima"
                self.is_loading = False
                return
            
            if self.hum_min >= self.hum_max:
                self.mensaje = "La humedad mínima debe ser menor que la máxima"
                self.is_loading = False
                return
            
            with rx.session() as db:
                tipo_planta = db.exec(
                    select(TipoPlanta).where(TipoPlanta.nombre == self.tipo_planta_seleccionado)
                ).first()
                
                if not tipo_planta:
                    tipo_planta = TipoPlanta(
                        nombre=self.tipo_planta_seleccionado,
                        descripcion=f"Tipo de planta {self.tipo_planta_seleccionado}"
                    )
                    db.add(tipo_planta)
                    db.commit()
                    db.refresh(tipo_planta)
                    self.mensaje = f"Tipo de planta '{self.tipo_planta_seleccionado}' creado"
                
                nueva_planta = Planta(
                    tipo_planta_id=tipo_planta.id,
                    temp_min=float(self.temp_min),
                    temp_max=float(self.temp_max),
                    hum_min=float(self.hum_min),
                    hum_max=float(self.hum_max),
                    estado=bool(self.estado)
                )
                
                db.add(nueva_planta)
                db.commit()
                db.refresh(nueva_planta)
                
                nuevo_invernadero = Invernadero(
                    planta_id=nueva_planta.id,
                    usuario_id=usuario_id,
                    Temperatura=float(0.0),
                    Humedad=float(0.0),
                    Nivel_Agua=float(0.0),
                    Riego_Activo=False,
                    is_active=False
                )
                
                db.add(nuevo_invernadero)
                db.commit()
                
                print(f"INVERNADERO CREADO - ID: {nuevo_invernadero.id}, Planta ID: {nuevo_invernadero.planta_id}")
                
                self.mensaje = f"Planta '{self.nombre_planta}' guardada"
            
                self.nombre_planta = ""
                self.tipo_planta_seleccionado = ""
                self.temp_min = 0.0
                self.temp_max = 0.0
                self.hum_min = 0.0
                self.hum_max = 0.0
                self.estado = True
            
            yield GreenhouseState.cerrar_dialogo
            yield GreenhouseState.cargar_invernaderos
            
        except Exception as e:
            self.mensaje = f"Error al guardar planta: {str(e)}"
            print(f"Error al guardar planta: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading = False
    
    async def limpiar_formulario(self):
        self.nombre_planta = ""
        self.tipo_planta_seleccionado = ""
        self.temp_min = 0.0
        self.temp_max = 0.0
        self.hum_min = 0.0
        self.hum_max = 0.0
        self.estado = True
        self.mensaje = ""
        
    def on_mount(self):
        self.cargar_tipos_planta()
