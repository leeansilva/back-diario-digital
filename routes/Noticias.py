from sqlmodel import Session
from fastapi import APIRouter, File, UploadFile, Depends, Header, Response, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from db.sqlite import get_session
from db.models.Historias import (Historia, HistoriaCreacion, HistoriaModificacion)

REGISTROS = APIRouter(
    prefix='/backend/registros',
    tags=["Registros Moreno"]
)

@REGISTROS.get('/registros/all')
def getAllREGISTROS(session: Session = Depends(get_session)):
    return Historia.ConsultarTodo(session)

# @REGISTROS.get('/registros/{id}')
# def getRegistro(id: int, session: Session = Depends(get_session)):
#     return Historia.Consultar(id, session)

@REGISTROS.post('/registros')
def createRegistro(registro: HistoriaCreacion, session: Session = Depends(get_session)):
    return Historia.Crear(registro, session)

@REGISTROS.put('/registros/{id}')
def getAllRegistro(id: int, registro: HistoriaModificacion, session: Session = Depends(get_session)):
    return Historia.Modificar(id, registro, session)

@REGISTROS.delete('/registros/{id}')
def deleteRegistro(id: int, session: Session = Depends(get_session)):
    return Historia.Borrar(id, session)
