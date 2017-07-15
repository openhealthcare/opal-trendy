from django.views.generic import TemplateView
from opal.core.views import LoginRequiredMixin
from trendy.trends import SubrecordTrend
# from opal.core import patient_lists
import ipdb; ipdb.set_trace()



class TrendyList(LoginRequiredMixin, TemplateView):
    template_name = "trendy/trend_list.html"

    def get_context_data(self, *args, **kwargs):
        return SubrecordTrend().get_request_information()


class TrendyView(LoginRequiredMixin, TemplateView):
    template_name = "trendy/trend_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TrendyView, self).get_context_data(**kwargs)
        context["obj"] = SubrecordTrend().get_request_information()
        return context
