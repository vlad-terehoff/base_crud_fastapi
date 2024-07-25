from typing import Callable
from fastapi import APIRouter
from src.base.base_models.dto_models import BaseDto
from src.base_crud.base_consts import Method, DEFAULT_METHODS, SINGLE_METHODS, METHOD_WRAPPER
from src.base_crud.base_meta_class import DynamicParamMeta


class ControllerRouter(APIRouter):

    def add_endpoint(self, path: str, view_func: Callable, method: str, response_model: BaseDto, status_code=200):
        self.add_api_route(path, view_func, methods=[method], status_code=status_code, response_model=response_model)


def add_routers(
        controller: DynamicParamMeta,
        response_model: dict = None,
        methods: set[Method] = DEFAULT_METHODS,
        exclude_methods: set[Method] = {}
        ) -> ControllerRouter:
    default_router = ControllerRouter()

    for method_name in methods:
        if method_name not in exclude_methods:
            add_path(controller, method_name, default_router, response_model)

    return default_router


def add_path(controller: DynamicParamMeta, method_name: Method, default_router: ControllerRouter, response_model: dict):
    method = getattr(controller(), method_name.name)
    path = f"/{{{controller.url_field}}}" if method_name in SINGLE_METHODS else "/"
    if method_name is Method.delete:
        response_model = None
    else:
        response_model = response_model[method_name.name]
    default_router.add_endpoint(path, method, METHOD_WRAPPER[method_name], response_model)
