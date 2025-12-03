import reflex as rx
from MonitoreoRegado.pages.index_page import index
from MonitoreoRegado.pages.register_page import pagina_registro
from MonitoreoRegado.pages.login_page import pagina_login
from MonitoreoRegado.pages.greenhouse_page import pagina_invernadero
from MonitoreoRegado.pages.greenhouse_form import formulario_invernadero
from MonitoreoRegado.state.arduino_state import ArduinoState

app = rx.App()
app.add_page(pagina_login, route="/", title="Login")
app.add_page(pagina_registro, route="/registro", title="Registro")
app.add_page(index, route="/monitoreo", title="Inicio", on_load=ArduinoState.iniciar_monitoreo)
app.add_page(pagina_invernadero, route="/greenhouse", title="Invernadero")
app.add_page(formulario_invernadero, route="/greenhouse_form", title="Agregar Planta")