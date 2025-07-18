from fastapi import FastAPI
from app.routes.pdf import router as pdf_router
app = FastAPI()

app.include_router(pdf_router, prefix='/pdf')


@app.get('/')
def hello():
    return {'message': 'WELCOME TO CHAT PDF'}
