import reflex as rx
from MonitoreoRegado.state.auth_state import AuthState

def auth_card(title: str, on_submit,
              show_confirm: bool = False, show_rol: bool = False) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="7"),
            rx.cond(
                show_rol,
                rx.input(
                    placeholder="Nombre",
                    value=AuthState.name,
                    on_change=AuthState.set_name,
                    width="100%",
                ),
            ),
            rx.input(
                placeholder="aquí@túemail.com",
                type="email",
                value=AuthState.email,
                on_change=AuthState.set_email,
                width="100%",
            ),
            rx.cond(
                show_rol,
                rx.select(
                    ["admin", "usuario"],
                    value=AuthState.rol,
                    on_change=AuthState.set_rol,
                    placeholder="Seleccionar Rol",
                    width="100%",
                ),
            ),
            rx.input(
                placeholder="contraseña",
                type="password",
                value=AuthState.password,
                on_change=AuthState.set_password,
                width="100%",
            ),
            rx.cond(
                show_confirm,
                rx.input(
                    placeholder="Repite tu contraseña",
                    type="password",
                    value=AuthState.confirmacion_password,
                    on_change=AuthState.set_confirmacion_password,
                    width="100%",
                ),
            ),
            rx.button(title, on_click=on_submit, width="100%"),
            rx.cond(
                AuthState.error_registro != "",
                rx.text(AuthState.error_registro, color="red"),
            ),
            rx.cond(
                AuthState.error_login != "",
                rx.text(AuthState.error_login, color="red"),
            ),
            rx.cond(
                AuthState.logro_registro != "",
                rx.text(AuthState.logro_registro, color="green"),
            ),
            rx.cond(
                AuthState.logro_login != "",
                rx.text(AuthState.logro_login, color="green"),
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
        max_width="420px",
        padding="24px",
    )
