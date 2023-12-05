from fastapi import HTTPException
from sqlmodel import SQLModel, Session, Field, select, desc
from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc

# TODO: hacer que sea hashed password

class UsuarioCreacion(SQLModel):
    nombre: Optional[str]
    email: Optional[str]
    password: Optional[str]
    img_perfil: Optional[str]
    disabled: Optional[str]

class UsuarioModificacion(SQLModel):
    nombre: Optional[str]
    email: Optional[str]
    password: Optional[str]
    img_perfil: Optional[str]

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    password: str
    img_perfil: Optional[str] = Field(default=None)
    disabled: Optional[str]

    @classmethod
    def ConsultarTodo(cls, session: Session):
        query = select(cls).order_by(desc(cls.id))
        listaUsuarios = session.exec(query).all()
        return listaUsuarios

    @classmethod
    def Consultar(cls, name: str, session: Session):
        usuario = session.query(cls).filter(cls.nombre == name).first()
        if usuario:
            return usuario
        else:
            raise HTTPException(
                status_code=404, detail=f'No se encuentra el usuario en la base : ID {name}')

    @classmethod
    def Crear(cls, usuario: UsuarioCreacion, session: Session):
        usuario_db = session.query(cls).filter(
            cls.nombre == usuario.nombre).all()
        nuevoUsuario = cls.from_orm(usuario)
        if (usuario_db == []):
            session.add(nuevoUsuario)
            session.commit()
            session.refresh(nuevoUsuario)
            return nuevoUsuario
        else:
            return 'Ese nombre de usuario ya existe.'

    @classmethod
    def Modificar(cls, name: str, usuarioModificado: UsuarioModificacion, session: Session):
        usuario_db = session.query(cls).filter(cls.nombre == name).first()
        print(f"Valor de 'name': {name}")
        if usuario_db:
            usuario_data = usuarioModificado.dict(exclude_unset=True)
            for clave, valor in usuario_data.items():
                setattr(usuario_db, clave, valor)
            session.add(usuario_db)
            session.commit()
            session.refresh(usuario_db)
            return usuario_db
        else:
            raise HTTPException(
                status_code=404, detail=f'No se encuentra al usuario solicitado : ID {name}')

    @classmethod
    def Borrar(cls, id: int, session: Session):
        usuario = session.get(cls, int(id))
        if usuario:
            session.delete(usuario)
            session.commit()
            return {'status': '200 OK'}
        else:
            raise HTTPException(
                status_code=404, detail=f'No se encuentra al usuario solicitado : ID {id}')
