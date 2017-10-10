from __future__ import unicode_literals


from django import template
import json
from opal.core.views import OpalSerializer
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


@register.inclusion_tag(
    'templatetags/trendy/default_trend.html', takes_context=True
)
def trend_panel(
        context, subrecord
):
    fk_ft_fields = []
    fieldnames = [f.attname for f in subrecord.__class__._meta.fields]
    fk_ft_fields = [f[:-6] for f in fieldnames if f.endswith('_fk_id')]
    context["subrecord"] = subrecord
    context["is_singleton"] = subrecord._is_singleton
    context["fk_ft_fields"] = fk_ft_fields
    return context
