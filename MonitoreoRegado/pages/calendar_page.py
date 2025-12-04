import reflex as rx
from MonitoreoRegado.state.calendar_state import CalendarState, ProgramacionData
from MonitoreoRegado.state.auth_state import AuthState
from MonitoreoRegado.components.drawer import drawer_content

def encabezado_calendario() -> rx.Component:
    return rx.hstack(
        rx.heading(
            "Calendario de Riego",
            size="9",
            color="white",
            font_weight="700",
        ),
        
        rx.spacer(),
        
        rx.button(
            rx.icon("plus", size=20),
            "Programar Riego",
            on_click=CalendarState.abrir_formulario,
            size="3",
            color_scheme="green",
            cursor="pointer",
        ),
        
        width="100%",
        align="center",
    )
    
def lista_programaciones() -> rx.Component:
    return rx.box(
        rx.cond(
            CalendarState.programaciones.length == 0,
            rx.center(
                rx.vstack(
                    rx.icon("calendar-x", size=60, color="rgba(255,255,255,0.5)"),
                    rx.text(
                        "No hay programaciones registradas",
                        font_size="1.2rem",
                        color="rgba(255,255,255,0.7)",
                    ),
                    rx.text(
                        "Haz clic en 'Programar Riego' para comenzar",
                        font_size="0.9rem",
                        color="rgba(255,255,255,0.5)",
                    ),
                    spacing="1",
                    align="center",
                ),
                padding="4rem",
            ),
            
            rx.vstack(
                rx.foreach(
                    CalendarState.programaciones,
                    tarjeta_programacion
                ),
                spacing="1",
                width="100%"
            )
        ),
        width="100%",
    )
    
def tarjeta_programacion(prog: ProgramacionData) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.badge(
                        prog.dia_semana,
                        color_scheme="blue",
                        size="2",
                    ),
                    rx.badge(
                        prog.invernadero_nombre,
                        color_scheme="purple",
                        size="2",
                    ),
                    spacing="1",
                ),
                
                rx.hstack(
                    rx.icon("clock", size=16, color="rgba(255,255,255,0.7)"),
                    rx.text(
                        f"{prog.hora_inicial} - {prog.hora_final}",
                        font_size="1.1rem",
                        font_weight="600",
                        color="white",
                    ),
                    spacing="1",
                ),
                
                rx.cond(
                    prog.ultima_confirmacion,
                    rx.text(
                        f"Última confirmación: {prog.ultima_confirmacion}",
                        font_size="0.8rem",
                        color="rgba(255,255,255,0.5)",
                    ),
                    rx.text(
                        "Sin confirmar aún",
                        font_size="0.8rem",
                        color="rgba(255,255,255,0.5)",
                    ),
                ),
                
                align_items="start",
                spacing="1",
            ),
            
            rx.hstack(
                rx.button(
                    rx.icon("check", size=18),
                    "Confirmar",
                    on_click=lambda: CalendarState.confirmar_programacion(prog.id),
                    size="2",
                    color_scheme="green",
                    disabled=~prog.necesita_confirmacion,
                    cursor="pointer",
                ),
                
                rx.button(
                    rx.icon("pencil", size=18),
                    on_click=lambda: CalendarState.editar_programacion(prog.id),
                    size="2",
                    color_scheme="blue",
                    cursor="pointer",
                ),
                
                rx.button(
                    rx.icon("trash-2", size=18),
                    on_click=lambda: CalendarState.eliminar_programacion(prog.id),
                    size="2",
                    color_scheme="red",
                    cursor="pointer",
                ),
                
                spacing="1",
            ),
            
            width="100%",
            align="center",
            padding="1.5rem"
        ),
    )
    
def modal_formulario() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.heading(
                    rx.cond(
                        CalendarState.editando_id,
                        "Editar Programación",
                        "Nueva Programación",
                    ),
                    size="6",
                    margin_bottom="1rem",
                ),
                
                rx.cond(
                    CalendarState.mensaje_error != "",
                    rx.callout(
                        CalendarState.mensaje_error,
                        icon="circle-alert",
                        color_scheme="red",
                        size="2",
                        margin_bottom="1rem",
                    ),
                ),
                
                formulario_programacion(),
                
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            color_scheme="gray",
                            size="2",
                            on_click=CalendarState.cerrar_formulario,
                        ),
                    ),
                    rx.button(
                        rx.cond(
                            CalendarState.editando_id,
                            "Guardar Cambios",
                            "Crear Programación",
                        ),
                        on_click=CalendarState.guardar_programacion,
                        size="2",
                        color_scheme="green",
                    ),
                    spacing="1",
                    justify="end",
                    width="100%",
                ),
                
                spacing="1",
                width="100%",
            ),
            max_width="500px",
        ),
        open=CalendarState.form_abierto,
        on_open_change=CalendarState.set_form_abierto,
    )
    
