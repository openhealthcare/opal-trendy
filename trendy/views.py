from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from opal.core.views import LoginRequiredMixin
from opal import models
from opal.core.fields import ForeignKeyOrFreeText
from trendy.trends import Trendy
# from trendy.trends import SubrecordTrend
from opal.core import patient_lists
from opal.core.subrecords import (
    get_subrecord_from_api_name, patient_subrecords
)
from opal.models import Episode


def get_qs_from_pl(pl):
    if hasattr(pl, "subtag"):
        return Episode.objects.all().filter(tagging__value=pl.subtag)
    elif hasattr(pl, "tag"):
        return Episode.objects.all().filter(tagging__value=pl.tag)
    else:
        return pl.get_queryset()


def get_path_and_qs_from(get_param, value, qs):
    subrecord = get_subrecord_from_api_name(get_param.split("__")[0])
    field = get_param.split("__")[1]

    lookup = "{0}__{1}".format(subrecord.__name__.lower(), field)

    if subrecord in patient_subrecords():
        lookup = "patient__{}".format(lookup)

    if isinstance(getattr(subrecord, field), ForeignKeyOrFreeText):
        if value == 'None':
            value = None
            lookup = "{}_fk".format(lookup)
        else:
            lookup = "{}_fk__name".format(lookup)

    path = (
        "{0}-{1}: {2}".format(
            subrecord.get_display_name(),
            subrecord._get_field_title(field),
            value
        )
    )

    qs = qs.filter(**{lookup: value})
    return path, qs


def get_trend_and_qs_from(get_param, value, qs):
    # the query string is made up of trend__t__function__field=value
    split_query = get_param.split("__")
    field = None
    if len(split_query) == 4:
        trend_api_name, _, trend_function, field = split_query
    else:
        trend_api_name, _, trend_function = split_query

    trend_function = "{}_query".format(trend_function)
    trend = Trend.get_trend(trend_api_name)()
    some_fun = getattr(trend, trend_function)
    qs = some_fun(qs, trend, value=value, field=field)
    path = "{0}-{1}:{2}".format(
        trend.get_display_name(),
        trend_function.replace("_", " "),
        value
    )
    return path, qs


class AbstractTrendyFilterView(LoginRequiredMixin, TemplateView):
    template_name = "trendy/trend_detail.html"

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

                trend = Trendy.get_from_get_param(request, k)
                qs = trend.query(v, qs)
                path.append(trend.get_description(v))

        return listname, path, qs

    def get_context_data(self, *args, **kwargs):
        listname, path, qs = self.get_episodes_from_url(self.request)
        context = {}
        context["listname"] = listname
        context["path"] = path
        context["obj_list"] = qs
        return context

teams = dict(
    opat="OPAT",
    walkin="Walkin",
    id_inpatients="ID Inpatients"
)


class TrendyPatientList(AbstractTrendyFilterView):
    template_name = "trendy/trend_detail.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(TrendyPatientList, self).get_context_data(*args, **kwargs)
        ctx["obj_list"] = ctx["obj_list"].filter(
            tagging__value=self.kwargs["list"]
        )
        ctx["title"] = teams[self.kwargs["list"]]
        ctx["title_url"] = reverse(
            "trendy_patient_list", kwargs={"list": self.kwargs["list"]}
        )

        return ctx


class TrendyList(TemplateView):
    template_name = "trendy/trend_list.html"

    def get_context_data(self, *args, **kwargs):

        ctx = super(TrendyList, self).get_context_data(*args, **kwargs)
        ctx["lists"] = []
        for k, v in teams.items():
            ctx["lists"].append(dict(
                display_name=v,
                slug=k,
                episode_count=Episode.objects.filter(
                    tagging__value=k
                ).count()
            ))

        return ctx
