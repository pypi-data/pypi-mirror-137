import click
import pypelinez.git as git
from pypelinez.click_ext import assertUsage


# -------------------------- commands

# group
@click.group()
def feature():
    pass


# name
@feature.command()
def name():
    print(git.current_branch())


# start
@feature.command()
@click.argument("name")
def start(name):
    """Creates a new branch with the format feature/<name>


    Parameters:
    name (str): feature branch name

    """

    assertUsage(git.current_branch() == "develop", "Must create feature from develop branch")

    click.echo("Creating feature: feature/" + name)

    git.create_branch("feature/" + name)


# commit
@feature.command()
def add_commit():

    git.add()

    git.commit()


@feature.command()
def submit():

    merge_request_file = open("MERGE_REQUEST.md", "r")
    merge_description = merge_request_file.read()
    merge_request_file.close()

    git.merge_request("develop", merge_description)


# finish
@feature.command()
def finish():
    branch = git.current_branch()

    git.change_to_branch("develop")

    git.pull("origin", "develop")

    git.delete(branch)
