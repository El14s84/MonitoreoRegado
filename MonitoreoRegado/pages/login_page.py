import reflex as rx
from MonitoreoRegado.components.navbar import loginNavbar
from MonitoreoRegado.components.auth_card import auth_card
from MonitoreoRegado.state.auth_state import AuthState

def pagina_login() -> rx.Component:
    return rx.container(
        loginNavbar(),
        rx.flex(
            auth_card("Iniciar sesión", AuthState.login, show_confirm=False, show_rol=False),
            wrap="wrap",
            gap="24px",
            justify="center",
            margin_top="40px",
        ),
        padding_y="40px",
    )
