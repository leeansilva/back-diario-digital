from fastapi import HTTPException
from sqlmodel import SQLModel, Session, Field, select, desc
from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc

class ElementoHistoriaCreacion(SQLModel):
    noticia_id: str
    tipo: Optional[str]
    descripcion: str

class ElementoHistoriaModificacion(SQLModel):
    noticia_id: str
    tipo: Optional[str]
    descripcion: str

class ElementoHistoria(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    noticia_id: str
    tipo: Optional[str]
    descripcion: str
    formato: str
    url: str
    fecha_inicial: Optional[datetime] = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def ConsultarTodo(cls, session : Session):
        query = select(cls).order_by(desc(cls.fecha_actualizacion))
        listaHistorias = session.exec(query).all()
        return listaHistorias

    # @classmethod
    # def Consultar(id : int, session : Session):
    # 	incidencia = session.get(cls,int(id))
    # 	if incidencia : return incidencia
    # 	else : raise HTTPException(status_code=404, detail=f'No se encuentra la incidencia solicitada : ID {id}')

    @classmethod
    def Crear(cls,elemento : ElementoHistoriaCreacion, session : Session):
        nuevoElemento = cls.from_orm(elemento)
        print(nuevoElemento)
        session.add(nuevoElemento)
        session.commit()
        session.refresh(nuevoElemento)
        return nuevoElemento

    @classmethod
    def Modificar(cls,id : int, elementoHistoriaModificado : ElementoHistoriaModificacion, session : Session):
        elemento_db = session.get(cls, int(id))
        if elemento_db :
            historia_data = elementoHistoriaModificado.dict(exclude_unset=True)
            for clave, valor in historia_data.items():
                setattr(elemento_db, clave, valor)
            elemento_db.fecha_actualizacion = datetime.utcnow()
            session.add(elemento_db)
            session.commit()
            session.refresh(elemento_db)
            return elemento_db
        else : raise HTTPException(status_code=404, detail=f'No se encuentra la historia solicitada : ID {id}')

    @classmethod
    def Borrar(cls, id: int, session : Session):
        elemento_db = session.get(cls,int(id))
        if elemento_db:
            session.delete(elemento_db)
            session.commit()
            return {'status': '200 OK'}
        else : raise HTTPException(status_code=404, detail=f'No se encuentra la historia solicitada : ID {id}')