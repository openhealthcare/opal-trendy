from django import template
from trendy.trends import Trendy

register = template.Library()


@register.inclusion_tag(
    'templatetags/trendy/gauge.html', takes_context=True
)
def gauge_trend(
    context, function, queryset, subrecord_api_name, label=None, field=None
):
    trend_cls = Trendy.get(function)
    trend = trend_cls(
        subrecord_api_name, field_name=field, request=context["request"]
    )
    context.update(trend.get_graph_data(queryset))
    if label:
        context["label"] = label
    else:
        context["label"] = trend.label

    return context


@register.inclusion_tag(
    'templatetags/trendy/pie_chart.html', takes_context=True
)
def pie_chart(
        context, function, queryset, subrecord_api_name, field=None, label=None
):
    trend_cls = Trendy.get(function)
    trend = trend_cls(
        subrecord_api_name, field_name=field, request=context["request"]
    )
    context.update(trend.get_graph_data(queryset))
    if label:
        context["label"] = label
    else:
        context["label"] = trend.label
    return context


@register.inclusion_tag(
    'templatetags/trendy/bar_chart.html', takes_context=True
)
def bar_chart(
        context, function, queryset, subrecord_api_name, field=None, label=None
):

    trend_cls = Trendy.get(function)
    trend = trend_cls(
        subrecord_api_name, field_name=field, request=context["request"]
    )
    context.update(trend.get_graph_data(queryset))
    if label:
        context["label"] = label
    else:
        context["label"] = trend.label

    return context
