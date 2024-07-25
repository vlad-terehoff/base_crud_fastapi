from fastapi import FastAPI
from fastapi_pagination import add_pagination
from src.task.api import task_router, file_task_router
from src.user.api import user_router

app = FastAPI()

add_pagination(app)


app.include_router(user_router)
app.include_router(task_router)
app.include_router(file_task_router)