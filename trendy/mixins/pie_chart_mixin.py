from opal.core import subrecords
from trendy import decorators
from trendy.utils import (
    aggregate_free_text_or_foreign_key,
    get_subrecord_qs_from_episode_qs
)
from opal.core.fields import ForeignKeyOrFreeText


def aggregate_field(queryset, subrecord, field_name):
    """ looks at the total number of subrecords for the related episodes
    """
    qs = get_subrecord_qs_from_episode_qs(subrecord, queryset)

    field = getattr(subrecord, field_name)

    if isinstance(field, ForeignKeyOrFreeText):
        return aggregate_free_text_or_foreign_key(qs, subrecord, field_name)
    else:
        raise NotImplementedError(
            'at the moment we only support free text or fk'
        )


class PieChartMixin(object):
    """
        provides all pie chart methods
    """

    @decorators.subrecord_attr
    def subrecord_break_down(
        self,
        queryset,
        subrecord_api_name,
        request,
        field
    ):
        subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
        return aggregate_field(queryset, subrecord, field)
