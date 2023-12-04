from fastapi import HTTPException
from sqlmodel import SQLModel, Session, Field, select, desc  
from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc

class Usuario(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key = True)
    nombre: str
    email: str 
    img_perfil: Optional[str] = Field(default = None)

class UsuarioCreacion(SQLModel, table = True):
    nombre: str
    email: str 
    img_perfil: Optional[str]
    
class UsuarioModificacion(SQLModel, table = True):
    nombre: str
    email: str Optional[str]
    img_perfil: Optional[str]
    
    @classmethod
    def ConsultarTodo(cls, session : Session):
        query = select(cls).order_by(desc(cls.fecha_actualizacion))
        listaUsuarios = session.exec(query).all()
        return listaHistoria
    
    @classmethod
    def Consultar(id : int, session : Session):
    	usuario = session.get(cls,int(id))
    	if usuario : return usuario
    	else : raise HTTPException(status_code=404, detail=f'No se encuentra el usuario en la base : ID {id}')

    @classmethod
    def Crear(cls,usuario : usuarioCreacion, session : Session):
        nuevoUsuario = cls.from_orm(usuario)
        print(nuevoUsuario)
        session.add(nuevoUsuario)
        session.commit()
        session.refresh(nuevoUsuario)
        return nuevoUsuario

    @classmethod
    def Modificar(cls,id : int, usuarioModificado : UsuarioModificacion, session : Session):
        usuario_db = session.get(cls, int(id))
        if usuario_db :
            historia_data = historiaModificada.dict(exclude_unset=True)
            for clave, valor in historia_data.items():
                setattr(usuario_db, clave, valor)
            usuario_db.fecha_actualizacion = datetime.utcnow()
            session.add(usuario_db)
            session.commit()
            session.refresh(usuario_db)
            return usuario_db
        else : raise HTTPException(status_code=404, detail=f'No se encuentra al usuario solicitado : ID {id}')
    
    @classmethod
    def Borrar(cls, id: int, session : Session):
        usuario = session.get(cls,int(id))
        if usuario:
            session.delete(usuario)
            session.commit()
            return {'status': '200 OK'}
        else : raise HTTPException(status_code=404, detail=f'No se encuentra al usuario solicitado : ID {id}')