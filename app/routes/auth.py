from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.validators.auth import SignupBody, SigninBody
from app.config.db import user_collection
from app.config.utils import hash_password, success_response, verify_password, create_token
router = APIRouter()


@router.post('/signup')
async def signup(user:SignupBody):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException( status_code=409, detail="User Already exist with this email")

    hashed_pwd = hash_password(user.password)
    
    new_user = User(
        email=user.email,
        password=hashed_pwd,
        username=user.username,
    )
    user = await user_collection.insert_one(new_user.model_dump(mode='json', by_alias=True))
    user = str(user.inserted_id)
    return success_response(status_code=201, message="User created successfully")


@router.post('/signin')
async def sigin(user:SigninBody):
    find_user = await user_collection.find_one({'email': user.email})
    
    print("FIND USER", find_user)
    
    if not find_user:
        raise ValueError("User does not Exist with this Email. Please Signup first")
    print("HASHED", find_user['password'])
    print("PASSWORD", user.password)
    is_password_correct = verify_password(find_user['password'], user.password)
    
    if not is_password_correct:
        raise ValueError("Email or Password is Incorrect")
    
    token = create_token(data={"_id": str(find_user['_id'])})

    return success_response(
        status_code=200,
        message="User Found Successfully",
        data={"token": token}
    )