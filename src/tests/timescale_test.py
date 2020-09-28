import os
from timeit import default_timer as timer
from unittest.mock import call, patch

import psycopg2
import pytest
from click.testing import CliRunner

from timescale.main import (get_queries, main, perform_all_query,
                            perform_query, run_analytics, run_worker_pool)

CONNECTION = "postgres://docker:docker@localhost:5432/homework"

# Three examples of unit tests


def test_get_queries():
    result = get_queries(os.path.join(os.path.dirname(__file__), 'test.csv'))
    assert result[0]['host_000008'][0]['start'] == '2017-01-01 08:59:22'
    assert result[0]['host_000001'][0]['end'] == '2017-01-02 14:02:02'


@patch("timescale.main.perform_query")
def test_perform_all_query(mocked_perform_query):
    mocked_perform_query.return_value = 10
    test_queries = ['host_000008', [
        {'start': '2017-01-01 08:59:22', 'end': '2017-01-01 09:59:22'}]]
    query_times, build_statistic = perform_all_query(test_queries)
    assert query_times == [10]
    assert list(build_statistic[0].keys()) == [
        'host', 'pid', 'median', 'min', 'max', 'query_times']
    assert build_statistic[0]['host'] == 'host_000008'


def test_perform_query():
    with psycopg2.connect(CONNECTION) as conn:
        time = perform_query(conn, 'host_000008', {
                             'start': '2017-01-01 08:59:22', 'end': '2017-01-01 10:00:01'})
        assert isinstance(time, float)
    pass
