from typing import Any, Dict, Union
from django.db import models


def try_to_get_object(
    manager: Union[models.Manager, models.QuerySet],
    exception: Exception,
    error_message: str = "Object not found",
    **kwargs: Dict[str, Any]) -> models.Model:
    try:
        return manager.get(**kwargs)
    except Exception as _:
        raise exception(error_message)