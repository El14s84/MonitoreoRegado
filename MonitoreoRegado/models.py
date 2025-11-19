from datetime import datetime
from typing import List, Optional
import reflex as rx
from sqlmodel import Field, Relationship, SQLModel

class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str = Field(unique=True)
    
    usuarios: List["Usuario"] = Relationship(back_populates="rol")
    
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rol_id: Optional[int] = Field(default=None, foreign_key="rol.id")
    rol: Optional[Rol] = Relationship(back_populates="usuarios")
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)