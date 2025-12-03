import reflex as rx
from MonitoreoRegado.components.navbar import navbar
from MonitoreoRegado.state.auth_state import AuthState

def drawer_content() -> rx.Component:
    return rx.drawer.portal(
        rx.drawer.content(
            rx.vstack(
                rx.flex(
                    rx.drawer.close(
                        rx.button("×", variant="ghost")
                    ),
                    justify="end",
                    width="100%",
                    padding_bottom="1rem"
                ),
                
                rx.heading("Navegación", size="5", padding_x="1rem"),
                
                rx.card(
                    rx.avatar(src="/images/profile-icon.png", size="5"),
                    rx.text(
                        AuthState.nombre_actual, 
                        margin_top="1rem", 
                        margin_bottom="0.5rem",
                        font_weight="bold",
                    ),
                    rx.text(
                        AuthState.rol_actual, 
                        margin_top="0.5rem", 
                        margin_bottom="1rem",
                    ),
                    rx.spacer(),
                    padding="1rem",
                ),
                
                rx.vstack(
                    rx.link("Inicio", href="/monitoreo"),
                    rx.link("Invernadero", href="/greenhouse"),
                    spacing="4",
                    padding="1rem",
                ),
                
                rx.spacer(),
                
                rx.box(
                    rx.button(
                        "Cerrar Sesión",
                        on_click=AuthState.logout,
                        color_scheme="red",
                        width="100%"
                    ),
                    padding="1rem",
                ),
                align="stretch",
                height="100%",
                width="250px",
                padding="1em",
                bg=rx.color("mauve", 2),
            )
        )
    )