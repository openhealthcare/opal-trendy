import datetime
from django.utils.functional import cached_property
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import discoverable
from opal.core import subrecords
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from trendy.utils import (
    get_subrecord_qs_from_episode_qs, aggregate_free_text_or_foreign_key
)
import json


class Trendy(discoverable.DiscoverableFeature):
    module_name = "trends"

    def __init__(self, subrecord_api_name, request, field_name=None):
        self.subrecord_api_name = subrecord_api_name
        self.field_name = field_name
        self.request = request

    def get_graph_data(self, episode_queryset):
        raise NotImplementedError("a query needs to be implemented")

    def get_description(self, value=None):
        raise NotImplementedError("description needs to be implemented")

    def query(self, value, episode_queryset):
        raise NotImplementedError("query needs to be implemented")

    @classmethod
    def get_from_get_param(cls, request, some_key):
        splitted = some_key.split("__")
        if len(splitted) == 2:
            subrecord_api_name, trend_api_name = splitted
            Trend = cls.get(trend_api_name)
            return Trend(subrecord_api_name, request)
        else:
            subrecord_api_name, trend_api_name, field_name = splitted
            Trend = cls.get(trend_api_name)
            return Trend(subrecord_api_name, request, field_name=field_name)

    def append_to_request(self, link):
        full_path = self.request.get_full_path()
        if "?" in full_path:
            return "{0}&{1}".format(full_path, link)
        else:
            return "{0}?{1}".format(full_path, link)

    def to_link(self, value):
        link = None
        if self.field_name:
            link = "{0}__{1}__{2}={3}".format(
                self.subrecord_api_name,
                self.__class__.get_slug(),
                self.field_name,
                value
            )
        else:
            link = "{0}__{1}={2}".format(
                self.subrecord_api_name,
                self.__class__.get_slug(),
                value
            )
        return self.append_to_request(link)

    @cached_property
    def subrecord(self):
        return subrecords.get_subrecord_from_api_name(
            self.subrecord_api_name
        )

    @cached_property
    def is_patient_subrecord(self):
        return self.subrecord in subrecords.patient_subrecords()

    def get_field(self):
        if self.field_name:
            return getattr(self.subrecord, self.field_name)


class FKFTMixin(object):
    @property
    def relative_fk_field(self):
        fk_field = "{0}__{1}_fk".format(
            self.subrecord_api_name, self.field_name
        )
        if self.is_patient_subrecord:
            fk_field = "patient__{}".format(fk_field)

        return fk_field

    @property
    def relative_ft_field(self):
        ft_field = "{0}__{1}_ft".format(
            self.subrecord_api_name, self.field_name
        )
        if self.is_patient_subrecord:
            ft_field = "patient__{}".format(ft_field)

        return ft_field

    @property
    def ft_field(self):
        return "{0}_ft".format(self.field_name)

    @property
    def fk_field(self):
        return "{0}_fk".format(self.field_name)


class FTFKQueryPieChart(Trendy, FKFTMixin):
    """
        supplies a pie chart of the aggregated values of fk ft
    """
    display_name = "FKFTQuery"

    def query(self, value, episode_queryset):
        field = self.get_field()
        if not isinstance(field, ForeignKeyOrFreeText):
            raise ValueError("this trend expects a foreign key or free text")

        if value == 'None':
            value = None
            lookup = self.relative_fk_field
        else:
            lookup = "{0}__name".format(self.relative_fk_field)

        return episode_queryset.filter(**{lookup: value})

    def get_graph_data(self, episode_queryset):
        qs = get_subrecord_qs_from_episode_qs(self.subrecord, episode_queryset)

        field = self.get_field()

        if isinstance(field, ForeignKeyOrFreeText):
            aggregate = aggregate_free_text_or_foreign_key(
                qs, self.subrecord, self.field_name
            )
        else:
            raise NotImplementedError(
                'at the moment we only support free text or fk'
            )

        links = {}
        for i in aggregate:
            links[i[0]] = self.to_link(i[0])
        result = {}
        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            links=links
        ))
        return result

    def get_description(self, value=None):
        return "{0} is {1}".format(self.field_name, value)


