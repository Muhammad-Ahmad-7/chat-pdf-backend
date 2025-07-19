from fastapi import FastAPI
from app.routes.pdf import router as pdf_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_router, prefix='/pdf')


@app.get('/')
def hello():
    return {'message': 'WELCOME TO CHAT PDF'}
