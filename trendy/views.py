from django.views.generic import TemplateView
from trends import SubrecordTrend


"""
Views for the trendy Opal Plugin
"""
# from django.views.generic import View

# You might find these helpful !
# from opal.core.views import LoginRequiredMixin, json_response


class TrendyView(TemplateView):
    template_name = "trendy/trend_detail.html"

    def get_context_data(self, *args, **kwargs):
        return SubrecordTrend().get_request_information()
