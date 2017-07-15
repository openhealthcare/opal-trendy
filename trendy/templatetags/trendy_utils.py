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
