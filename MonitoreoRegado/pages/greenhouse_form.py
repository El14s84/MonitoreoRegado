import reflex as rx
from MonitoreoRegado.state.plant_state import PlantState
from MonitoreoRegado.state.greenhouse_state import GreenhouseState

def formulario_invernadero() -> rx.Component:
    return rx.vstack(
            rx.heading(
                "Agregar Nueva Planta",
                size="6"
            ),
            rx.text(
                "Completa los datos para crear un nuevo invernadero",
                size="2",
                color="gray"
            ),
                
            rx.divider(),
                
            rx.vstack(
                rx.vstack(
                    rx.text("Nombre de la planta", size="2", weight="bold"),
                    rx.input(
                        placeholder="Ej: Mi Tomate del Balcón",
                        value=PlantState.nombre_planta,
                        on_change=PlantState.set_nombre_planta,
                        width="100%"
                    ),
                    rx.text(
                        "Este es el nombre que aparecerá en tu invernadero",
                        size="1",
                        color="gray"
                    ),
                    spacing="1",
                    width="100%"
                ),
                    
                rx.vstack(
                    rx.text("Tipo de planta", size="2", weight="bold"),
                    rx.select(
                        PlantState.plantas_disponibles,
                        placeholder="Selecciona un tipo",
                        value=PlantState.tipo_planta_seleccionado,
                        on_change=PlantState.set_tipo_planta_seleccionado,
                        width="100%"
                    ),
                    rx.text(
                        "Los rangos se completarán automáticamente",
                        size="1",
                        color="gray"
                    ),
                    spacing="1",
                    width="100%"
                ),
                    
                rx.cond(
                    PlantState.tipo_planta_seleccionado != "",
                    rx.vstack(
                        rx.text("Rangos de Temperatura", size="2", weight="bold"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Mínima (°C)", size="1"),
                                rx.input(
                                    type="number",
                                    value=PlantState.temp_min,
                                    on_change=PlantState.set_temp_min,
                                    width="100%"
                                ),
                                spacing="1",
                                flex="1"
                            ),
                            rx.text("—", margin_top="1.5em"),
                            rx.vstack(
                                rx.text("Máxima (°C)", size="1"),
                                rx.input(
                                    type="number",
                                    value=PlantState.temp_max,
                                    on_change=PlantState.set_temp_max,
                                    width="100%"
                                ),
                                spacing="1",
                                flex="1"
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        spacing="2",
                        width="100%"
                    )
                ),
                rx.cond(
                    PlantState.tipo_planta_seleccionado != "",
                    rx.vstack(
                        rx.text("Rangos de Humedad", size="2", weight="bold"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Mínima (%)", size="1"),
                                rx.input(
                                    type="number",
                                    value=PlantState.hum_min,
                                    on_change=PlantState.set_hum_min,
                                    width="100%"
                                ),
                                spacing="1",
                                flex="1"
                            ),
                            rx.text("—", margin_top="1.5em"),
                            rx.vstack(
                                rx.text("Máxima (%)", size="1"),
                                rx.input(
                                    type="number",
                                    value=PlantState.hum_max,
                                    on_change=PlantState.set_hum_max,
                                    width="100%"
                                ),
                                spacing="1",
                                flex="1"
                            ),
                            spacing="2",
                            width="100%"
                        ),
                        spacing="2",
                        width="100%"
                    )
                ),
                    
                rx.cond(
                    PlantState.mensaje != "",
                    rx.callout(
                        PlantState.mensaje,
                        icon="info",
                        color_scheme="blue" if "exitosamente" else "red",
                        margin_top="1em"
                    )
                ),
                    
                spacing="4",
                width="100%"
            ),  
            spacing="4",
            width="100%"
        )
