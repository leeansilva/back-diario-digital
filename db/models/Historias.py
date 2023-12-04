from fastapi import HTTPException
from sqlmodel import SQLModel, Session, Field, select, desc  
from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc

class HistoriaCreacion(SQLModel):
    titulo: str 
    subtitulo: Optional[str]
    descripcion: str
    fuente: str

class HistoriaModificacion(SQLModel):
    titulo: Optional[str] 
    subtitulo: Optional[str] 
    descripcion: Optional[str] 
    fuente: Optional[str] 

class Historia(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    titulo: str 
    subtitulo: Optional[str] 
    descripcion: str 
    fuente: str 
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
    def Crear(cls,historia : HistoriaCreacion, session : Session):
        nuevaHistoria = cls.from_orm(historia)
        print(nuevaHistoria)
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