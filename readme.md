# Timescale assignment

## Installation

To install the depedencies, you need poetry.
To install poetry go here: https://python-poetry.org/docs/#installation
Then run this
```bash
poetry install
```
Now you need to have the test timescale instance running.
For this you can use the makefile which wrap docker command. (Note I use sudo to interact with the docker deamon)
Follow those steps:
1. Build the docker image
  ```bash
  make build
  ```
2. Run the postgres server
  ```bash
  make run
  ```
Now you have everything to test the tool.
## Use the cli tool
Once you have poetry and installed the depedencies you can run the tool with
this command:
```bash
poetry run python src/timescale/main.py process setup-files/query_params.csv -w <number of process>
```
The tool will output something like:
```
Starting computations with 12 process

        Stats accross all queries:
            Number of queries performed: 200
            Time to perform all queries: 0.10700366800301708
            Minimum query time: 0.0013296249962877482
            Maximum query time: 0.010922279994701967
            Mean query time: 0.0025623715747497043
            Median query time: 0.0023742880002828315
```
## Unittests
To run the unittests, you need to complete the installation steps then use this command:
```bash
poetry run pytest
```
## Conclusion

- The tool complete its purpose. I did notice that the median query time is similar accross
with different number of psql clients.
- Plus the CLI does split the query in different process as the overall time to perform the queries is cut in half. (time for 2 workers compared to 4)