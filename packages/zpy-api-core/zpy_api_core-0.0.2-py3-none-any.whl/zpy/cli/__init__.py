from typing import List, Dict

from zpy.cli.agregations import add_config
from zpy.cli.scaffolding import scaffolding_dispatcher

import click


@click.group()
def cli():
    """This is an example script to learn Click."""


@cli.command()
@click.option('--project', '-p', required=True, type=str, help='Project name')
@click.option('--verbose', '-v', required=False, is_flag=True, default=False, help='Show logs')
@click.option('--description', '-d', required=False, type=str, help='Project description',
              default="This is very boring haha xd...")
@click.option('--developer', '-dev', required=False, type=str, help='Author', default="Zurck'z 2022")
@click.option('--context', '-c', required=False, type=str, help='Context name', default="Users")
@click.option('--use_case', '-uc', required=False, type=str, help='Use Case Name', default="GetUser")
@click.option('--developer_url', '-dev-url', required=False, type=str, help='Author url',
              default="https://www.linkedin.com/in/zurckz/")
@click.option('--open_project', '-op', required=False, is_flag=True, default=False, help='Open project')
@click.option('--only_content', '-oc', required=False, is_flag=True, default=False,
              help='Create only structure project')
def make(project, verbose, description, developer, context, use_case, developer_url, open_project,
         only_content):
    in_data: List[Dict[str, str]] = [{"value": project, "title": "Project name:"},
                                     {"value": description, "title": "Project description:"},
                                     {"value": developer, "title": "Author:"},
                                     {"value": developer_url, "title": "Url Author:"},
                                     {"value": context.lower(), "title": "Context:"},
                                     {"value": use_case, "title": "Use Case:"},
                                     {"value": context.title(), "title": "Repository"},
                                     {"value": open_project, "title": "Open Project?:"},
                                     {"value": only_content, "title": "Only Content?:"},
                                     None
                                     ]
    if verbose is True:
        click.echo(f'\N{grinning face} - Initializing for create new project...')
        for data in in_data:
            if data is not None:
                click.echo(f'\N{grinning face} - With {data["title"]} {data["value"]}')

    scaffolding_dispatcher(in_data, verbose, click)


@cli.group()
def add():
    ...


@add.command()
@click.option('--database', '-db', required=True, type=bool, is_flag=True, help='Database configuration')
def config(database: bool):
    add_config(database)


@cli.command()
def drop():
    click.echo('Dropping...')
