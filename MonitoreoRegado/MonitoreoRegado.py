import reflex as rx
from MonitoreoRegado.pages.index_page import index
from MonitoreoRegado.pages.register_page import pagina_registro
from MonitoreoRegado.pages.login_page import pagina_login
from MonitoreoRegado.pages.dashboard_page import dashboard

app = rx.App()
app.add_page(pagina_login, route="/", title="Login")
app.add_page(pagina_registro, route="/registro", title="Registro")
app.add_page(index, route="/monitoreo", title="Inicio")
