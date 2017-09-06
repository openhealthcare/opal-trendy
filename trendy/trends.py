# from collections import OrderedDict
#
# from opal.core import discoverable
# from opal import models
# from opal.core.subrecords import episode_subrecords, subrecords
# from opal.core.fields import ForeignKeyOrFreeText
# from django.db.models.fields.related import ManyToManyField
# from django.db.models import Count, Min, F, Max, Avg
from opal.core import discoverable
from trendy.mixins.gauge_mixin import GaugeMixin
from trendy.mixins.pie_chart_mixin import PieChartMixin
# from trendy.mixins.pie_chart_mixin impot PieChartMixin

# FIELD_OVERRIDES = {
#     "antimicrobial": "drug",
#     "presenting_complaint": "symptoms"
# }


class Trend(GaugeMixin, PieChartMixin, discoverable.DiscoverableFeature):
    module_name = "trends"
    template_name = "trendy/subrecords/default_trend.html"

    @classmethod
    def get_trend(cls, subrecord_api_name):
        for trend in cls.list():
            if trend.subrecord_api_name == subrecord_api_name:
                return trend


class DemographicsTrend(Trend):
    subrecord_api_name = "demographics"
    template_name = "trendy/subrecords/demographics_trend.html"


class DiagnosisTrend(Trend):
    subrecord_api_name = "diagnosis"
    template_name = "trendy/subrecords/diagnosis_trend.html"


# class SubrecordTrend(object):
#     def get_min(self, qs):
#         # get's the min of all the subrecord mins
#         min_args = []
#         for subrecord in episode_subrecords():
#             related_name = subrecord.__name__.lower()
#             min_args.append(F("{0}_min_created".format(related_name)))
#         return qs.annotate(min_created=min(*min_args))
#
#     def get_min_episode(self, qs):
#         # annotates an episode queryset with extra fields
#         # of the min created for non singleton subrecords
#         # and min updated for singleton subrecord
#         for subrecord in episode_subrecords():
#             related_name = subrecord.__name__.lower()
#             if subrecord._is_singleton:
#                 # if its a singleton, created is never populated, updated is
#                 # so use this as created
#                 min_updated = {
#                     "{0}_min_created".format(related_name): Min(
#                         "{}__updated".format(related_name)
#                     )
#                 }
#                 qs = qs.annotate(
#                     **min_updated
#                 )
#             else:
#                 min_created = {
#                     "{0}_min_created".format(related_name): Min(
#                         "{}__created".format(related_name)
#                     )
#                 }
#                 qs = qs.annotate(
#                     **min_created
#                 )
#             total_count = {
#                 "{0}_count".format(related_name): Count(
#                     related_name
#                 )
#             }
#             qs = qs.annotate(**total_count)
#
#         return qs
#
#     def get_many_to_many_counts(self, Subrecord, qs, field):
#         episode_subs = Subrecord.objects.filter(
#             episode__in=qs
#         )
#         subrecord_counts = OrderedDict()
#         subrecord_counts["all"] = dict(total=episode_subs.count())
#
#         field_totalled = episode_subs.values(field).annotate(
#             field_total=Count(field)
#         ).order_by('-field_total')
#
#         for row in field_totalled[:10]:
#             if row.get(field, None):
#                 field_obj = Subrecord._meta.get_field(field)
#                 related = field_obj.related_model.objects.get(id=row.get(field))
#                 subrecord_counts[related.name] = dict(
#                     total=row["field_total"]
#                 )
#         return subrecord_counts
#
#     def get_subrecord_summary(self, Subrecord, qs):
#         episode_subs = Subrecord.objects.filter(
#             episode__in=qs
#         )
#
#         if Subrecord._is_singleton:
#             episode_subs = episode_subs.exclude(updated=None)
#         else:
#             episode_subs = episode_subs.exclude(created=None)
#
#         if not episode_subs.exists():
#             return
#
#         if Subrecord.get_api_name() in FIELD_OVERRIDES:
#             field_names = [FIELD_OVERRIDES[Subrecord.get_api_name()]]
#         else:
#             field_names = Subrecord._get_fieldnames_to_serialize()
#             field_names = [
#                 i for i in field_names if isinstance(getattr(Subrecord, i, None), ForeignKeyOrFreeText)
#             ]
#         subrecord_counts = OrderedDict()
#
#         subrecord_counts["all"] = dict(total=episode_subs.count())
#         field = None
#         if len(field_names):
#             field = field_names[0]
#             if field in Subrecord._meta.get_all_field_names():
#                 if isinstance(
#                     Subrecord._meta.get_field(field), ManyToManyField
#                 ):
#                     subrecord_counts = self.get_many_to_many_counts(
#                         Subrecord, qs, field
#                     )
#             else:
#                 field = "{}_fk".format(field_names[0])
#                 field_totalled = episode_subs.values(field).annotate(
#                     field_total=Count(field)
#                 ).order_by('-field_total')
#
#                 for row in field_totalled[:10]:
#                     if row.get(field, None):
#                         related = getattr(Subrecord, field_names[0]).foreign_model
#                         related = related.objects.get(id=row.get(field))
#                         subrecord_counts[related.name] = dict(
#                             total=row["field_total"]
#                         )
#             return dict(
#                 subrecord=Subrecord,
#                 field=field,
#                 popular=subrecord_counts
#             )
#
#     def get_subrecord_difference(self, qs, f_base):
#         # for each subrecord, give me the difference between
#         # some f expression and when it was created or updated
#         for Subrecord in episode_subrecords():
#             related_name = Subrecord.__name__.lower()
#             min_created = "{0}_min_created".format(related_name)
#             qs = qs.annotate(**{
#                 "{}_diff_created".format(related_name): F(min_created) - f_base
#             })
#         return qs
#
#     def subrecord_detail(self, qs):
#         result = []
#         for Subrecord in episode_subrecords():
#             related_name = Subrecord.__name__.lower()
#             display_name = Subrecord.get_display_name()
#             field = "{0}_diff_created".format(related_name)
#             count_field = "{0}_count".format(related_name)
#             row = qs.aggregate(
#                 avg_created=Min(field),
#                 max_count=Max(count_field),
#                 avg_count=Avg(count_field),
#                 min_count=Min(count_field)
#             )
#             row[self.SUBRECORD_NAME] = display_name
#             row[self.SUBRECORD_DETAIL] = self.get_aggregate_subrecord_summary(
#                 Subrecord, qs
#             )
#             result.append(row)
#         return result
#
#     def get_request_information(self, qs):
#         # team = request_get_args.pop("team")
#
#         subrecords = []
#
#         qs = self.get_min_episode(qs)
#
#         for Subrecord in episode_subrecords():
#             summary = self.get_subrecord_summary(Subrecord, qs)
#
#             if summary:
#                 subrecords.append(summary)
#         return {
#             "subrecords": subrecords,
#             "team": "team"
#         }











