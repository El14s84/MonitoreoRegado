import reflex as rx
from MonitoreoRegado.autenticar import State, required_auth

def auth_card(title: str, on_submit,
              show_confirm: bool = False, show_rol: bool = False) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="7"),
            rx.cond(
                show_rol,
                rx.input(
                    placeholder="Nombre",
                    value=State.name,
                    on_change=State.set_name,
                    width="100%",
                ),
            ),
            rx.input(
                placeholder="aquí@túemail.com",
                type="email",
                value=State.email,
                on_change=State.set_email,
                width="100%",
            ),
            rx.cond(
                show_rol,
                rx.select(
                    ["admin", "usuario"],
                    value=State.rol,
                    on_change=State.set_rol,
                    placeholder="Seleccionar Rol",
                    width="100%",
                ),
            ),
            rx.input(
                placeholder="contraseña",
                type="password",
                value=State.password,
                on_change=State.set_password,
                width="100%",
            ),
            rx.cond(
                show_confirm,
                rx.input(
                    placeholder="Repite tu contraseña",
                    type="password",
                    value=State.confirmacion_password,
                    on_change=State.set_confirmacion_password,
                    width="100%",
                ),
            ),
            rx.button(title, on_click=on_submit, width="100%"),
            rx.cond(
                State.error_registro != "",
                rx.text(State.error_registro, color="red"),
            ),
            rx.cond(
                State.error_login != "",
                rx.text(State.error_login, color="red"),
            ),
            rx.cond(
                State.logro_registro != "",
                rx.text(State.logro_registro, color="green"),
            ),
            rx.cond(
                State.logro_login != "",
                rx.text(State.logro_login, color="green"),
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
        max_width="420px",
        padding="24px",
    )
    
def navbar() -> rx.Component:
    return rx.hstack(
        rx.link("Inicio", href="/"),
        rx.link("Registro", href="/registro"),
        rx.link("Login", href="/login"),
        spacing="4",
        justify="center",
        padding="12px",
        background="gray.100",
        border_radius="md",
        width="100%",
    )

def index() -> rx.Component:
    
    State.datos_iniciales()
    
    return rx.container(
        rx.color_mode.button(position="top-left"),
        navbar(),
        rx.vstack(
            rx.heading("HOLAAA", size="9"),
            rx.text(
                "Bbiieennvveenniiddoo",
                size="5",
            ),
            spacing="5",
            justify="center",
            min_height="60vh",
        ),
    )

def pagina_registro() -> rx.Component:
    return rx.container(
        navbar(),
        rx.flex(
            auth_card("Registrarme", State.ingreso, show_confirm=True, show_rol=True),
            wrap="wrap",
            gap="24px",
            justify="center",
        ),
        padding_y="40px",
    )

def pagina_login() -> rx.Component:
    return rx.container(
        navbar(),
        rx.flex(
            auth_card("Iniciar sesión", State.login, show_confirm=False, show_rol=False),
            wrap="wrap",
            gap="24px",
            justify="center",
        ),
        padding_y="40px",
    )

def dashboard() -> rx.Component:
    return rx.cond(
        State.correcta_autenticacion,
        rx.container(
            rx.vstack(
                rx.heading("Dashboard", size="9"),
                rx.text("Bienvenido al área privada", size="5"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=State.logout,
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
                    href="/login"
                ),
                spacing="5",
                justify="center",
                min_height="60vh",
            ),
        )
    )

app = rx.App()
app.add_page(index, route="/")
app.add_page(pagina_registro, route="/registro", title="Registro")
app.add_page(pagina_login, route="/login", title="Login")
app.add_page(dashboard, route="/dashboard", title="Dashboard")
