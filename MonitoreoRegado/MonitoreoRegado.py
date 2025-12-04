import reflex as rx
from MonitoreoRegado.pages.index_page import index
from MonitoreoRegado.pages.register_page import pagina_registro
from MonitoreoRegado.pages.login_page import pagina_login
from MonitoreoRegado.pages.greenhouse_page import pagina_invernadero
from MonitoreoRegado.state.arduino_state import ArduinoState
from MonitoreoRegado.pages.calendar_page import pagina_calendario
from MonitoreoRegado.state.calendar_state import CalendarState
from MonitoreoRegado.models import inicializar_datos

app = rx.App()

try:
    inicializar_datos()
except Exception as e:
    print(f"Error al inicializar datos: {e}")
    
app.add_page(
    pagina_calendario, 
    route="/calendario", 
    title="Calendario de Riego",
    on_load=CalendarState.cargar_programaciones
)
app.add_page(pagina_login, route="/", title="Login")
app.add_page(pagina_registro, route="/registro", title="Registro")
app.add_page(index, route="/monitoreo", title="Inicio", on_load=ArduinoState.iniciar_monitoreo)
app.add_page(pagina_invernadero, route="/greenhouse", title="Invernadero")