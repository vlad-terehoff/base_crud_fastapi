import functools
import inspect
from types import FunctionType
from typing import Callable, List
from inspect import Parameter
from pydantic import create_model
from fastapi import Depends, UploadFile
from fastapi_filters import FilterValues, create_filters_from_model
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db_settings.session import ISession


def change_annotation(def_ann, new_model):
    if def_ann is not int and def_ann is not str:
        fields = dict()
        for k, v in inspect.signature(new_model).parameters.items():
            fields[k] = (v.annotation, v.default)

        return create_model("ReqModel", **fields, )


    else:
        return def_ann


class DynamicParamMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == "Controller":
            return super().__new__(cls, name, bases, attrs)

        py_model = attrs["pydantic_model"]
        # slug_field = attrs.get("slug_field_type")

        for base in bases:
            for attr_name, attr_value in base.__dict__.items():
                if inspect.isfunction(attr_value) and attr_name not in attrs:
                    attrs[attr_name] = cls.deepcopy_func(attr_value)

                if attr_name == "url_field" and attr_name not in attrs:
                    attrs[attr_name] = attr_value

        for attr_name, attr_value in attrs.items():
            if inspect.isfunction(attr_value):
                attrs[attr_name] = cls.wrap_method(
                    attr_value,
                    return_type=py_model[attr_name])

        return super().__new__(cls, name, (), attrs)

    @staticmethod
    def deepcopy_func(f) -> Callable:
        g = FunctionType(
            f.__code__,
            f.__globals__,
            name=f.__name__,
            argdefs=f.__defaults__,
            closure=f.__closure__
        )

        g = functools.update_wrapper(g, f)
        g.__kwdefaults__ = f.__kwdefaults__

        return g

    @staticmethod
    def wrap_method(method, return_type=None):
        sig = inspect.signature(method)
        req_parameters: List[Parameter] = []
        def_parameters: List[Parameter] = []

        for name in sig.parameters:
            parameter = sig.parameters[name]
            if parameter.annotation is FilterValues:
                parameter = parameter.replace(default=Depends(create_filters_from_model(return_type)))

            elif parameter.annotation is AsyncSession:
                parameter = parameter.replace(annotation=ISession)

            elif parameter.annotation is UploadFile:
                parameter = parameter.replace(annotation=UploadFile)

            else:
                annotation = change_annotation(parameter.annotation, return_type)
                parameter = parameter.replace(annotation=annotation)

            if parameter.default is Parameter.empty:
                req_parameters.append(parameter)

            else:
                def_parameters.append(parameter)

        parameters = req_parameters + def_parameters
        return_annotation = sig.return_annotation

        method.__signature__ = sig.replace(parameters=parameters, return_annotation=return_annotation)
        return method

