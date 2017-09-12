import datetime
from django.utils.functional import cached_property
from opal.core import discoverable
from opal.core import subrecords
from dateutil.relativedelta import relativedelta
from trendy.mixins.gauge_mixin import GaugeMixin
from trendy.mixins.pie_chart_mixin import PieChartMixin
from trendy.mixins.bar_chart_mixin import BarChartMixin
from trendy.utils import get_subrecord_qs_from_episode_qs
from trendy.decorators import bar_link_from_trend
import json


class Trend(
    GaugeMixin, PieChartMixin, BarChartMixin, discoverable.DiscoverableFeature
):
    module_name = "trends"
    template_name = "trendy/subrecords/default_trend.html"

    @classmethod
    def get_trend(cls, subrecord_api_name):
        for trend in cls.list():
            if trend.subrecord_api_name == subrecord_api_name:
                return trend

    @classmethod
    def get_api_name(cls):
        return cls.subrecord_api_name

    @classmethod
    def get_display_name(cls):
        subrecords.get_subrecord_from_api_name(
            cls.subrecord_api_name
        ).get_display_name()

    @cached_property
    def subrecord(cls):
        return subrecords.get_subrecord_from_api_name(
            cls.subrecord_api_name
        )


class DemographicsTrend(Trend):
    subrecord_api_name = "demographics"
    template_name = "trendy/subrecords/demographics_trend.html"

    def age_bar_chart_query(
        self, episode_queryset, trend, field=None, value=None
    ):
        age_group = [int(i.strip()) for i in value.split("-") if i.strip()]
        today = datetime.date.today()
        start_dt = today - relativedelta(years=age_group[0])
        age_group_qs = episode_queryset.filter(
            patient__demographics__date_of_birth__lte=start_dt
        )

        if len(age_group) == 2:
            end_dt = today - relativedelta(years=age_group[1])
            age_group_qs = age_group_qs.filter(
                patient__demographics__date_of_birth__gt=end_dt
            )

        return age_group_qs

    def age_bar_chart(
        self,
        episode_queryset,
        subrecord_api_name,
        request,
        field=None
    ):
        subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
        result = {}
        age_groups = [
            [0, 20],
            [20, 40],
            [40, 60],
            [60, 80],
            [80]
        ]

        qs = get_subrecord_qs_from_episode_qs(subrecord, episode_queryset)

        age_counts = []
        today = datetime.date.today()

        for age_group in age_groups:
            start_dt = today - relativedelta(years=age_group[0])
            age_group_qs = qs.filter(date_of_birth__lte=start_dt)

            if len(age_group) == 1:
                age_counts.append(age_group_qs.count())
            else:
                end_dt = today - relativedelta(years=age_group[1])
                age_counts.append(
                    age_group_qs.filter(date_of_birth__gt=end_dt).count()
                )

        age_counts.insert(0, "Age")
        x_axis = ["x"]

        for age_group in age_groups:
            if len(age_group) == 1:
                x_axis.append(
                    "{} +".format(age_group[0])
                )
            else:
                x_axis.append(
                    "{0} - {1}".format(*age_group)
                )
        aggregate = [x_axis, age_counts]

        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            links=bar_link_from_trend(
                self.get_api_name(), "age_bar_chart", aggregate, request, field
            ),
            subrecord=subrecord_api_name
        ))
        return result


class DiagnosisTrend(Trend):
    subrecord_api_name = "diagnosis"
    template_name = "trendy/subrecords/diagnosis_trend.html"
