from typing import Optional, no_type_check

import pydantic
from humps import camelize


class BaseModel(pydantic.BaseModel):
    class Config:
        alias_generator = camelize


class AllOptional(pydantic.main.ModelMetaclass):
    """
    Metaclass for partial update models. Turn every field into Optional
    https://stackoverflow.com/questions/67699451/
    """

    @no_type_check
    def __new__(self, name, bases, namespaces, **kwargs):  # noqa
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            for klass in base.mro():
                # Iterate through all parents of inherited classes
                if hasattr(klass, "__annotations__"):
                    annotations.update(klass.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)
