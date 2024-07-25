from collections import defaultdict
from typing import List
from fastapi_pagination import Page
from fastapi import APIRouter
from src.base_crud.base_consts import FILE_METHODS
from src.base_crud.base_router import add_routers
from src.task.controllers import TaskController, FileTaskController
from src.task.schemas.task_schemas import FileDTO, GetTaskDTO

task_router = APIRouter()
file_task_router = APIRouter()


task_router.include_router(add_routers(TaskController,
                                  response_model=defaultdict(lambda: GetTaskDTO, {"get_all": Page[GetTaskDTO]})),
                           prefix="/task", tags=["TASK"])

file_task_router.include_router(add_routers(FileTaskController,
                                  response_model=defaultdict(lambda: FileDTO, {"get_all": List[FileDTO]}),
                                                                  methods=FILE_METHODS),
                                  prefix="/images_tools", tags=["IMAGES_TOOLS"])


