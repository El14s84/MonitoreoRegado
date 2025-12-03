import reflex as rx
from MonitoreoRegado.components.navbar import navbar
from MonitoreoRegado.state.auth_state import AuthState
from MonitoreoRegado.components.drawer import drawer_content
from MonitoreoRegado.state.arduino_state import ArduinoState

def render_fila(fila: dict):
    return rx.table.row(
        rx.table.cell(fila["Fecha y Hora"]),
        rx.table.cell(fila["Temperatura"]),
        rx.table.cell(fila["Humedad"]),
        rx.table.cell(fila["Nivel de Agua"]),
    )

def index() -> rx.Component:
    
    autenticado_view = rx.container(
        rx.hstack(
            rx.drawer.trigger(rx.button("☰")),
            rx.color_mode.button(),
            width="100%",
            justify="between",
            padding_bottom="1em",
        ),
        navbar(),
        rx.divider(),
        rx.heading("ÁREA DE MONITOREO", size="9", text_align="center", margin_top="40px",),
        rx.vstack(
            rx.hstack(
                rx.card(
                    rx.vstack(
                        rx.text("Nivel de agua", size="5", text_align="center"),
                        rx.icon("droplets", size=80, color="blue"),
                        rx.text(ArduinoState.nivel_agua, size="5", text_align="center"),
                        align="center",
                        justify="center",
                        height="100%",
                    ),
                    width="250px",
                    height="250px",
                    padding="20px",
                    box_shadow="md",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Nivel de temperatura", size="5", text_align="center"),
                        rx.icon("thermometer", size=80, color="red"),
                        rx.text(ArduinoState.temperatura, size="5", text_align="center"),
                        align="center",
                        justify="center",
                        height="100%",
                    ),
                    width="250px",
                    height="250px",
                    padding="20px",
                    box_shadow="md",
                    border_radius="md",
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Nivel de humedad", size="5", text_align="center"),
                        rx.icon("cloud-drizzle", size=80, color="teal"),
                        rx.text(ArduinoState.humedad, size="5", text_align="center"),
                        align="center",
                        justify="center",
                        height="100%",
                    ),
                    width="250px",
                    height="250px",
                    padding="20px",
                    box_shadow="md",
                    border_radius="md",
                ),
                spacing="5",
                align="center",
                justify="center",
            ),
            rx.card(
                    rx.vstack(
                        rx.heading("Últimos registros", size="5"),
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Tiempo Real"),
                                    rx.table.column_header_cell("Temperatura"),
                                    rx.table.column_header_cell("Humedad"),
                                    rx.table.column_header_cell("Nivel de Agua"),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(ArduinoState.historial_tabla, render_fila)
                            ),
                            variant="surface",
                            size="2",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
            ),
            spacing="5",
            margin_top="20px",
            align="center",
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
        direction="left",
    )