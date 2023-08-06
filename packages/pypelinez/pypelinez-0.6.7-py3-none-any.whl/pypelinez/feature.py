import click
import pypelinez.git as git
from pypelinez.click_ext import assertUsage


@click.group()
def feature():
    pass


@feature.command()
def name():
    """Adds and commits all changes to branch feature/<name>"""

    print(git.current_branch())


@feature.command()
@click.argument("name")
def start(name):
    """Creates a new branch with the format feature/<name>

    Parameters:
    name (str): feature branch name

    """

    if git.current_branch() == "develop":
        git.create_branch("feature/" + name)
    else:
        print("Must create feature from develop branch")

    assertUsage(git.current_branch() == "develop", "Must create feature from develop branch")

    click.echo("Creating feature: feature/" + name)

    git.create_branch("feature/" + name)


@feature.command()
def add_commit():
    """Adds and commits all changes to branch feature/<name>"""

    git.add()

    git.commit()


@feature.command()
def submit():
    """Submits merge request to develop for feature/<name>"""

    merge_request_file = open("MERGE_REQUEST.md", "r")
    merge_description = merge_request_file.read()
    merge_request_file.close()

    git.merge_request("develop", merge_description)


@feature.command()
def finish():
    """Finishes feature/<name>

    Assumes merge request was successful.
    Pulls from origin develop.
    Deletes the current feature/<name> branch

    """

    branch = git.current_branch()

    git.change_to_branch("develop")

    git.pull("origin", "develop")

    git.delete(branch)

    git.pull("origin", "develop")
