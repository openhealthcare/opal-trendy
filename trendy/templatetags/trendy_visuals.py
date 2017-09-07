from django import template
from trendy.trends import Trend
from opal.core import subrecords


register = template.Library()


def run_trend_function(
    context, function, queryset, subrecord_api_name, label=None, field=None
):
    trend = Trend.get_trend(subrecord_api_name)()
    if not label:
        if not field:
            raise "Unable to calculate the label without a field"

        subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
        label = subrecord._get_field_title(field)

    args = [
        queryset,
        subrecord_api_name,
        context["request"].GET,
        context["user"]
    ]

    if field:
        args.append(field)
    result = getattr(trend, function)(*args)
    result["label"] = label
    return result


@register.inclusion_tag(
    'templatetags/trendy/gauge.html', takes_context=True
)
def gauge_trend(
    context, function, queryset, subrecord_api_name, label=None, field=None
):
    context.update(run_trend_function(
        context, function, queryset, subrecord_api_name, label, field=field
    ))
    return context


@register.inclusion_tag(
    'templatetags/trendy/pie_chart.html', takes_context=True
)
def pie_chart(
        context, function, queryset, subrecord_api_name, field=None, label=None
):

    context.update(run_trend_function(
        context, function, queryset, subrecord_api_name, label, field=field
    ))
    return context


@register.inclusion_tag(
    'templatetags/trendy/bar_chart.html', takes_context=True
)
def bar_chart(
        context, function, queryset, subrecord_api_name, field=None, label=None
):

    context.update(run_trend_function(
        context, function, queryset, subrecord_api_name, label, field=field
    ))
    return context



# @register.inclusion_tag('templatetags/trendy/table.html', takes_context=True)
# def trendy_table(context, queryset, subrecord_api_name, field_name):
#     """
#         returns subrecord api name, field, and an list of dictionaries
#
#         in each dictionary,
#             field_value = name of the field
#             amount = the amount
#             link = whether this should be a link onwards
#         the list is ordered by -amount
#     """
#     result = aggregate_field(queryset, subrecord_api_name, field_name)
#     # result.append(dict(field="Total", amount=queryset.count(), link=False))
#     context["rows"] = [
#         dict(field_value=k, amount=v, link=True) for k, v in result
#     ]
#     context["rows"].sort(key=lambda x: -x['amount'])
#     context["field"] = field_name
#     context["subrecord"] = subrecord_api_name
#     return context
