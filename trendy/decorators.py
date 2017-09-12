from functools import wraps
import json


def append_to_path(request, query_param):
    full_path = request.get_full_path()
    if "?" not in full_path:
        return "{0}?{1}".format(full_path, query_param)
    else:
        return "{0}&{1}".format(full_path, query_param)


def link_from_subrecord(subrecord_api_name, field, aggregate, request):
    """
        provides the vanilla link to a subrecord field, e.g.
        demographics__sex=Femail
    """
    result = {}
    for i in aggregate:
        result[i[0]] = append_to_path(
            request,
            "{0}__{1}={2}".format(subrecord_api_name, field, i[0]),
        )
    return result


def link_from_trend(
    trend_api_name, func_name, aggregate, request, field=None
):
    """
        returns
            subrecord__t__function__field=value
        or
            subrecord__t__function=value
    """
    result = {}
    from trendy.trends import Trend
    trend = Trend.get_trend(trend_api_name)
    trend_query = "{}_query".format(func_name)
    if not hasattr(trend, trend_query):
        raise NotImplementedError("{0} needs a method called {1}".format(
            trend_api_name, trend_query
        ))

    for i in aggregate:
        if field:
            result[i[0]] = append_to_path(
                request, "{0}__t__{1}__{2}={3}".format(
                    trend_api_name,
                    func_name,
                    field,
                    i[0]
                )
            )
        else:
            result[i[0]] = append_to_path(
                request, "{0}__t__{1}={2}".format(
                    trend_api_name,
                    func_name,
                    i[0]
                )
            )
    return result


def bar_link_from_trend(
    trend_api_name, func_name, aggregate, request, field=None
):
    """
        returns
            subrecord__t__function__field=value
        or
            subrecord__t__function=value
    """
    result = {}
    from trendy.trends import Trend
    trend = Trend.get_trend(trend_api_name)
    trend_query = "{}_query".format(func_name)
    if not hasattr(trend, trend_query):
        raise NotImplementedError("{0} needs a method called {1}".format(
            trend_api_name, trend_query
        ))

    for i in aggregate[0][1:]:
        if field:
            result[i] = append_to_path(
                request, "{0}__t__{1}__{2}={3}".format(
                    trend_api_name,
                    func_name,
                    field,
                    i
                )
            )
        else:
            result[i] = append_to_path(
                request, "{0}__t__{1}={2}".format(
                    trend_api_name,
                    func_name,
                    i
                )
            )
    return result


def trend_method_wrap(aggregate_function):
    def subrecord_attr_wrap_with_template(f):
        @wraps(f)
        def wrapper(
            self,
            queryset,
            subrecord_api_name,
            request,
            field
        ):
            """
                adds 'links' to the context dictionary which is an dictionary
                of keys to links to that sub.
            """
            aggregate = f(self, queryset, subrecord_api_name, request, field)
            result = {}
            result["graph_vals"] = json.dumps(dict(
                aggregate=aggregate,
                links=aggregate_function(
                    subrecord_api_name,
                    field,
                    aggregate,
                    request
                )
            ))
            return result
        return wrapper
    return subrecord_attr_wrap_with_template


subrecord_attr = trend_method_wrap(link_from_subrecord)
trend_attr = trend_method_wrap(link_from_trend)
