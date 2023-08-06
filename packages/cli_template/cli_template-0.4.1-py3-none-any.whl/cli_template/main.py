"""Main module."""
import click


@click.group()
def cli():
    """
    Main group.
    """


@click.command()
def initdb():
    """
    Example command.
    """
    click.echo("Initialized the database")


@click.command()
def dropdb():
    """
    Another example command.
    """
    click.echo("Dropped the database")


cli.add_command(initdb)
cli.add_command(dropdb)
