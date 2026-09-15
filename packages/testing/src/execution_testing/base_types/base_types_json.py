"""JSON encoding and decoding for Sila types."""

from typing import Any, AnyStr, List

from .pydantic import SilaTestBaseModel, SilaTestRootModel


def to_json(
    input_model: (
        SilaTestBaseModel
        | SilaTestRootModel
        | AnyStr
        | List[SilaTestBaseModel | SilaTestRootModel | AnyStr]
    ),
) -> Any:
    """Convert a model to its json data representation."""
    if isinstance(input_model, list):
        return [to_json(item) for item in input_model]
    elif isinstance(input_model, (SilaTestBaseModel, SilaTestRootModel)):
        return input_model.model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
    else:
        return str(input_model)
