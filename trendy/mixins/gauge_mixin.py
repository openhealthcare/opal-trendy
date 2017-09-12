from opal.core import subrecords
import json
from trendy.utils import get_subrecord_qs_from_episode_qs
from trendy.decorators import link_from_trend
from django.db.models import Count


class GaugeMixin(object):
    """
        provides all gauge methods
    """

    def empty_field_gauge_query(self, episode_queryset, trend, field=None):
        fk_fields = "{0}__{1}_fk".format(trend.subrecord_api_name, field)
        ft_fields = "{0}__{1}_ft".format(trend.subrecord_api_name, field)
        return episode_queryset.filter(**{
            fk_fields: None,
            ft_fields: ""
        })

    def empty_field_gauge(
            self,
            queryset,
            subrecord_api_name,
            request,
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
        aggregate = [['None', amount]]
        links = link_from_trend(
            self.get_api_name(), "empty_field_gauge", aggregate, request, field
        )
        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            field=field,
            links=links,
            subrecord=subrecord_api_name
        ))
        return result

    def non_coded_gauge_query(
        self, episode_queryset, trend, value=None, field=None
    ):
        fk_fields = "{0}__{1}_fk".format(trend.subrecord_api_name, field)
        ft_fields = "{0}__{1}_ft".format(trend.subrecord_api_name, field)
        return episode_queryset.filter(**{
            fk_fields: None,
        }).exclude(**{
            ft_fields: ''
        })

    def non_coded_gauge(
            self, queryset, subrecord_api_name, request, field
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
        aggregate = [['None', amount]]
        links = link_from_trend(
            self.get_api_name(), "non_coded_gauge", aggregate, request, field
        )

        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            links=links,
            field=field,
            subrecord=subrecord_api_name
        ))
        return result

    def missing_subrecord_gauge_query(
        self, episode_queryset, trend, field=None, value=None
    ):
        related_name = trend.subrecord.__name__.lower()
        key = "num_{}".format(related_name)
        qs = episode_queryset.annotate(**{
            key: Count(related_name)
        })
        return qs.filter(**{key: 0})

    def missing_subrecord_gauge(
            self, queryset, subrecord_api_name, request
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
        aggregate = [['None', amount]]
        links = link_from_trend(
            self.get_api_name(),
            "missing_subrecord_gauge",
            aggregate,
            request,
        )
        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            subrecord=subrecord_api_name,
            links=links
        ))
        return result
