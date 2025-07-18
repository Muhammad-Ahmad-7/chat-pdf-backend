from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_pdf():
    return {'message': 'PDF IS UPLOADED'}