#
# class SubrecordTrends(object):
#     def __init__(self, request_get_args):
#         team = request_get_args.pop("team")
#         qs = models.Episode.objects.all()
#         qs = qs.filter(tagging__value=team)
#         qs = self.get_min_episode(qs)
#         qs = self.get_min(qs)
#         qs = self.get_subrecord_difference(qs, F('min_created'))
#         return self.subrecord_detail(qs)
#
    # def get_min_episode(self, qs):
    #     # annotates an episode queryset with extra fields
    #     # of the min created for non singleton subrecords
    #     # and min updated for singleton subrecord
    #     for subrecord in episode_subrecords():
    #         related_name = subrecord.__name__.lower()
    #         if subrecord._is_singleton:
    #             # if its a singleton, created is never populated, updated is
    #             # so use this as created
    #             min_updated = {
    #                 "{0}_min_created".format(related_name): Min(
    #                     "{}__updated".format(related_name)
    #                 )
    #             }
    #             qs = qs.annotate(
    #                 **min_updated
    #             )
    #         else:
    #             min_created = {
    #                 "{0}_min_created".format(related_name): Min(
    #                     "{}__created".format(related_name)
    #                 )
    #             }
    #             qs = qs.annotate(
    #                 **min_created
    #             )
    #         total_count = {
    #             "{0}_count".format(related_name): Count(
    #                 related_name
    #             )
    #         }
    #         qs = qs.annotate(**total_count)
    #
    #     return qs
#
#     def get_min(self, qs):
#         # get's the min of all the subrecord mins
#         min_args = []
#         for subrecord in episode_subrecords():
#             related_name = subrecord.__name__.lower()
#             min_args.append(F("{0}_min_created".format(related_name)))
#         return qs.annotate(min_created=min(*min_args))
#
#     def get_subrecord_difference(self, qs, f_base):
#         # for each subrecord, give me the difference between
#         # some f expression and when it was created or updated
#         for Subrecord in episode_subrecords():
#             related_name = Subrecord.__name__.lower()
#             min_created = "{0}_min_created".format(related_name)
#             qs = qs.annotate(**{
#                 "{}_diff_created".format(related_name): F(min_created) - f_base
#             })
#         return qs
#
#     def subrecord_detail(self, qs):
#         result = []
#         for Subrecord in episode_subrecords():
#             related_name = Subrecord.__name__.lower()
#             display_name = Subrecord.get_display_name()
#             field = "{0}_diff_created".format(related_name)
#             count_field = "{0}_count".format(related_name)
#             row = qs.aggregate(
#                 avg_created=Min(field),
#                 max_count=Max(count_field),
#                 avg_count=Avg(count_field),
#                 min_count=Min(count_field)
#             )
#             row[self.SUBRECORD_NAME] = display_name
#             row[self.SUBRECORD_DETAIL] = self.get_aggregate_subrecord_summary(
#                 Subrecord, qs
#             )
#             result.append(row)
#         return result
