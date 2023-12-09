from fastapi import HTTPException
from sqlmodel import SQLModel, Session, Field, select, desc  
from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc
import json

class Componente():
    subtitulo: str
    descripcion: str

class HistoriaCreacion(SQLModel):
    titulo: str 
    componentes: str
    imagen: str
    fuente: str

class HistoriaModificacion(SQLModel):
    titulo: Optional[str] 
    componentes: Optional[str] 
    imagen: str
    fuente: Optional[str] 

class Historia(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    titulo: str 
    componentes: str 
    imagen: str
    fuente: str 
    fecha_inicial: Optional[datetime] = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)
    
    @classmethod
    def ConsultarTodo(cls, session : Session):
        query = select(cls).order_by(desc(cls.fecha_actualizacion))
        listaHistorias = session.exec(query).all()
        return listaHistorias
    
    @classmethod
    def Consultar(cls, id: int, session: Session):
        historia = session.get(cls, int(id))
        if historia:
            return historia
        else:
            raise HTTPException(status_code=404, detail=f'No se encuentra la historia solicitada : ID {id}')

        
    @classmethod
    def Crear(cls,historia : HistoriaCreacion, session : Session):
        nuevaHistoria = cls.from_orm(historia)
        componentes_recibidos= json.loads(nuevaHistoria.componentes)
        subtitulos = []
        descripciones = []

        for componente in componentes_recibidos:
            subtitulo = componente.get('subtitulo')
            descripcion = componente.get('descripcion')
            
            if subtitulo is not None:
                subtitulos.append(subtitulo)
                
            if descripcion is not None:
                descripciones.append(descripcion)

        if subtitulos == [] or descripciones == []:
            raise HTTPException(status_code=422, detail="El campo 'componentes' debe ser una lista de objetos con las claves 'subtitulo' y 'descripcion' como mínimo. [{'subtitulo': 'Ejemplo Subtitulo'}, {'descripcion': 'Ejemplo Descripcion'}]")

        session.add(nuevaHistoria)
        session.commit()
        session.refresh(nuevaHistoria)
        return nuevaHistoria

    @classmethod
    def Modificar(cls,id : int, historiaModificada : HistoriaModificacion, session : Session):
        historia_db = session.get(cls, int(id))
        if historia_db :
            historia_data = historiaModificada.dict(exclude_unset=True)
            for clave, valor in historia_data.items():
                setattr(historia_db, clave, valor)
            historia_db.fecha_actualizacion = datetime.utcnow()
            session.add(historia_db)
            session.commit()
            session.refresh(historia_db)
            return historia_db
        else : raise HTTPException(status_code=404, detail=f'No se encuentra la historia solicitada : ID {id}')

    @classmethod
    def Borrar(cls, id: int, session : Session):
        historia = session.get(cls,int(id))
        if historia:
            session.delete(historia)
            session.commit()
            return {'status': '200 OK'}
        else : raise HTTPException(status_code=404, detail=f'No se encuentra la historia solicitada : ID {id}')