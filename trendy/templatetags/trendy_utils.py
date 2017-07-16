from django import template

register = template.Library()


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
def as_percentage_of(part, whole):
    try:
        return "%d%%" % (float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return ""


@register.assignment_tag(takes_context=True)
def in_request(context, subrecord_table, value, *args):
    subrecord = subrecord_table["subrecord"]
    field = subrecord_table["field"]
    field_key = "{0}__{1}".format(subrecord.get_api_name(), field)
    values = context["request"].GET.getlist(field_key, [])
    return value in values
