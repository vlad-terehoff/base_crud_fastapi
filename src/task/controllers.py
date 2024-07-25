from collections import defaultdict
from src.base_crud.base_controller import ControllerMixin, Controller, FileControllerMixin
from src.base_crud.base_service import FileGenericService, GenericServicePaginate
from src.task.models import TaskModel, FileTaskModel
from src.task.schemas.task_schemas import CreateTaskDTO, PatchTaskDTO, FileToolsFilterDTO


class TaskController(ControllerMixin, Controller):
    pydantic_model = defaultdict(lambda: CreateTaskDTO, {"partial_update": PatchTaskDTO})
    service = GenericServicePaginate(TaskModel).get_service()
    slug_field_type = int


class FileTaskController(FileControllerMixin, Controller):
    pydantic_model = defaultdict(lambda: FileToolsFilterDTO)
    service = FileGenericService(model=FileTaskModel, field_name="task_id").get_service()
    slug_field_type = int