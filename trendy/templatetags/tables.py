"""
Dashboard template tags
"""
from django import template
from copy import copy

register = template.Library()


@register.inclusion_tag('templatetags/table.html', includes_context=True)
def table(
    ctx, rows, table_headers, table_class=None
):
    """
        example args:
        table_headers = ["author", "book count"]
        rows = [
            ("Roald Dahl", "http://authors.com/roalddahl"), (3, None)
        ]

        rows is a list of rows.
        each row has the column value in order
        the column value is a tuple, if there are two elements
        then its treated as a link
    """
    return_ctx = copy(ctx)

    if not table_headers:
        table_headers = rows.keys()
    return_ctx["table_data"] = dict(
        rows=rows,
        table_headers=table_headers
    )
    return return_ctx
