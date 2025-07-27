from fastapi import APIRouter, Request
from app.config.db import user_collection
from app.models.user import User
from bson import ObjectId
from app.config.utils import success_response
router = APIRouter()


@router.get('/get-user')
async def get_user(request: Request):
    user_id = request.state.user_id
    
    try:
        user = await user_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return {'message': "User not found", "status": 400}
        user['_id'] = str(user['_id'])
        res_user = {
            '_id':str(user['_id']),
            'username': user.get('username'),
            'email': user.get('email')
        }
        return success_response(status_code=200, data=res_user, message="User Found Successfully")
    except Exception:
        return Exception