def formulario_programacion() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text("Invernadero", font_weight="600", font_size="0.9rem"),
            rx.el.select(
                rx.el.option("Selecciona un invernadero", value="0"),
                rx.foreach(
                    CalendarState.lista_invernadero,
                    lambda inv: rx.el.option(inv["nombre"], value=inv["id"])
                ),
                value=CalendarState.invernadero_seleccionado,
                on_change=CalendarState.set_invernadero_seleccionado,
                width="100%",
                padding="0.5rem",
            ),
            align_items="start",
            width="100%",
        ),
        
        rx.vstack(
            rx.text("Día de la semana", font_weight="600", font_size="0.9rem"),
            rx.el.select(
                rx.el.option("Selecciona un día", value="0"),
                rx.foreach(
                    CalendarState.lista_dias_semana,
                    lambda dia: rx.el.option(dia["nombre"], value=dia["id"])
                ),
                value=CalendarState.semana_seleccionada,
                on_change=CalendarState.set_semana_seleccionada,
                width="100%",
                padding="0.5rem",
            ),
            align_items="start",
            width="100%",
        ),
        
        rx.vstack(
            rx.text("Hora inicial", font_weight="600", font_size="0.9rem"),
            rx.input(
                type="time",
                value=CalendarState.hora_inicial,
                on_change=CalendarState.set_hora_inicial,
                width="100%",
            ),
            align_items="start",
            width="100%",
        ),
        
        rx.vstack(
            rx.text("Hora final", font_weight="600", font_size="0.9rem"),
            rx.input(
                type="time",
                value=CalendarState.hora_final,
                on_change=CalendarState.set_hora_final,
                width="100%",
            ),
            align_items="start",
            width="100%",
        ),
        
        spacing="1",
        width="100%",
    )
    
def notificacion_riego() -> rx.Component:
    return rx.cond(
        CalendarState.mostrar_notificacion,
        rx.box(
            rx.hstack(
                rx.icon(
                    "droplet",
                    size=30,
                    color="white",
                ),
                
                rx.vstack(
                    rx.text(
                        "¡Hora de Riego!",
                        font_weight="700",
                        font_size="1.2rem",
                        color="white",
                    ),
                    rx.text(
                        CalendarState.mensaje_notificacion,
                        font_size="0.9rem",
                        color="rgba(255,255,255,0.9)",
                    ),
                    align_items="start",
                    spacing="1",
                ),
                
                rx.spacer(),
                
                rx.vstack(
                    rx.button(
                        rx.icon("check", size=18),
                        "Confirmar",
                        on_click=lambda: CalendarState.confirmar_programacion(
                            CalendarState.notificacion_calendario_id
                        ),
                        size="2",
                        color_scheme="green",
                    ),
                    rx.button(
                        rx.icon("x", size=18),
                        on_click=CalendarState.cerrar_notificacion,
                        size="1",
                        color_scheme="gray",
                        variant="ghost",
                    ),
                    spacing="1",
                ),
                
                width="100%",
                align="center",
                padding="1rem",
            ),
        ),
    )

def pagina_calendario() -> rx.Component:
    menu_lateral = rx.drawer.root(
        rx.drawer.trigger(rx.button("☰", variant="ghost", color="white")),
        drawer_content(),
        rx.drawer.overlay(z_index="9999"), # Z-index alto para tapar todo al abrirse
        direction="left",
    )

    # 2. Vista de usuario autenticado
    autenticado_view = rx.box( # Usamos box como contenedor principal
        # Agregamos la notificación con posición fija (FLOTANTE)
        rx.box(
            notificacion_riego(),
            position="fixed",
            top="20px",
            right="20px",
            z_index="9000", # Para que flote sobre todo
        ),
        
        rx.container(
            rx.hstack(
                # Aquí ponemos el menú lateral corregido
                menu_lateral,
                rx.color_mode.button(),
                width="100%",
                justify="between",
                padding_bottom="1em",
            ),
            rx.vstack(
                encabezado_calendario(),
                lista_programaciones(),
                modal_formulario(),
                
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding="2rem",
                spacing="2", # Corregido a string "2" o "2em"
            ),
            
            # Eventos de carga
            on_mount=[
                CalendarState.iniciar_verificacion,
                CalendarState.cargar_programaciones,
                CalendarState.cargar_listas,
            ],
        ),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
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
    
    # 3. Retorno simple condicional (Ya no envuelve todo en Drawer)
    return rx.cond(
        AuthState.correcta_autenticacion,
        autenticado_view,
        no_autenticado_view,
    )