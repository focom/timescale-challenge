import click
# from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

CONNECTION = "postgres://docker:docker@localhost:5432/homework"

@click.group()
def main():
  pass

@click.command()
@click.option("-w","--worker", type=int, default=2, prompt="Number of concurent clients", help="hehe")
@click.argument("filepath", type=click.Path('r'))
def hello(worker, file):
    """Test program for timescale"""
    click.echo(f"Hello, Pedro!")

main.add_command(hello)

if __name__ == '__main__':
    main()
