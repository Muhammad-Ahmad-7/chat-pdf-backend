from fastapi import FastAPI
from app.routes.pdf import router as pdf_router
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.config.middleware import AuthMiddleWare

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://chat-ai-pdf-ten.vercel.app"],  # Replace with your frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleWare)

app.include_router(pdf_router, prefix='/pdf')
app.include_router(user_router, prefix='/user')
app.include_router(auth_router, prefix='/auth')


@app.get('/')
def hello():
    return {'message': 'WELCOME TO CHAT PDF'}
