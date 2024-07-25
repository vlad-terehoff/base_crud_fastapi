from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi import HTTPException, status
# from src.auth.exceptions import unauthed_exc
from src.base.base_models.dto_models import BaseDto


class ExecResp(BaseDto):
    title: str
    code: int


no_result_found = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запрашиваемого объекта не существует")


def exec_catch(fn):
    async def wrapped(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except NoResultFound as exc:
            # e = ExecResp(title=str(exc), code=400)
            # return e
            raise no_result_found

    return wrapped


def exec_catch_none(fn):
    async def wrapped(*args, **kwargs):
        res = await fn(*args, **kwargs)
        if res:

            return res

        raise no_result_found

    return wrapped

# def exec_catch_check_user_in_db(fn):
#     async def wrapped(*args, **kwargs):
#         try:
#             return await fn(*args, **kwargs)
#         except NoResultFound as exc:
#             # e = ExecResp(title=str(exc), code=400)
#             # return e
#             raise unauthed_exc
#
#     return wrapped