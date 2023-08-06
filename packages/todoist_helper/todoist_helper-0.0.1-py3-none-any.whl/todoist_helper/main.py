"""Main module."""
import click

from .add_todoist_task import add_todoist_task


@click.group()
def cli():
    """
    Main group.
    """


@click.command()
def add():
    """
    Add a new todoist task to the inbox.
    """
    add_todoist_task()
    click.echo("Logged.")


cli.add_command(add)
