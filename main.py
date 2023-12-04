from fastapi import FastAPI
import uvicorn
from routes.Noticias import REGISTROS
from db.sqlite import CrearTablas
app = FastAPI()
app.include_router(REGISTROS)

CrearTablas()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    # webbrowser.open('http://127.0.0.1:8000/docs')
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)