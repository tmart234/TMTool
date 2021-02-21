import click
from . import gui
import traceback

@click.command()
def cli():
    try:
        gui.main()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        quit()
    return

def main():
    cli()
    quit()

if __name__ == '__main__':
    main()