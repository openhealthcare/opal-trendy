from opal.core import subrecords
import json
from trendy.utils import get_subrecord_qs_from_episode_qs
from django.db.models import Count


class GaugeMixin(object):
    """
        provides all gauge methods
    """

    def empty_field_gauge(
            self,
            queryset,
            subrecord_api_name,
            get_params,
            user,
            field
    ):
        """ gives the % of subrecords where the field is None
        """
        subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
        qs = get_subrecord_qs_from_episode_qs(subrecord, queryset)
        total = qs.count()
        count = 0

        if total == 0:
            amount = 0
        else:
            count = qs.filter(**{
                "{}_fk".format(field): None,
                "{}_ft".format(field): '',
            }).count()
            amount = round(float(count)/total, 3) * 100
        result = {}
        result["total"] = total
        result["count"] = count
        result["graph_vals"] = json.dumps(dict(
            aggregate=[['None', amount]],
            field=field,
            subrecord=subrecord_api_name
        ))
        return result

    def non_coded_gauge(
            self, queryset, subrecord_api_name, get_params, user, field
    ):
        subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
        qs = get_subrecord_qs_from_episode_qs(subrecord, queryset)
        total = qs.count()
        count = 0

        if total == 0:
            amount = 0
        else:
            count = qs.filter(**{
                "{}_fk".format(field): None
            }).exclude(**{
                "{}_ft".format(field): ''
            }).count()
            amount = round(float(count)/total, 3) * 100
        result = {}
        result["total"] = total
        result["count"] = count
        result["graph_vals"] = json.dumps(dict(
            aggregate=[['None', amount]],
            field=field,
            subrecord=subrecord_api_name
        ))
        return result

    def missing_subrecord_gauge(
            self, queryset, subrecord_api_name, get_params, user
    ):
        """ gives the % of subrecords where the field is None
        """
        total = queryset.count()
        count = 0
        result = {}

        if total == 0:
            amount = 0
        else:
            count = queryset.annotate(
                subrecord_count=Count(subrecord_api_name)
            ).filter(subrecord_count=0).count()

            amount = round(float(count)/total, 3) * 100
        result["total"] = total
        result["count"] = count
        result["graph_vals"] = json.dumps(dict(
            aggregate=[['None', amount]],
            subrecord=subrecord_api_name
        ))
        return result
