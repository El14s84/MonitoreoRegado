import reflex as rx
from MonitoreoRegado.state.auth_state import AuthState

def dashboard() -> rx.Component:
    return rx.cond(
        AuthState.correcta_autenticacion,
        rx.container(
            rx.vstack(
                rx.heading("Dashboard", size="9"),
                rx.text("Bienvenido al área privada", size="5"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    color_scheme="red",
                ),
                spacing="5",
                justify="center",
                min_height="60vh",
            ),
        ),
        rx.container(
            rx.vstack(
                rx.heading("Acceso denegado", size="9"),
                rx.text("Necesitas iniciar sesión", size="5"),
                rx.link(
                    rx.button("Ir al login", color_scheme="blue"),
                    href="/"
                ),
                spacing="5",
                justify="center",
                min_height="60vh",
            ),
        )
    )
