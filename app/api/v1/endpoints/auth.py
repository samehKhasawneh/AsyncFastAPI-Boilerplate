from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.crud.user import crud_user
from app.schemas.user import ResetPasswordConfirm, ResetPasswordRequest, User, UserCreate, UserLogin, UserPassword
from app.schemas.token import RefreshToken, Token
from app.core.security import create_reset_token, generate_tokens, get_password_hash, validate_refresh_token, verify_reset_token
from app.api.deps import get_current_user, get_db

router = APIRouter()


@router.post("/signup", response_model=User)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    filters = {
        "email":(user_in.email, "=")
    }
    user = await crud_user.search(db=db, filters=filters, single_result=True)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    try:
        user = await crud_user.create(db, obj_in=user_in)
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The phone number already exists in the system.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An integrity error occurred.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred",
        )

    return user
    

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await crud_user.authenticate(db, email=user_in.email, password=user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is inactive",
        )
    access_token, refresh_token = generate_tokens(sub=user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=Token)
async def refresh_token(token: RefreshToken, db: AsyncSession = Depends(get_db)):
    user_id = validate_refresh_token(token.refresh_token)

    user = await crud_user.get(db=db, id=user_id)
    if not user or not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive",
        )

    access_token, refresh_token = generate_tokens(sub=user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/forget-password", response_model=dict)
async def forget_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    filters = {
        "email":(request.email, "=")
    }
    user = await crud_user.search(db=db, filters=filters, single_result=True)
    if not user or not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive",
        )

    reset_token = create_reset_token(user.email)
    print(f"reset_token {reset_token}")
    # send_reset_email(user.email, reset_token)
    return {"message": "Password reset email sent."}


@router.post("/reset-password", response_model=dict)
async def reset_password(confirm: ResetPasswordConfirm, db: AsyncSession = Depends(get_db)):
    email = verify_reset_token(confirm.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token.",
        )
    filters = {
        "email":(email, "=")
    }
    user = await crud_user.search(db=db, filters=filters, single_result=True)
    if not user or not user.isActive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive",
        )


    hashed_password = get_password_hash(confirm.new_password)

    updated_user_password = UserPassword(
        passwordHash = hashed_password
    )
    _ = await crud_user.update(db=db, db_obj=user, obj_in=updated_user_password.dict())
    return {"message": "Password has been reset successfully."}