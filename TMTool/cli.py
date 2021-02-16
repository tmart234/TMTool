import click
from . import gui

@click.command()
def cli():
    gui.main()

if __name__ == '__main__':
    cli()