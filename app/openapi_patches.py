"""Compatibility patches for generated models returned by X's web API."""

import inspect
import typing

import twitter_openapi_python_generated.models as models
from pydantic import BaseModel, BeforeValidator

_patched = False


def _null_to_empty_list(value: object) -> object:
    return [] if value is None else value


def relax_null_lists() -> None:
    global _patched
    if _patched:
        return

    for model in vars(models).values():
        if not (inspect.isclass(model) and issubclass(model, BaseModel)):
            continue

        relaxed = False
        for field in model.model_fields.values():
            if field.is_required() and typing.get_origin(field.annotation) is list:
                field.metadata.append(BeforeValidator(_null_to_empty_list))
                relaxed = True
        if relaxed:
            model.model_rebuild(force=True)

    _patched = True

