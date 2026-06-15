from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.db.dependencies import get_db
from app.services.user_services import create_user


from app.schemas.user import LoginRequest
from app.services.user_services import authenticate_user
from app.core.security import create_access_token

from app.core.current_user import get_current_user
from app.models.user import User


router = APIRouter()

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email
    }



@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        new_user = create_user(
            db=db,
            name=user.name,
            email=user.email,
            password=user.password
        )

        return {
            "id": str(new_user.id),
            "name": new_user.name,
            "email": new_user.email
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        request.email,
        request.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }