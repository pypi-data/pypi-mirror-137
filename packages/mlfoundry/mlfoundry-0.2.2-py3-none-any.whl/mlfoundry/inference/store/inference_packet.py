import logging
import typing
from datetime import datetime

import numpy as np
from pydantic import BaseModel, Field, constr, validator

from mlfoundry.exceptions import MlFoundryException

logger = logging.getLogger(__name__)

ValueType = typing.Dict[str, typing.Union[str, float, int, bool, np.ndarray]]
# TODO: The user may want to pass np.uint8, np.float32 values directly. Support these types too.
ShapType = typing.Dict[str, typing.Union[float, np.ndarray, typing.List[float]]]


class InferencePacket(BaseModel):
    model_name: constr(min_length=1, max_length=256)
    model_version: constr(min_length=1, max_length=64)
    inference_id: constr(min_length=16, max_length=36)

    features: ValueType
    predictions: ValueType

    shap_values: typing.Optional[ShapType] = None
    raw_data: typing.Optional[ValueType] = None
    actuals: typing.Optional[ValueType] = None
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("features", "predictions")
    def check_dict_length(cls, value):
        if len(value) == 0:
            raise MlFoundryException("features, predictions must be an non-empty dict")
        return value

    class Config:
        arbitrary_types_allowed = True
