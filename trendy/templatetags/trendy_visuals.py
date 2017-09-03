from django import template
from opal.core import subrecords
from opal.models import Patient
from django.db.models import Count
from opal.core.fields import ForeignKeyOrFreeText
from opal.core.subrecords import patient_subrecords
# from django.db.models import Count

import json

register = template.Library()


def get_subrecord_qs_from_episode_qs(subrecord, queryset):
    if subrecord in patient_subrecords():
        patients = Patient.objects.filter(episode__in=queryset)
        return subrecord.objects.filter(patient__in=patients)
    else:
        return subrecord.objects.filter(episode__in=queryset)


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


def aggregate_free_text_or_foreign_key(qs, subrecord, field_name):
    field_name = "{}_fk__name".format(field_name)
    annotated = qs.values(field_name).annotate(Count('id'))
    result = []
    for key_connection in annotated:
        total_count = key_connection.pop('id__count')
        key = key_connection.values()[0]
        result.append([str(key), total_count])
    return result


@register.inclusion_tag(
    'templatetags/trendy/gauge.html', takes_context=True
)
def missing_subrecord_gauge(
        context, queryset, subrecord_api_name, field, label
):
    total = queryset.count()
    count = 0

    if total == 0:
        amount = 0
    else:
        count = queryset.annotate(
            subrecord_count=Count(subrecord_api_name)
        ).filter(subrecord_count=0).count()

        amount = round(float(count)/total, 3) * 100
    context["total"] = total
    context["count"] = count
    context["label"] = label
    context["graph_vals"] = json.dumps(dict(
        aggregate=[['None', amount]],
        field=field,
        subrecord=subrecord_api_name
    ))
    return context


@register.inclusion_tag(
    'templatetags/trendy/gauge.html', takes_context=True
)
def empty_field_gauge(
        context, queryset, subrecord_api_name, field, label
):
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
    context["total"] = total
    context["count"] = count
    context["label"] = label
    context["graph_vals"] = json.dumps(dict(
        aggregate=[['None', amount]],
        field=field,
        subrecord=subrecord_api_name
    ))
    return context


@register.inclusion_tag(
    'templatetags/trendy/gauge.html', takes_context=True
)
def non_coded_gauge(
        context, queryset, subrecord_api_name, field, label
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

    context["total"] = total
    context["count"] = count
    context["label"] = label
    context["graph_vals"] = json.dumps(dict(
        aggregate=[['None', amount]],
        field=field,
        subrecord=subrecord_api_name
    ))
    return context


@register.inclusion_tag(
    'templatetags/trendy/pie_chart.html', takes_context=True
)
def pie_chart(
        context, queryset, subrecord_api_name, field, label
):
    subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
    result = aggregate_field(queryset, subrecord, field)
    context["label"] = label
    context["template"] = "templatetags/trendy/pie_chart.html"
    context["graph_vals"] = json.dumps(dict(
        aggregate=result,
        field=field,
        subrecord=subrecord_api_name
    ))
    return context


@register.inclusion_tag('templatetags/trendy/table.html', takes_context=True)
def trendy_table(context, queryset, subrecord_api_name, field_name):
    """
        returns subrecord api name, field, and an list of dictionaries

        in each dictionary,
            field_value = name of the field
            amount = the amount
            link = whether this should be a link onwards
        the list is ordered by -amount
    """
    result = aggregate_field(queryset, subrecord_api_name, field_name)
    # result.append(dict(field="Total", amount=queryset.count(), link=False))
    context["rows"] = [
        dict(field_value=k, amount=v, link=True) for k, v in result
    ]
    context["rows"].sort(key=lambda x: -x['amount'])
    context["field"] = field_name
    context["subrecord"] = subrecord_api_name
    return context
