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
                
                rx.box(
                    navbar(),
                    padding="1rem"
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