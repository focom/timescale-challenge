import csv
import itertools
import os
import re
import statistics
import sys
from datetime import datetime
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer

import click
import psycopg2

CONNECTION = "postgres://docker:docker@localhost:5432/homework"


def verify_csv_file(csv_path):
    with open(csv_path) as csv_file:
        try:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            assert dialect.delimiter == ',', 'Separator should be a comma'
        except Exception as err:
            click.echo(f'An error occured while reading the file: {repr(err)}')
            sys.exit(1)


def verify_timestamp_format(timestamp):
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except Exception as err:
        click.echo(f'Incorrect timestamp in the csv file: {repr(err)}')
        sys.exit(1)


def get_queries(csv_filepath):
    queries = {}
    verify_csv_file(csv_filepath)
    with open(csv_filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                verify_timestamp_format(row[1])
                verify_timestamp_format(row[2])
                try:
                    queries[row[0]].append({'start': row[1], 'end': row[2]})
                except KeyError:
                    queries[row[0]] = [{'start': row[1], 'end':row[2]}]
            line_count += 1
    return queries, line_count-1


def perform_all_query(queries):
    host = queries[0]
    timestamps = queries[1]
    query_times = []
    pid = os.getpid()
    with psycopg2.connect(CONNECTION) as conn:
        for timestamp in timestamps:
            query_time = perform_query(conn, host, timestamp)
            query_times.append(query_time)
    return query_times, build_statistic(host, pid, query_times)


def build_statistic(host, pid, query_times):
    result = [{
        'host': host,
        'pid': pid,
        'median': statistics.median(query_times),
        'min': min(query_times),
        'max': max(query_times),
        'query_times': query_times
    }]
    return result


def perform_query(conn, host, timestamps):
    SQL = "SELECT usage FROM cpu_usage WHERE host=%s AND ts > %s AND ts < %s;"
    start = timer()
    cur = conn.cursor()
    cur.execute(SQL, (host, timestamps['start'], timestamps['end']))
    cur.fetchall()
    end = timer()
    return end - start


def run_worker_pool(csv_filepath, nb_process=cpu_count()):
    print(f'Starting computations with {nb_process} process')
    start = timer()
    queries, nb_queries = get_queries(csv_filepath)
    with Pool(nb_process) as pool:
        res = pool.map(perform_all_query, list(queries.items()))
    end = timer()
    query_times = []
    for perf in res:
        query_times.append(perf[0])
    query_times = list(itertools.chain(*query_times))
    print(f"""
        Stats accross all queries:
            Number of queries performed: {nb_queries}
            Time to perform all queries: {end - start}
            Minimum query time: {min(query_times)}
            Maximum query time: {max(query_times)}
            Mean query time: {sum(query_times)/len(query_times)}
            Median query time: {statistics.median(query_times)}
    """)


@click.group()
def main():
    pass


@click.command("process")
@click.option("-w", "--worker", type=click.IntRange(1, os.cpu_count()), default=os.cpu_count(),
              prompt="Choose the number of process to use",
              help="Number of process that will process the queries")
@click.argument("filepath", type=click.Path('r'))
def run_analytics(worker, filepath):
    """Test program for timescale"""
    run_worker_pool(filepath, worker)


main.add_command(run_analytics)

if __name__ == '__main__':
    main()
