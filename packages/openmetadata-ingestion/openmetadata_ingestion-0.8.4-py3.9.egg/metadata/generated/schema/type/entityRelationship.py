# generated by datamodel-codegen:
#   filename:  schema/type/entityRelationship.json
#   timestamp: 2022-02-01T18:34:01+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from . import basic


class EntityRelationship(BaseModel):
    class Config:
        extra = Extra.forbid

    fromId: Optional[basic.Uuid] = Field(
        None,
        description='Unique identifier that identifies the entity from which the relationship originates.',
    )
    fromFQN: Optional[str] = Field(
        None,
        description='Fully qualified name of the entity from which the relationship originates.',
    )
    fromEntity: str = Field(
        ...,
        description='Type of the entity from which the relationship originates. Examples: `database`, `table`, `metrics` ...',
    )
    toId: Optional[basic.Uuid] = Field(
        None,
        description='Unique identifier that identifies the entity towards which the relationship refers to.',
    )
    toFQN: Optional[str] = Field(
        None,
        description='Fully qualified name of the entity towards which the relationship refers to.',
    )
    toEntity: str = Field(
        ...,
        description='Type of the entity towards which the relationship refers to. Examples: `database`, `table`, `metrics` ...',
    )
    relation: str = Field(
        ..., description='Describes relationship between the two entities.'
    )
    deleted: Optional[bool] = Field(
        False, description='`true` indicates the relationship has been soft deleted.'
    )
