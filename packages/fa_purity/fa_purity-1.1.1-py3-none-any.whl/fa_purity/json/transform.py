from fa_purity.json.factory import (
    JsonObj,
)
from fa_purity.json.value import (
    transform as jval_transform,
)
from typing import (
    Any,
    Dict,
)


def to_raw(json_obj: JsonObj) -> Dict[str, Any]:  # type: ignore[misc]
    return {key: jval_transform.to_raw(val) for key, val in json_obj.items()}  # type: ignore[misc]
