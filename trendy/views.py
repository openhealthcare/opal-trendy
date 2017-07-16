from django.views.generic import TemplateView
from opal.core.views import LoginRequiredMixin
from opal import models
from trendy.trends import SubrecordTrend
from opal.core import patient_lists
from opal.core.subrecords import get_subrecord_from_api_name


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
        context["path"] = []
        pl_slug = self.request.GET.get('list', None)

        if pl_slug:
            pl = patient_lists.PatientList.get(pl_slug)
            qs = pl().get_queryset()
            context["listname"] = pl.display_name
        else:
            qs = models.Episode.objects.all()

        for k in self.request.GET.keys():
            for v in self.request.GET.getlist(k):
                if k == "list":
                    continue

                subrecord = get_subrecord_from_api_name(k.split("__")[0])
                field_name = k.split("__")[1].rstrip("_fk")
                field = getattr(subrecord, field_name)
                related_model = field.foreign_model

                context["path"].append(dict(
                    subrecord=subrecord.get_display_name(),
                    field_value=v
                ))

                related_id = related_model.objects.filter(
                    name=v
                )

                qs = qs.filter(**{k: related_id})

        context["obj"] = SubrecordTrend().get_request_information(qs)

        return context
