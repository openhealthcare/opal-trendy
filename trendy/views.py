from django.views.generic import TemplateView
from trends import SubrecordTrend
# from opal.core import patient_lists


"""
Views for the trendy Opal Plugin
"""
# from django.views.generic import View

# You might find these helpful !
# from opal.core.views import LoginRequiredMixin, json_response


class TrendyList(TemplateView):
    template_name = "trendy/trend_list.html"

    def get_context_data(self, *args, **kwargs):
        return SubrecordTrend().get_request_information()


class TrendyView(TemplateView):
    template_name = "trendy/trend_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TrendyView, self).get_context_data(**kwargs)
        context["obj"] = SubrecordTrend().get_request_information()
        return context
