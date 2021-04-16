import click
from . import gui
import traceback

@click.command()
def cli():
    gui.main()
    quit()

def main():
    cli()
    quit()

if __name__ == '__main__':
    main()