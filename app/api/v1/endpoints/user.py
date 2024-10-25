from app.models.user import OrganizationStatus
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import crud_user
from app.schemas.user import User, UserUpdate, UserRole
from app.api.deps import get_current_user, get_db

router = APIRouter()


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.SYSTEM_ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform user delete",
        )
    
    user = await crud_user.get(db=db, id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    _ = await crud_user.delete(db=db, id=user_id)

    return {"message": "User has been deleted successfully."}


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.SYSTEM_ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update users",
        )
    user = await crud_user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_in.dict(exclude_unset=True)
    _ =  await crud_user.update(db=db, db_obj=user, obj_in=update_data)

    return {"message": "User has been updated successfully."}