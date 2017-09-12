from django import template
import json
from opal.core.views import OpalSerializer
from trendy.trends import Trend


register = template.Library()


@register.simple_tag(takes_context=True)
def create_link(context, number):
    request = context["request"]
    url = request.get_full_path()
    if request.GET:
        sep = "&"
    else:
        sep = "?"
    newurl = sep.join(url.split(sep)[:number])
    return newurl.format(url)


@register.filter
def already_filtered(trend__field, request):
    return trend__field in request.GET


@register.simple_tag(takes_context=True)
def append_to_request(context, api_name, field, value):
    request = context["request"]
    url = request.get_full_path()

    if request.GET:
        url = "{}&".format(url)
    else:
        url = "{}?".format(url)

    return "{0}{1}__{2}={3}".format(
        url, api_name, field, value
    )


@register.filter
def as_json(subrecord, request):
    return json.dumps([subrecord.to_json(request.user)], cls=OpalSerializer)


def trend_template(subrecord_api_name):
    trend = Trend.get_trend(subrecord_api_name)

    if trend is None:
        return Trend.template_name
    else:
        return trend.template_name

register.filter('trend_template', trend_template)