class EpisodeAdmissionBarChart(Trendy):
    display_name "Episode Admission"


class AgeBarChart(Trendy):
    """
        supplies a bar chart of the demographics ages
    """
    display_name = "Age"

    def get_description(self, value=None):
        return "Age range between {}".format(value)

    def query(self, value, episode_queryset):
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

    def get_graph_data(
        self,
        episode_queryset,
    ):
        subrecord = subrecords.get_subrecord_from_api_name(
            self.subrecord_api_name
        )
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
        links = {}

        for i in aggregate[0][1:]:
            links[i] = self.to_link(i)

        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            links=links,
            subrecord=self.subrecord_api_name
        ))
        return result


class EmptyFieldGauge(Trendy, FKFTMixin):
    """
        provides all the subrecords where {{ field }} is empty
    """
    display_name = "EmptyFieldGauge"

    def get_description(self, value=None):
        return "{0} has not been filled in".format(self.field_name)

    def query(self, episode_queryset):
        return episode_queryset.filter(**{
            self.relative_fk_field: None,
            self.relative_ft_field: ""
        })

    def get_graph_data(
        self,
        episode_queryset,
    ):
        """ gives the % of subrecords where the field is None
        """
        qs = get_subrecord_qs_from_episode_qs(self.subrecord, episode_queryset)
        total = qs.count()
        count = 0

        if total == 0:
            amount = 0
        else:
            count = qs.filter(**{
                self.fk_field: None,
                self.ft_field: '',
            }).count()
            amount = round(float(count)/total, 3) * 100
        result = {}
        result["total"] = total
        result["count"] = count
        aggregate = [['None', amount]]
        links = {"None": self.to_link("None")}
        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            field=self.field_name,
            links=links,
            subrecord=self.subrecord_api_name
        ))
        return result


class NonCodedFkAndFTGauge(Trendy, FKFTMixin):
    """
        provides all fields where we have a free text field
    """
    display_name = "NonCodedFkAndFTGauge"

    def query(
        self, episode_queryset
    ):
        return episode_queryset.filter(**{
            self.relative_fk_field: None,
        }).exclude(**{
            self.relative_ft_field: ''
        })

    def get_graph_data(
            self, episode_queryset
    ):
        subrecord = subrecords.get_subrecord_from_api_name(
            self.subrecord_api_name
        )
        qs = get_subrecord_qs_from_episode_qs(subrecord, episode_queryset)
        total = qs.count()
        count = 0

        if total == 0:
            amount = 0
        else:
            count = qs.filter(**{
                self.fk_field: None
            }).exclude(**{
                self.ft_field: ''
            }).count()
            amount = round(float(count)/total, 3) * 100
        result = {}
        result["total"] = total
        result["count"] = count
        aggregate = [['None', amount]]
        links = {"None": self.to_link("None")}
        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            links=links,
            field=self.field_name,
            subrecord=self.subrecord_api_name
        ))
        return result


class MissingGauge(Trendy):
    display_name = "MissingGauge"

    def query(
        self, episode_queryset
    ):
        related_name = self.subrecord.__name__.lower()
        key = "num_{}".format(related_name)
        qs = episode_queryset.annotate(**{
            key: Count(related_name)
        })
        return qs.filter(**{key: 0})

    def get_graph_data(
            self, episode_queryset
    ):
        """ gives the % of subrecords where the field is None
        """
        total = episode_queryset.count()
        count = 0
        result = {}

        if total == 0:
            amount = 0
        else:
            count = episode_queryset.annotate(
                subrecord_count=Count(self.subrecord_api_name)
            ).filter(subrecord_count=0).count()

            amount = round(float(count)/total, 3) * 100
        result["total"] = total
        result["count"] = count
        aggregate = [['None', amount]]
        links = {"None": self.to_link("None")}
        result["graph_vals"] = json.dumps(dict(
            aggregate=aggregate,
            subrecord=self.subrecord_api_name,
            links=links
        ))
        return result
