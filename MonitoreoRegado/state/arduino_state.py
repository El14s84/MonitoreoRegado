import reflex as rx
import serial
import json
import asyncio
from datetime import datetime
from sqlmodel import select, Session
from MonitoreoRegado.models import Sensor, Invernadero 

class ArduinoState(rx.State):
    temperatura: str = "--"
    humedad: str = "--"
    nivel_agua: str = "--"
    
    historial_tabla: list[dict] = []
    
    is_running: bool = False
    serial_port: str = "/dev/cu.usbmodem1051DB2BBC942" 
    baud_rate: int = 9600
    _ser = None

    async def iniciar_monitoreo(self):
        if self.is_running: return
        self.is_running = True
        
        try:
            if not self._ser:
                self._ser = serial.Serial(self.serial_port, self.baud_rate, timeout=0.1)
                self._ser.reset_input_buffer()
                print(f"Conectado a {self.serial_port}")
        except Exception as e:
            print(f"Error conectando: {e}")
            self.is_running = False
            return

        yield ArduinoState.lectura_bucle

    async def lectura_bucle(self):
        if not self.is_running: return

        try:
            if self._ser and self._ser.in_waiting > 0:
                linea = self._ser.readline().decode('utf-8').strip()
                if linea.startswith('{') and linea.endswith('}'):
                    datos = json.loads(linea)
                    
                    self.temperatura = f"{datos.get('temp')}°C"
                    self.humedad = f"{datos.get('hum')}%"
                    self.nivel_agua = "Estable" if int(datos.get('suelo', 0)) > 300 else "Bajo"
                    
                    self.procesar_lectura(
                        temp=float(datos.get('temp', 0)),
                        hum=float(datos.get('hum', 0)),
                        agua=int(datos.get('suelo', 0))
                    )
                    
                    self.actualizar_tabla(datos) 
                    
        except Exception:
            pass 
        
        await asyncio.sleep(0.5)
        yield ArduinoState.lectura_bucle

    def procesar_lectura(self, temp: float, hum: float, agua: int):
        
        self.temperatura = f"{temp}°C"
        self.humedad = f"{hum}%"
        self.nivel_agua = "Estable" if agua > 300 else "Bajo" 

        try:
            with rx.session() as session:
                
                invernadero_activo = session.exec(
                    select(Invernadero).where(Invernadero.is_active == True)
                ).first()
                if invernadero_activo:
                    nuevo_sensor = Sensor(
                        temperatura=temp,
                        humedad=hum,
                        nivel_agua=float(agua),
                        fecha_hora=datetime.now(),
                        invernadero_id=invernadero_activo.id
                    )
                    session.add(nuevo_sensor)
                    
                    invernadero_activo.Temperatura = temp
                    invernadero_activo.Humedad = hum
                    invernadero_activo.Nivel_Agua = float(agua)
                    invernadero_activo.Registro_Lectura = datetime.now()
                    
                    if hum < invernadero_activo.planta.hum_min:
                        invernadero_activo.Riego_Activo = True
                    
                    session.commit()
                    print(f"✓ Datos guardados en invernadero {invernadero_activo.id}")
                
                else:
                    print("No hay invernadero activo para guardar datos.")
                
        except Exception as e:
            print(f"Error guardando en BBDD: {e}")

        nueva_fila = {
            "Fecha y Hora": datetime.now().strftime("%H:%M:%S"),
            "Temperatura": f"{temp} °C",
            "Humedad": f"{hum} %",
            "Nivel de Agua": f"{agua}"
        } 
        
        self.historial_tabla.append(nueva_fila)
        if len(self.historial_tabla) > 5:
            self.historial_tabla.pop(0)
            
    def enviar_comando(self, comando: str):
        try:
            if self._ser and self._ser.is_open:
                self._ser.write(f"{comando}\n".encode())
                print(f"Comando enviado: {comando}")
                return True
        except Exception as e:
            print(f"Error enviando comando: {e}")
        return False

    def activar_riego_programado(self, invernadero_id: int):
        if self.enviar_comando("RIEGO_ON"):
            try:
                with rx.session() as session:
                    invernadero = session.get(Invernadero, invernadero_id)
                    if invernadero:
                        invernadero.Riego_Activo = True
                        session.add(invernadero)
                        session.commit()
                        print(f"Invernadero {invernadero_id} activado.")
            except Exception as e:
                print(f"Error al activar riego programado: {e}")
    
    def desactivar_riego_programado(self, invernadero_id: int):
        if self.enviar_comando("RIEGO_OFF"):
            try:
                with rx.session() as session:
                    invernadero = session.get(Invernadero, invernadero_id)
                    if invernadero:
                        invernadero.Riego_Activo = False
                        session.add(invernadero)
                        session.commit()
                        print(f"Invernadero {invernadero_id} desactivado.")
            except Exception as e:
                print(f"Error al desactivar riego programado: {e}")
    
    def volver_modo_automatico(self):
        self.enviar_comando("MODO_AUTOMATICO")

    def detener_monitoreo(self):
        self.is_running = False
        if self._ser:
            try:
                self._ser.close()
                self._ser = None
                print("Conexión serial cerrada.")
            except Exception as e:
                print(f"Error cerrando conexión: {e}")