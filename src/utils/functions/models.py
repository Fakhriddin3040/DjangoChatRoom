from typing import Any, Dict, Union

from django.db import models


def try_to_get_object(
    manager: Union[models.Manager, models.QuerySet],
    exception: type,
    error_message: str = "Object not found",
    **kwargs: Dict[str, Any]
) -> models.Model:
    """Try to get an object from the database or raise an exception."""
    try:
        return manager.get(**kwargs)
    except manager.model.DoesNotExist as e:
        raise exception(error_message) from e

async def a_try_to_get_object(
    manager: Union[models.Manager, models.QuerySet],
    exception: type,
    error_message: str = "Object not found",
    **kwargs: Dict[str, Any]
) -> models.Model:
    """Try to get an object asynchronously from the database or raise an exception."""
    try:
        return await manager.aget(**kwargs)
    except manager.model.DoesNotExist as e:
        raise exception(error_message) from e
