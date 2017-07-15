from collections import OrderedDict

from opal import models
from opal.core.subrecords import episode_subrecords
from opal.core.fields import ForeignKeyOrFreeText
from django.db.models import Count, Min, F, Max, Avg


class SubrecordTrend(object):
    def get_request_information(self, qs):
        # team = request_get_args.pop("team")

        subrecords = []

        for Subrecord in episode_subrecords():
            episode_subs = Subrecord.objects.filter(
                episode__in=qs
            )

            field_names = Subrecord._get_fieldnames_to_serialize()
            field_names = [
                i for i in field_names if isinstance(getattr(Subrecord, i, None), ForeignKeyOrFreeText)
            ]
            subrecord_counts = OrderedDict()
            subrecord_counts["all"] = dict(total=episode_subs.count())

            if len(field_names):
                field = "{}_fk".format(field_names[0])
                field_totalled = episode_subs.annotate(
                    field_total=Count(field)
                ).order_by('field_total')
                for row in field_totalled[:10]:
                    if getattr(row, field):
                        subrecord_counts[getattr(row, field).name] = dict(
                            total=getattr(row, "field_total")
                        )

            subrecords.append(dict(
                subrecord=Subrecord,
                popular=subrecord_counts
            ))
        return {
            "subrecords": subrecords,
            "team": "team"
        }











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
