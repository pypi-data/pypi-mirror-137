import click
import pypelinez.git as git
from pypelinez.click_ext import assertUsage, assertBadParameter
import pypelinez.utilities as utilities


@click.group()
def release():
    pass


@release.command()
@click.argument("version")
def start(version):
    """Creates a new release branch"""

    assertBadParameter(utilities.validate_semantic_version(version), "Version must follow Semantic Versioning rules")

    assertUsage(git.current_branch() == "develop", "Must create feature from develop branch")

    click.echo("Creating release: release/" + version)

    git.create_branch("release/" + version)


# commit
@release.command()
def add_commit():

    git.add()

    git.commit()


@release.command()
def submit():
    """Submits the release as a merge request"""

    current, _, version = validate_release_branch()

    assertBadParameter(utilities.validate_semantic_version(version), "Version must follow Semantic Versioning rules")

    click.echo("Submitting " + current + " for release")

    merge_description = "Release " + version + " submission"

    git.merge_request("develop", merge_description)


# finish
@release.command()
def finish():
    current, _, version = validate_release_branch()

    assertBadParameter(utilities.validate_semantic_version(version), "Version must follow Semantic Versioning rules")

    git.change_to_branch("develop")

    git.pull("origin", "develop")

    git.delete(current)


def validate_release_branch():
    current = git.current_branch()

    branchInfo = current.split("/")

    branchType = branchInfo[0]

    assertUsage(branchType == "release", "Branch must be release/<version>")

    version = branchInfo[1]

    assertBadParameter(utilities.validate_semantic_version(version), "Version must follow Semantic Versioning rules")

    return (current, branchType, version)
