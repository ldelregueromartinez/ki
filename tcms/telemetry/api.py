from django.db.models import CharField, Count, Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from modernrpc.auth.basic import http_basic_auth_login_required
from modernrpc.core import rpc_method

from tcms.testcases.models import TestCase
from tcms.testruns.models import TestExecution, TestExecutionStatus


@http_basic_auth_login_required
@rpc_method(name="Testing.breakdown")
def breakdown(query=None):
    """
    .. function:: RPC Testing.breakdown(query)

        Perform a search and return the statistics for the selected test cases

        :param query: Field lookups for :class:`tcms.testcases.models.TestCase`
        :type query: dict
        :return: Object, containing the statistics for the selected test cases
        :rtype: dict
    """

    if query is None:
        query = {}

    test_cases = TestCase.objects.filter(**query).distinct()

    manual_count = test_cases.filter(is_automated=False).count()
    automated_count = test_cases.filter(is_automated=True).count()
    count = {
        "manual": manual_count,
        "automated": automated_count,
        "all": manual_count + automated_count,
    }

    priorities = _get_field_count_map(test_cases, "priority", "priority__value")
    categories = _get_field_count_map(test_cases, "category", "category__name")

    return {
        "count": count,
        "priorities": priorities,
        "categories": categories,
    }


def _get_field_count_map(test_cases, expression, field):
    query_set_confirmed = (
        test_cases.filter(case_status__is_confirmed=True)
        .values(field)
        .annotate(count=Count(expression, distinct=True))
    )
    query_set_not_confirmed = (
        test_cases.exclude(case_status__is_confirmed=True)
        .values(field)
        .annotate(count=Count(expression, distinct=True))
    )
    return {
        str(_("CONFIRMED")): _map_query_set(query_set_confirmed, field),
        str(_("OTHER")): _map_query_set(query_set_not_confirmed, field),
    }


def _map_query_set(query_set, field):
    return {entry[field]: entry["count"] for entry in query_set}


@http_basic_auth_login_required
@rpc_method(name="Testing.status_matrix")
def status_matrix(query=None):
    """
    .. function:: RPC Testing.status_matrix(query)

        Perform a search and return data_set needed to visualize the status matrix
        of test plans, test cases and test executions

        :param query: Field lookups for :class:`tcms.testcases.models.TestPlan`
        :type query: dict
        :return: A dictionary, containing the information about test executions
        :rtype: dict
    """
    if query is None:
        query = {}

    base_query = TestExecution.objects.filter(**query)

    test_cases = list(
        base_query.values("case_id", "case__summary").order_by("case_id").distinct()
    )
    test_executions = {}
    for execution in base_query.values(
        "pk",
        "case_id",
        "run_id",
        "status_id",
        key=Concat("case_id", Value("-"), "run_id", output_field=CharField()),
    ):
        test_executions[execution["key"]] = execution

    # test run summaries for column hints, keyed by TR.pk
    test_runs = dict(
        base_query.values_list("run_id", "run__summary").order_by("run_id").distinct()
    )
    # test plan IDs, keyed by TR.pk
    test_plans = dict(base_query.values_list("run_id", "run__plan").distinct())

    status_colors = dict(TestExecutionStatus.objects.values_list("pk", "color"))

    return {
        "cases": test_cases,
        "executions": test_executions,
        "plans": test_plans,
        "runs": test_runs,
        "statusColors": status_colors,
    }


@http_basic_auth_login_required
@rpc_method(name="Testing.execution_trends")
def execution_trends(query=None):
    if query is None:
        query = {}

    data_set = {}
    categories = []
    colors = []
    counts = {}

    for status in TestExecutionStatus.objects.all():
        data_set[status.name] = []
        colors.append(status.color)
    data_set[str(_("TOTAL"))] = []
    colors.append("black")

    status_count = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }
    run_id = 0
    for test_execution in (
        TestExecution.objects.filter(**query)
        .select_related("status")
        .order_by("run_id")
    ):
        status = test_execution.status

        if status.weight > 0:
            status_count["positive"] += 1
        elif status.weight < 0:
            status_count["negative"] += 1
        else:
            status_count["neutral"] += 1

        if test_execution.run_id == run_id:
            if status.name in counts:
                counts[status.name] += 1
            else:
                counts[status.name] = 1

        else:
            _append_status_counts_to_result(counts, data_set)

            counts = {status.name: 1}
            run_id = test_execution.run_id
            categories.append(run_id)

    # append the last result
    _append_status_counts_to_result(counts, data_set)

    for _key, value in data_set.items():
        del value[0]

    return {
        "categories": categories,
        "data_set": data_set,
        "colors": colors,
        "status_count": status_count,
    }


def _append_status_counts_to_result(counts, result):
    total = 0
    for status_name in filter(lambda x: x != _("TOTAL"), result.keys()):
        status_count = counts.get(status_name, 0)
        result.get(status_name).append(status_count)

        total += status_count

    result.get(str(_("TOTAL"))).append(total)


@http_basic_auth_login_required
@rpc_method(name="Testing.test_case_health")
def test_case_health(query=None):
    if query is None:
        query = {}

    all_test_executions = TestExecution.objects.filter(**query)

    test_executions = _get_count_for(all_test_executions)
    failed_test_executions = _get_count_for(
        all_test_executions.filter(status__weight__lt=0)
    )

    data = {}
    for value in test_executions:
        data[value["case_id"]] = {
            "case_id": value["case_id"],
            "case_summary": value["case__summary"],
            "count": {"all": value["count"], "fail": 0},
        }

    _count_test_executions(data, failed_test_executions, "fail")

    # remove all with 100% success rate, because they are not interesting
    _remove_all_excellent_executions(data)

    data = list(data.values())
    data.sort(key=_sort_by_failing_rate, reverse=True)

    if len(data) > 30:
        data = data[:30]

    return data


@http_basic_auth_login_required
@rpc_method(name="Testing.individual_test_case_health")
def individual_test_case_health_simple(query=None):
    if query is None:
        query = {}

    res = (
        TestExecution.objects.filter(**query)
        .values("run__plan", "case_id", "status__name", "status__weight")
        .order_by("case", "run__plan", "status__weight")
    )

    return list(res)


def _remove_all_excellent_executions(data):
    for key in dict.fromkeys(data):
        if data[key]["count"]["fail"] == 0:
            data.pop(key)


def _count_test_executions(data, test_executions, status):
    for value in test_executions:
        data[value["case_id"]]["count"][status] = value["count"]


def _sort_by_failing_rate(element):
    return element["count"]["fail"] / element["count"]["all"]


def _get_count_for(test_executions):
    return (
        test_executions.values("case_id", "case__summary")
        .annotate(count=Count("case_id"))
        .order_by("case_id")
    )
