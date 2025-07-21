from fastapi import APIRouter
from app.config.db import user_collection
from app.models.user import User
router = APIRouter()


@router.get('/')
async def get_user():
    user_data = User(
        username='Ahmad',
        email='ahmad@gmail.com',
        password='12345678'
    )
    data = await user_collection.insert_one(user_data.model_dump(mode='json', by_alias=True))
    
    return {'message': 'USER GET', 'data': str(data)}