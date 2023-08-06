import click
import os
import pypelinez.utilities as utilities
import pypelinez.git as git
import toml


def get_config():
    cwd = os.getcwd()
    file = open(os.path.join(cwd, "pyproject.toml"), "r", encoding="utf8")
    config = toml.loads(file.read())
    file.close()
    return config


# group
@click.group()
def python():
    pass


@python.group()
def version():
    pass


@version.command()
def get():
    result = utilities.action("poetry version -s", os.getcwd())
    utilities.print_result(result)
    utilities.assert_result(result)


# config = get_config()
# version = Version(config['tool']['poetry']['version'])
# print(version)


@version.command()
@click.argument(
    "value",
    type=click.Choice(
        ["major", "minor", "patch", "premajor", "preminor", "prepatch", "prerelease"], case_sensitive=False
    ),
)
def bump(value):
    def bumped(value):
        switch = {
            "major": "poetry version major",
            "minor": "poetry version minor",
            "patch": "poetry version patch",
            "premajor": "poetry version premajor",
            "preminor": "poetry version preminor",
            "prepatch": "poetry version prepatch",
            "prerelease": "poetry version prerelease",
        }
        return switch.get(value, "Invalid bump expectation")

    result = utilities.action(bumped(value), os.getcwd())
    utilities.print_result(result)
    utilities.assert_result(result)


@version.command()
def tag():
    current_branch = git.current_branch()
    if current_branch == "main":
        result = utilities.action("poetry version -s", os.getcwd())
        utilities.assert_result(result)
        git.tag(result)
    else:
        print("Must tag on main branch")
