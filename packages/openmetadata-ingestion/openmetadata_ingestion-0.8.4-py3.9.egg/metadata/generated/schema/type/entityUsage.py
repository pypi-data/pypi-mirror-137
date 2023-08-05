# generated by datamodel-codegen:
#   filename:  schema/type/entityUsage.json
#   timestamp: 2022-02-01T18:34:01+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Extra, Field

from . import entityReference, usageDetails


class UsageDetailsOfAnEntity(BaseModel):
    class Config:
        extra = Extra.forbid

    entity: entityReference.EntityReference = Field(
        ..., description='Entity for which usage is returned.'
    )
    usage: List[usageDetails.TypeUsedToReturnUsageDetailsOfAnEntity] = Field(
        ..., description='List usage details per day.'
    )
