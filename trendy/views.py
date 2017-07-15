from django.views.generic import TemplateView
from opal.core.views import LoginRequiredMixin
from opal import models
from trendy.trends import SubrecordTrend
from opal.core import patient_lists


class TrendyList(LoginRequiredMixin, TemplateView):
    template_name = "trendy/trend_list.html"

    def get_context_data(self, *args, **kwargs):
        result = []
        for l in patient_lists.PatientList.list():
            result.append(dict(
                display_name=l.display_name,
                slug=l.get_slug(),
                count=l().get_queryset().count()
            ))
        return dict(obj_list=sorted(result, key=lambda x: -x["count"]))


class TrendyView(LoginRequiredMixin, TemplateView):
    template_name = "trendy/trend_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TrendyView, self).get_context_data(**kwargs)
        pl_slug = self.request.GET.get('list', None)
        if pl_slug:
            pl = patient_lists.PatientList.get(pl_slug)
            qs = pl.get_queryset()
        else:
            qs = models.Episode.objects.all()
        context["obj"] = SubrecordTrend().get_request_information(qs)
        return context
