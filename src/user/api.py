from collections import defaultdict
from typing import List
from fastapi import APIRouter
from src.base_crud.base_router import add_routers
from src.user.controllers import UserController
from src.user.schemas.user_schemas import GetUserDTO, GetUserAndTasksDTO

user_router = APIRouter(prefix="/user", tags=["USER"])


user_router.include_router(add_routers(UserController,
                                       response_model=defaultdict(lambda: GetUserDTO, {"get_all": List[GetUserDTO]})))

user_router.add_api_route(path="/get_user_with_tasks/{pk}", endpoint=UserController().get_user_with_tasks,
                          response_model=GetUserAndTasksDTO, methods=["get"])

user_router.add_api_route(path="/change_role/{pk}", endpoint=UserController().change_role,
                          response_model=GetUserDTO, methods=["patch"])