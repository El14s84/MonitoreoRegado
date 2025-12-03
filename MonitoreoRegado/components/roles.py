import reflex as rx
from MonitoreoRegado.state.auth_state import AuthState


def solo_para_admin(componente: rx.Component) -> rx.Component:
    return rx.cond(
        AuthState.correcta_autenticacion & (AuthState.rol_actual == "admin"),
        componente,
        rx.container(
            rx.vstack(
                rx.heading("Acceso no autorizado", size="9"),
                rx.text("Necesitas permisos de administrador", size="5"),
                rx.link(
                    rx.button("Ir al inicio", color_scheme="blue"),
                    href="/monitoreo"
                ),
                spacing="5",
                justify="center",
                min_height="60vh",
            ),  
        )
    )

def solo_para_usuario(componente: rx.Component) -> rx.Component:
    return rx.cond(
        AuthState.correcta_autenticacion,
        componente,
        rx.container(
            rx.vstack(
                rx.heading("Acceso no autorizado", size="9"),
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