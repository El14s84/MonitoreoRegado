import reflex as rx

def navbar() -> rx.Component:
    return rx.hstack(
        rx.link("Inicio", href="/monitoreo"),
        rx.link("Invernadero", href="/greenhouse"),
        rx.link("Calendario", href="/calendario"),
        spacing="4",
        justify="center",
        padding="12px",
        background="gray.100",
        border_radius="md",
        width="100%",
    )

def loginNavbar() -> rx.Component:
    return rx.hstack(
        rx.link("Login", href="/"),
        rx.link("Registro", href="/registro"),
        spacing="4",
        justify="center",
        padding="12px",
        background="gray.100",
        border_radius="md",
        width="100%",
    )