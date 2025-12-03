import reflex as rx
from MonitoreoRegado.state.auth_state import AuthState
from MonitoreoRegado.components.drawer import drawer_content
from MonitoreoRegado.state.greenhouse_state import GreenhouseState
from MonitoreoRegado.pages.greenhouse_form import formulario_invernadero
from MonitoreoRegado.state.plant_state import PlantState


def tarjeta_invernadero(invernadero: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.switch(
                    checked=invernadero["is_active"],
                    on_change=lambda _: GreenhouseState.toque_invernadero(invernadero["id"]),
                    color_scheme="green",
                ),
                rx.text(
                    rx.cond(invernadero["is_active"], "Activo", "Inactivo"),
                    size="2",
                    color=rx.cond(invernadero["is_active"], "green", "gray"),
                ),
                justify="between",
                width="100%",
            ),
            rx.divider(),
            rx.heading(
                f"{invernadero['nombre_planta']}",
                size="3",
                margin_bottom="0.5em",
                font_weight="bold",
            ),
            
            rx.vstack(
                rx.hstack(
                    rx.text("Temperatura:", weight="bold", size="3"),
                    rx.text(
                        rx.cond(
                            (invernadero["is_active"]) & (invernadero["temperatura"] != None),
                            f"{invernadero['temperatura']:.1f} %",
                            "--"
                        ),
                        size="3",
                        color=rx.cond(invernadero["is_active"], "green", "gray"),
                    ),
                    spacing="2"
                ),
                rx.hstack(
                    rx.text("Humedad:", weight="bold", size="3"),
                    rx.text(
                        rx.cond(
                            (invernadero["is_active"]) & (invernadero["humedad"] != None),
                            f"{invernadero['humedad']:.1f} %",
                            "--"
                        ),
                        size="3",
                        color=rx.cond(invernadero["is_active"], "green", "gray"),
                    ),
                    spacing="2"
                ),
                rx.hstack(
                    rx.text("Nivel de agua:", weight="bold", size="3"),
                    rx.text(
                        rx.cond(
                            (invernadero["is_active"]) & (invernadero["nivel_agua"] != None),
                            f"{invernadero['nivel_agua']:.1f} %",
                            "--"
                        ),
                        size="3",
                        color=rx.cond(invernadero["is_active"], "green", "gray"),
                    ),
                    spacing="2"
                ),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            
            rx.cond(
                invernadero["is_active"],
                rx.box(
                    rx.divider(margin_y="0.5em"),
                    rx.text(
                        f"Rangos: {invernadero['temp_min']}-{invernadero['temp_max']}°C | "
                        f"{invernadero['hum_min']}-{invernadero['hum_max']}%",
                        size="1",
                        color="gray"
                    )
                )
            ),
            spacing="3",
            align_items="start",
            width="100%"
        ),
        size="3",
        width="300px",
        height="auto"
    )
    
def tarjeta_principal() -> rx.Component:
    return rx.card(
        rx.center(
            rx.vstack(
                rx.icon_button(
                    rx.icon("plus", size=40),
                    size="4",
                    variant="ghost",
                    color_scheme="blue",
                    on_click=GreenhouseState.abrir_dialogo,
                    cursor="pointer",
                ),
                rx.text(
                    "Agregar Invernadero",
                    size="2",
                    color="gray"
                ),
                spacing="2",
                align_items="center",
            ),
            height="100%",
        ),
        size="3",
        width="300px",
        height="250px",
        style={
            "cursor": "pointer",
            "border": "2px dashed var(--gray-6)",
            ":hover":{
                "border-color": "var(--blue-9)",
                "background": "var(--gray-2)"
            }
        },
        on_click=GreenhouseState.abrir_dialogo
    )
    
def modal_formulario() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            formulario_invernadero(),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                        on_click=[
                            PlantState.limpiar_formulario,
                            GreenhouseState.cerrar_dialogo
                            
                        ]
                    ),
                ),
                rx.spacer(),
                rx.button(
                    "Guardar",
                    on_click=[
                        PlantState.guardar_planta,
                        GreenhouseState.cerrar_dialogo,
                        GreenhouseState.cargar_invernaderos,
                    ],
                    disabled=PlantState.is_loading,
                    color_scheme="green",
                ),
                spacing="3",
                margin_top="2em",
            ),
            max_width="500px",
            padding="2em",
        ),
        open=GreenhouseState.mostrar_dialogo,
        on_open_change=GreenhouseState.set_mostrar_dialogo,
    )

def pagina_invernadero() -> rx.Component:
    autenticado_view = rx.container(
        rx.hstack(
            rx.drawer.trigger(rx.button("☰")),
            rx.color_mode.button(),
            width="100%",
            justify="between",
            padding_bottom="1em",
        ),
        rx.heading("INVERNADEROS", size="9", text_align="center", margin_top="40px", margin_bottom="20px"),
        
        modal_formulario(),
        
        rx.grid(
            tarjeta_principal(),
            rx.foreach(GreenhouseState.invernaderos, tarjeta_invernadero),
            columns="3",
            spacing="4",
            width="100%",
            responsive={
                "0px": {"columns": "1"},
                "768px": {"columns": "2"},
                "1024px": {"columns": "3"},
            }
        ),
             
        rx.cond(
            GreenhouseState.mensaje != "",
            rx.callout(
                GreenhouseState.mensaje,
                icon="info",
                color_scheme="blue",
                margin_top="2em"
            )
        ),
            
        padding="2em",
        on_mount=GreenhouseState.cargar_invernaderos
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
    ),