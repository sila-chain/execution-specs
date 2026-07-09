"""Base pydantic classes used to define the models for Sila tests."""

from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, RootModel
from pydantic.alias_generators import to_camel
from typing_extensions import Self

from .mixins import ModelCustomizationsMixin

RootModelRootType = TypeVar("RootModelRootType")


class SilaTestBaseModel(BaseModel, ModelCustomizationsMixin):
    """Base model for all models for Sila tests."""

    pass


class SilaTestRootModel(
    RootModel[RootModelRootType], ModelCustomizationsMixin
):
    """Base model for all models for Sila tests."""

    root: Any


class CopyValidateModel(SilaTestBaseModel):
    """Model that supports copying with validation."""

    def copy(self, **kwargs: Any) -> Self:
        """
        Create a copy of the model with the updated fields that are validated.
        """
        # Only include actual model fields, not computed fields
        model_field_names = set(self.__class__.model_fields.keys())
        dumped = {
            k: v
            for k, v in self.model_dump(exclude_unset=True).items()
            if k in model_field_names
        }
        return self.__class__(**(dumped | kwargs))


class CamelModel(CopyValidateModel):
    """
    A base model that converts field names to camel case when serializing.

    For example, the field name `current_timestamp` in a Python model will be
    represented as `currentTimestamp` when it is serialized to json.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        validate_default=True,
        extra="forbid",
    )
