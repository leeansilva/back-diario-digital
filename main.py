from fastapi import FastAPI, Depends
import uvicorn
from routes.Noticias import REGISTROS
from routes.Usuarios import USUARIOS
from db.sqlite import CrearTablas,get_session
from sqlmodel import Session
app = FastAPI()
app.include_router(REGISTROS)
app.include_router(USUARIOS)

CrearTablas()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    # webbrowser.open('http://127.0.0.1:8000/docs')
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)