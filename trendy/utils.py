from __future__ import unicode_literals

from opal.core.subrecords import patient_subrecords
from opal.models import Patient
from django.db.models import Count


def get_subrecord_qs_from_episode_qs(subrecord, queryset):
    if subrecord in patient_subrecords():
        patients = Patient.objects.filter(episode__in=queryset)
        return subrecord.objects.filter(patient__in=patients)
    else:
        return subrecord.objects.filter(episode__in=queryset)


def aggregate_free_text_or_foreign_key(qs, subrecord, field_name):
    field_name = "{}_fk__name".format(field_name)
    annotated = qs.values(field_name).annotate(Count('id'))
    result = []
    for key_connection in annotated:
        total_count = key_connection.pop('id__count')
        key = key_connection.values()[0]
        result.append([str(key), total_count])
    return result
