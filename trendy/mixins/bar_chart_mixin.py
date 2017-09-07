# from opal.core import subrecords
# import json
# from trendy.utils import (
#     aggregate_free_text_or_foreign_key, get_subrecord_qs_from_episode_qs
# )


class BarChartMixin(object):
    """
        provides all pie chart methods
    """

    def subrecord_break_down(
        self,
        queryset,
        subrecord_api_name,
        get_params,
        user,
        field
    ):
        # we split out
        #
        # subrecord = subrecords.get_subrecord_from_api_name(subrecord_api_name)
        # result = aggregate_field(queryset, subrecord, field)
        context = {}
        # context["template"] = "templatetags/trendy/pie_chart.html"
        # context["graph_vals"] = json.dumps(dict(
        #     aggregate=result,
        #     field=field,
        #     subrecord=subrecord_api_name
        # ))
        return context
