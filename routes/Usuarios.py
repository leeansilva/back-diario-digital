from sqlmodel import Session
from fastapi import APIRouter, File, UploadFile, Depends, Header, Response, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from db.sqlite import get_session
from db.models.Usuarios import (Usuario, UsuarioCreacion, UsuarioModificacion)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

USUARIOS = APIRouter(
    tags=["Usuarios diario digital"]
)
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer("/token")

#crear jwt
def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes = 30)
    else:
        expires = datetime.utcnow() + time_expire

    data_copy.update({'exp':expires})
    jwt_token = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

#Verificamos que el usuario tenga los permisos requeridos:
def get_user_current(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get('sub')
        if username == None:
            raise HTTPException(status_code = 401, detail='Credencial invalida.', headers={'WWW-Authenticate': 'Bearer'})
    except JWTError:
        raise HTTPException(status_code = 401, detail='Credencial invalida.', headers={'WWW-Authenticate': 'Bearer'})

    usuario = Usuario.Consultar(username, session)
    if usuario.disabled != 'false':
        raise HTTPException(status_code = 400, detail = 'Usuario sin permisos')
    return usuario

#testeando la seguridad:
@USUARIOS.get("/usuarios/me")
def user(usuario : str = Depends(get_user_current)):
    return usuario

#1er filtro para acceder al token:
@USUARIOS.post('/token')
def authUser(session: Session = Depends(get_session),form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = Usuario.Consultar(form_data.username, session)
    access_token_expires = timedelta(minutes = 30)
    access_token_jwt = create_token({'sub':usuario.nombre},access_token_expires)
    if not usuario:
        raise HTTPException(status_code = 401, detail='Usuario inválido.', headers={'WWW-Authenticate': 'Bearer'})
    if not usuario.password == form_data.password:
        raise HTTPException(status_code = 401, detail='Contraseña inválida.', headers={'WWW-Authenticate': 'Bearer'})
    return {
        'access_token' : access_token_jwt,
        'token_type' : 'bearer',
        'user': usuario
    }

@USUARIOS.get('/usuarios/all')
def getAllREGISTROS(session: Session = Depends(get_session),usuario_activo : str = Depends(get_user_current)):
    return Usuario.ConsultarTodo(session)

@USUARIOS.get('/usuarios/{name}')
def getUsuario(name: str, session: Session = Depends(get_session), usuario_activo : str = Depends(get_user_current)):
    usuario = Usuario.Consultar(name, session)
    return usuario

@USUARIOS.post('/usuarios')
def createUsuario(usuario: UsuarioCreacion, session: Session = Depends(get_session),usuario_activo : str = Depends(get_user_current)):
    usuario = Usuario.Crear(usuario, session)
    return usuario

@USUARIOS.put('/usuarios/{name}')
def modUsuario(name: str, usuario: UsuarioModificacion, session: Session = Depends(get_session),usuario_activo : str = Depends(get_user_current)):
    return Usuario.Modificar(name, usuario, session)

@USUARIOS.delete('/usuarios/{name}')
def deleteUsuario(id: int, session: Session = Depends(get_session),usuario_activo : str = Depends(get_user_current)):
    return Usuario.Borrar(id, session)
