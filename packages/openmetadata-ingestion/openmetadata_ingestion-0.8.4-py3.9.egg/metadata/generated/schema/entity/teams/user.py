# generated by datamodel-codegen:
#   filename:  schema/entity/teams/user.json
#   timestamp: 2022-02-01T18:34:01+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field, constr

from ...type import basic, entityHistory, entityReference, profile


class UserName(BaseModel):
    __root__: constr(min_length=1, max_length=128) = Field(
        ...,
        description='A unique name of the user, typically the user ID from an identity provider. Example - uid from LDAP.',
    )


class User(BaseModel):
    class Config:
        extra = Extra.forbid

    id: basic.Uuid = Field(
        ..., description='Unique identifier that identifies a user entity instance.'
    )
    name: UserName
    description: Optional[str] = Field(None, description='Used for user biography.')
    displayName: Optional[str] = Field(
        None,
        description="Name used for display purposes. Example 'FirstName LastName'.",
    )
    version: Optional[entityHistory.EntityVersion] = Field(
        None, description='Metadata version of the entity.'
    )
    updatedAt: Optional[basic.Timestamp] = Field(
        None,
        description='Last update time corresponding to the new version of the entity in Unix epoch time milliseconds.',
    )
    updatedBy: Optional[str] = Field(None, description='User who made the update.')
    email: basic.Email = Field(..., description='Email address of the user.')
    href: basic.Href = Field(
        ..., description='Link to the resource corresponding to this entity.'
    )
    timezone: Optional[str] = Field(None, description='Timezone of the user.')
    isBot: Optional[bool] = Field(
        None, description='When true indicates a special type of user called Bot.'
    )
    isAdmin: Optional[bool] = Field(
        None,
        description='When true indicates user is an administrator for the system with superuser privileges.',
    )
    profile: Optional[profile.Profile] = Field(None, description='Profile of the user.')
    teams: Optional[entityReference.EntityReferenceList] = Field(
        None, description='Teams that the user belongs to.'
    )
    owns: Optional[entityReference.EntityReferenceList] = Field(
        None, description='List of entities owned by the user.'
    )
    follows: Optional[entityReference.EntityReferenceList] = Field(
        None, description='List of entities followed by the user.'
    )
    changeDescription: Optional[entityHistory.ChangeDescription] = Field(
        None, description='Change that lead to this version of the entity.'
    )
    deleted: Optional[bool] = Field(
        False, description='When `true` indicates the entity has been soft deleted.'
    )
    roles: Optional[entityReference.EntityReferenceList] = Field(
        None, description='Roles that the user has been assigned.'
    )
