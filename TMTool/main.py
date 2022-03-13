import click
import TMTool.gui as _gui

@click.command()
def main():
    _gui.main()

if __name__ == '__main__':
    main()