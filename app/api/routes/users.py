from fastapi import APIRouter, Depends, HTTPException, Path, Body
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.models.user import UserCreate, UserPublic

from app.db.repositories.users import UsersRepository

router = APIRouter()


@router("/", response_model=UserPublic, name="users:register-new-user", status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    created_user = await users_repo.create_user(new_user=new_user)

    return created_user
