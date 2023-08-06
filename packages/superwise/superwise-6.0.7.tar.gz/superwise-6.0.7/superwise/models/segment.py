""" This module implement Segment model  """
import enum

from superwise.models.base import BaseModel
from superwise.models.data_entity import DataEntity
from superwise.models.model import Model


class SegmentCondition(enum.Enum):
    __name__ = "SegmentCondition"
    GREATER_THAN_EQ = ">="
    LESS_THAN_EQ = "<="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    IS_NULL = "is null"
    IN = "in"
    NOT_IN = "not in"
    EQUALS = "=="
    BETWEEN = "between"


class SegmentConditionDefinition:
    def __init__(self, entity_name, condition, value):
        self.entity_name =  entity_name
        self.condition = condition
        self.value = value
        assert isinstance(condition, SegmentCondition)

    def to_dict(self):
        return dict(entity_name=self.entity_name, condition=self.condition.value, value=self.value)


class Segment(BaseModel):
    """ Segment model class """

    def __init__(
        self,
        id=None,
        model_id=None,
        name=None,
        status=None,
        definition=None,
        definition_json=None,
        definition_query=None,
        created_at=None,
        created_by=None,
        archived_at=None,
        **kwargs
    ):
        """
        ### Description:

        Constructor of Segment model class

        ### Args:

        `id`: id of segment

        `name`: name of segment (string)

        `status`:

        `definition`:

        `definition_query`:

        `created_at`:

        `created_by`:

        `archived_at`:

        """

        self.id = id
        self.model_id = model_id
        self.name = name
        self.status = status

        if definition is not None:
            if any([isinstance(i, SegmentConditionDefinition) for i in definition]):
                self.definition_json = [i.to_dict() for i in definition]
        else:
            self.definition_json = definition_json
        self.definition_query = definition_query
        self.created_at = created_at
        self.created_by = created_by
        self.archived_at = archived_at
