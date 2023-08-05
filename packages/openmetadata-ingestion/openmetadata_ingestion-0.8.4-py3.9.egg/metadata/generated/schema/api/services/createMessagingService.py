# generated by datamodel-codegen:
#   filename:  schema/api/services/createMessagingService.json
#   timestamp: 2022-02-01T18:34:01+00:00

from __future__ import annotations

from typing import Optional

from pydantic import AnyUrl, BaseModel, Field, constr

from ...entity.services import messagingService
from ...type import schedule


class CreateMessagingServiceEntityRequest(BaseModel):
    name: constr(min_length=1, max_length=128) = Field(
        ..., description='Name that identifies the this entity instance uniquely'
    )
    description: Optional[str] = Field(
        None, description='Description of messaging service entity.'
    )
    serviceType: messagingService.MessagingServiceType
    brokers: messagingService.Brokers = Field(
        ...,
        description='Multiple bootstrap addresses for Kafka. Single proxy address for Pulsar.',
    )
    schemaRegistry: Optional[AnyUrl] = Field(None, description='Schema registry URL')
    ingestionSchedule: Optional[schedule.Schedule] = Field(
        None, description='Schedule for running metadata ingestion jobs'
    )
