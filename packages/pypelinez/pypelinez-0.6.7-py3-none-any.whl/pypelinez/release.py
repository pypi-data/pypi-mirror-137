import click
import pypelinez.git as git
from pypelinez.click_ext import assertUsage, assertBadParameter, assertLocalVersionIsLatest
import pypelinez.utilities as utilities
from semantic_version import Version


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

    git.create_tag(version)


# publish
@release.command()
def publish_start():

    assertUsage(git.current_branch() == "develop", "Must publish from a develop branch")

    latest_local_version = git.get_current_local_tag()

    click.echo("Latest local version is " + latest_local_version)

    assertBadParameter(
        utilities.validate_semantic_version(latest_local_version), "Version must follow Semantic Versioning rules"
    )

    remote_versions = git.get_current_remote_tags()

    if len(remote_versions) == 0:

        click.echo("No remote versions")

    else:
        latest_remote_version = remote_versions[0]

        click.echo("Latest remote version is " + latest_remote_version)

        assertLocalVersionIsLatest(
            Version(latest_local_version) > Version(latest_remote_version),
            "Latest remote version ["
            + latest_remote_version
            + "] is higher than latest local version ["
            + latest_local_version
            + "]",
        )

    click.echo("Creating publish request")

    git.create_branch("publish")

    git.merge_request("main", "Publishing " + latest_local_version)


def validate_release_branch():
    current = git.current_branch()

    branchInfo = current.split("/")

    branchType = branchInfo[0]

    assertUsage(branchType == "release", "Branch must be release/<version>")

    version = branchInfo[1]

    assertBadParameter(utilities.validate_semantic_version(version), "Version must follow Semantic Versioning rules")

    return (current, branchType, version)
