import reflex as rx
from MonitoreoRegado.state.auth_state import AuthState
from MonitoreoRegado.components.roles import solo_para_admin, solo_para_usuario
from MonitoreoRegado.components.drawer import drawer_content

def pagina_reporte() -> rx.Component:
    es_admin_view = rx.container(
        rx.hstack(
            rx.drawer.trigger(rx.button("☰")),
            rx.color_mode.button(),
            width="100%",
            justify="between",
            padding_bottom="1em",
        ),
        rx.heading("Reporte - Vista de Administrador", size="8", text_align="center", margin_top="40px",),
        rx.text("Aquí puedes ver y gestionar todos los datos del sistema.", text_align="center"),
        margin_top="20px",
        margin_bottom="20px",
    )
    
    no_admin_view = rx.container(
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
    
    return rx.drawer.root(
        rx.cond(
            AuthState.correcta_autenticacion & (AuthState.rol_actual == "admin"),
            es_admin_view,
            no_admin_view
        ),
        drawer_content(),
        rx.drawer.overlay(z_index="5"),
        direction="left",
    )