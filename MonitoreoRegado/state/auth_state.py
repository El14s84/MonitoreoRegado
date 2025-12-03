from datetime import datetime
import reflex as rx
from sqlmodel import select
from MonitoreoRegado.models import Usuario, Rol
from MonitoreoRegado.api.auth import (
    hash_password,
    check_password,
    validar_email,
    validar_fuerte_pass,
)

ROLES = ["admin", "usuario"]

class AuthState(rx.State):
    
    def datos_iniciales(self):
        with rx.session() as session:
            try:
                roles_existentes = session.exec(select(Rol)).all()
                desc_existentes = {r.descripcion for r in roles_existentes}
                print(f"Roles encontrados: {desc_existentes}")
                
                for desc_rol in ["admin", "usuario"]:
                    if desc_rol not in desc_existentes:
                        print(f"Creando rol: {desc_rol}")
                        session.add(Rol(descripcion=desc_rol))
                
                session.commit()
                print("datos_iniciales completado")
            except Exception as e:
                print(f"Error en datos_iniciales: {e}")
    
    state_auto_setters: bool = False
    
    # Formulario
    name: str = ""
    email: str = ""
    rol: str = ""
    password: str = ""
    confirmacion_password: str = ""
    
    # Mensajes
    error_registro: str = ""
    logro_registro: str = ""
    error_login: str = ""
    logro_login: str = ""
    
    # autenticación
    usuario_id: int = 0
    correcta_autenticacion: bool = False
    
    # toma de datos
    rol_actual: str = ""
    nombre_actual: str = ""
    
    def set_name(self, name: str):
        self.name = name
    
    def set_email(self, email: str):
        self.email = email
    
    def set_rol(self, rol: str):
        self.rol = rol
    
    def set_password(self, password: str):
        self.password = password
    
    def set_confirmacion_password(self, confirmacion_password: str):
        self.confirmacion_password = confirmacion_password
    
    def limpiar(self):
        self.error_registro = ""
        self.logro_registro = ""
        self.error_login = ""
        self.logro_login = ""
    
    def _validar_inputs(self, require_fuerte_pass: bool = True,
                        require_confirm: bool = False) -> bool:
        self.error_registro = ""
        if not validar_email(self.email):
            self.error_registro = "Email invalido."
            return False
        if require_fuerte_pass and not validar_fuerte_pass(self.password):
            self.error_registro = "La contraseña debe tener 8 o más carácteres, letras y números."
            return False
        if require_confirm and self.password != self.confirmacion_password:
            self.error_registro = "Las contraseñas no coinciden."
            return False
        return True
    
    def ingreso(self):
        self.limpiar()
        if not self._validar_inputs(require_fuerte_pass=True, require_confirm=True):
            self.logro_registro = ""
            return
        
        with rx.session() as session:
            
            todos_los_roles = session.exec(select(Rol)).all()
            if not todos_los_roles:
                print("Creando roles automáticamente...")
                for desc_rol in ["admin", "usuario"]:
                    session.add(Rol(descripcion=desc_rol))
                session.commit()
                todos_los_roles = session.exec(select(Rol)).all()
                print(f"Roles creados: {[r.descripcion for r in todos_los_roles]}")
        
            
            existe = session.exec(
                select(Usuario).where(Usuario.email == self.email)
            ).first()
            if existe:
                self.error_registro = "Email ya existente."
                self.logro_registro = ""
                return
            
            print(f"DEBUG: Rol seleccionado = '{self.rol}'")
            print(f"DEBUG: Tipo de rol = {type(self.rol)}")
            
            todos_los_roles = session.exec(select(Rol)).all()
            print(f"DEBUG: Roles en BD = {[r.descripcion for r in todos_los_roles]}")
            
            seleccion_rol = session.exec(
                select(Rol).where(Rol.descripcion == self.rol)
            ).first()
            
            if not seleccion_rol:
                self.error_registro = "Rol no válido."
                self.logro_registro = ""
                return
            
            usuario = Usuario(
                name=self.name,
                email=self.email,
                password_hash=hash_password(self.password),
                is_active=True,
                rol_id=seleccion_rol.id,
                created_at=datetime.now()
            )
            session.add(usuario)
            session.commit()
            
            self.logro_registro = "¡Cuenta Creada!"
            self.error_registro = ""
            self.password = ""
            self.confirmacion_password = ""
        
    def login(self):
        self.limpiar()
        if not self._validar_inputs(require_fuerte_pass=False,
                                    require_confirm=False):
            self.logro_login = ""
            return
        
        with rx.session() as session:
            user = session.exec(
                select(Usuario).where(Usuario.email == self.email)
            ).first()
            
            if not user:
                self.error_login = "Usuario no válido."
                self.logro_login = ""
                return
            
            if not user.is_active:
                self.error_login = "Usuario no activo."
                self.logro_login = ""
                return
                
            if not check_password(self.password, user.password_hash):
                self.error_login = "Contraseña no válida."
                self.logro_login = ""
                return
        
        self.usuario_id = user.id
        self.correcta_autenticacion = True
        self.nombre_actual = user.name
        self.rol_actual = self.obtener_rol_usuario(user.id)
        self.logro_login = "¡Login exitoso!"
        self.error_login = ""
        self.password = ""
        
        print(f"Usuario '{self.nombre_actual}' con rol '{self.rol_actual}' ha iniciado sesión.")
        return rx.redirect("/monitoreo")
    
    def logout(self):
        self.usuario_id = 0
        self.correcta_autenticacion = False
        self.nombre_actual = ""
        self.rol_actual = ""
        self.name = ""
        self.email = ""
        self.password = ""
        self.confirmacion_password = ""
        self.error_login = ""
        self.logro_login = ""
        return rx.redirect("/")
    
    def get_rol_actual(self) -> str:
        return self.rol_actual
    
    def es_admin(self) -> bool:
        return self.rol_actual == "admin"
    
    def es_usuario(self) -> bool:
        return self.rol_actual == "usuario"
    
    def tiene_permiso(self, roles_permitidos: list) -> bool:
        return self.rol_actual in roles_permitidos
    
    def obtener_rol_usuario(self, usuario_id: int) -> str:
        with rx.session() as session:
            usuario = session.exec(
                select(Usuario).where(Usuario.id == usuario_id)
            ).first()
            if usuario:
                rol = session.exec(
                    select(Rol).where(Rol.id == usuario.rol_id)
                ).first()
                return rol.descripcion if rol else "usuario"
            return "usuario"