from django.views.generic import TemplateView
from django.db.models.fields.related import ManyToManyField
from opal.core.views import LoginRequiredMixin
from opal import models
from opal.core.fields import ForeignKeyOrFreeText
# from trendy.trends import SubrecordTrend
from opal.core import patient_lists
from opal.core.subrecords import (
    get_subrecord_from_api_name, patient_subrecords
)
from opal.models import Episode
from opal.core.views import json_response


def get_qs_from_pl(pl):
    if hasattr(pl, "subtag"):
        return Episode.objects.all().filter(tagging__value=pl.subtag)
    elif hasattr(pl, "tag"):
        return Episode.objects.all().filter(tagging__value=pl.tag)
    else:
        return pl.get_queryset()


class AbstractTrendyFilterView(LoginRequiredMixin, TemplateView):

    def get_episodes_from_url(self, request):
        path = []
        listname = None
        pl_slug = self.request.GET.get('list', None)

        if pl_slug:
            pl = patient_lists.PatientList.get(pl_slug)
            qs = get_qs_from_pl(pl())
            listname = pl.display_name
        else:
            qs = models.Episode.objects.all()

        for k in request.GET.keys():
            for v in request.GET.getlist(k):
                if k == "list":
                    continue

                subrecord = get_subrecord_from_api_name(k.split("__")[0])
                field = k.split("__")[1]
                lookup = "{0}__{1}".format(subrecord.__name__.lower(), field)

                if subrecord in patient_subrecords():
                    lookup = "patient__{}".format(lookup)

                if isinstance(getattr(subrecord, field), ForeignKeyOrFreeText):
                    if v == 'None':
                        v = None
                        lookup = "{}_fk".format(lookup)
                    else:
                        lookup = "{}_fk__name".format(lookup)

                path.append(dict(
                    subrecord=subrecord.get_display_name(),
                    field=subrecord._get_field_title(field),
                    field_value=v
                ))

                qs = qs.filter(**{lookup: v})

        return listname, path, qs

    def get_context_data(self, **kwargs):
        listname, path, qs = self.get_episodes_from_url(self.request)
        context = {}
        context["listname"] = listname
        context["path"] = path
        context["obj_list"] = qs
        return context


class TrendyEpisodeView(AbstractTrendyFilterView):
    template_name = "trendy/trend_episodes.html"


class TrendyList(AbstractTrendyFilterView):
    template_name = "trendy/trend_list.html"


class TrendyView(AbstractTrendyFilterView):
    template_name = "trendy/trend_detail.html"
