import click
import pypelinez.git as git
from pypelinez.click_ext import assertLocalVersionIsLatest, assertUsage, assertBadParameter
import pypelinez.utilities as utilities
from semantic_version import Version


@click.group()
def publish():
    pass


# start
@publish.command()
def start():

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

    git.create_branch("publish/" + latest_local_version)

    git.merge_request("main", "Publishing " + latest_local_version)
