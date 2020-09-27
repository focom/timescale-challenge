import csv
import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count

CONNECTION = "postgres://docker:docker@localhost:5432/homework"

def get_queries(csv_filepath):
    queries = {}
    with open(csv_filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                try:
                    queries[row[0]].append({'start':row[1],'end':row[2]})
                except KeyError as err:
                    queries[row[0]] = [{'start':row[1],'end':row[2]}]
            line_count += 1
    return queries

def perform_query():
    example = [{'start': '2017-01-02 13:02:02', 'end': '2017-01-02 14:02:02'}

def run_worker_pool():
    start = timer()
    print(f'starting computations on {cpu_count()} cores')
    queries = get_queries(csv_filepath)
    with Pool() as pool:
        res = pool.map(square, queries)
        print(res)
    end = timer()
    print(f'elapsed time: {end - start}')


get_queries("./setup-files/query_params.csv")