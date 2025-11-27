import reflex as rx
from MonitoreoRegado.components.navbar import navbar
from MonitoreoRegado.state.auth_state import AuthState
from MonitoreoRegado.components.drawer import drawer_content

def index() -> rx.Component:
    
    autenticado_view = rx.container(
        rx.hstack(
            rx.color_mode.button(),
            rx.drawer.trigger(rx.button("☰")),
            width="100%",
            justify="between",
            padding_bottom="1em",
        ),
        navbar(),
        rx.heading("MONITOREO DE REGADO", size="9", text_align="center", margin_top="40px",),
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.text("nivel de agua"),
                    rx.image(
                        src="/images/onda-de-agua-acuarela.jpg",
                        width="200px",
                        height="200px",
                        object_fit="cover",
                    ),
                    margin_bottom="20px",
                ),
                padding="20px",
                box_shadow="md",
                border_radius="md",
                max_width="600px",
            ),
            rx.card(
                rx.vstack(
                    rx.text("nivel de temperatura"),
                    rx.image(
                        src="/images/pintura-en-aerosol.jpg",
                        width="200px",
                        height="200px",
                        object_fit="cover",
                    ),
                    margin_bottom="20px",
                ),
                padding="20px",
                box_shadow="md",
                border_radius="md",
                max_width="600px",
            ),
            rx.card(
                rx.vstack(
                    rx.text("nivel de humedad"),
                    rx.image(
                        src="/images/diseno-abstracto-circulo-azul.jpg",
                        width="200px",
                        height="200px",
                        object_fit="cover",
                        margin_bottom="20px",
                    ),
                ),
                padding="20px",
                box_shadow="md",
                border_radius="md",
                max_width="600px",
            ),
            spacing="5",
            justify="center",
            min_height="60vh",
            margin_top="60px",
        ),
    )
    
    no_autenticado_view = rx.container(
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
    
    return rx.drawer.root(
        rx.cond(
            AuthState.correcta_autenticacion,
            autenticado_view,
            no_autenticado_view,
        ),
        drawer_content(),
        rx.drawer.overlay(z_index="5"),
        direction="right",
    )
    

