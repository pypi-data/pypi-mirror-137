# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Type registry.
"""

from ..constants import *
from ..types import *
from sweetrpg_library_objects.api.volume.schema import VolumeAPISchema
from sweetrpg_library_objects.api.person.schema import PersonAPISchema
from sweetrpg_library_objects.api.contribution.schema import ContributionAPISchema
from sweetrpg_library_objects.api.publisher.schema import PublisherAPISchema
from sweetrpg_library_objects.api.studio.schema import StudioAPISchema
from sweetrpg_library_objects.api.system.schema import SystemAPISchema
from sweetrpg_library_objects.api.review.schema import ReviewAPISchema
from sweetrpg_library_objects.model.volume import Volume
from sweetrpg_library_objects.model.person import Person
from sweetrpg_library_objects.model.contribution import Contribution
from sweetrpg_library_objects.model.publisher import Publisher
from sweetrpg_library_objects.model.system import System
from sweetrpg_library_objects.model.studio import Studio
from sweetrpg_library_objects.model.review import Review


_types = {
    VOLUME: {
        ENDPOINT_PATH: 'volumes',
        API_SCHEMA_CLASS: VolumeAPISchema,
        OBJECT_CLASS: Volume,
    },
    PERSON: {
        ENDPOINT_PATH: 'persons',
        API_SCHEMA_CLASS: PersonAPISchema,
        OBJECT_CLASS: Person,
    },
    CONTRIBUTION: {
        ENDPOINT_PATH: 'contributions',
        API_SCHEMA_CLASS: ContributionAPISchema,
        OBJECT_CLASS: Contribution,
    },
    PUBLISHER: {
        ENDPOINT_PATH: 'publishers',
        API_SCHEMA_CLASS: PublisherAPISchema,
        OBJECT_CLASS: Publisher,
    },
    STUDIO: {
        ENDPOINT_PATH: 'studios',
        API_SCHEMA_CLASS: StudioAPISchema,
        OBJECT_CLASS: Studio,
    },
    SYSTEM: {
        ENDPOINT_PATH: 'systems',
        API_SCHEMA_CLASS: SystemAPISchema,
        OBJECT_CLASS: System,
    },
    REVIEW: {
        ENDPOINT_PATH: 'reviews',
        API_SCHEMA_CLASS: ReviewAPISchema,
        OBJECT_CLASS: Review,
    },
}
