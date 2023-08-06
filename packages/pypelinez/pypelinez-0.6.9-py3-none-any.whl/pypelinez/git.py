import pypelinez.utilities as utilities


def current_branch():
    """Current git branch name

    Returns:
    str:Returning current git branch name

    """

    result = utilities.action("git rev-parse --abbrev-ref HEAD")
    utilities.assert_result(result)
    return utilities.transform_result(result)


def create_branch(name):
    """Creates a new branch with <name> based on the current branch

    Returns:
    str:Returning current git branch name

    """

    result = utilities.action("git checkout -b " + name)
    utilities.print_result(result)
    utilities.assert_result(result)


def change_to_branch(name):
    result = utilities.action("git checkout " + name)
    utilities.print_result(result)
    utilities.assert_result(result)


def add():
    result = utilities.action("git add -A")
    utilities.print_result(result)
    utilities.assert_result(result)


def commit():
    result = utilities.action("git commit -F COMMIT.md")
    utilities.print_result(result)
    utilities.assert_result(result)


def merge(branch):
    result = utilities.action("git merge --squash " + branch)
    utilities.print_result(result)
    utilities.assert_result(result)


def delete(branch):
    result = utilities.action("git branch -D " + branch)
    utilities.print_result(result)
    utilities.assert_result(result)


def pull(source, branch):
    result = utilities.action("git pull " + source + " " + branch)
    utilities.print_result(result)
    utilities.assert_result(result)


# merge request
# https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html
def merge_request(target, description):
    current = current_branch()

    request = """\
    git push \\
    -o merge_request.create \\
    -o merge_request.target={target} \\
    -o merge_request.merge_when_pipeline_succeeds \\
    -o merge_request.remove_source_branch \\
    -o merge_request.title=\"Merge request for {current}\" \\
    -o merge_request.description=\"{description}\" \\
    origin {current}
  """.format(
        target=target, current=current, description=description
    )

    result = utilities.action(request)
    utilities.print_result(result)
    utilities.assert_result(result)


# merge request
# https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html
def release_request(version):

    branch = current_branch()

    request = """\
    git push \\
    -o merge_request.create \\
    -o merge_request.target=main \\
    -o merge_request.merge_when_pipeline_succeeds \\
    -o merge_request.remove_source_branch \\
    -o merge_request.title=\"Merge request for Release {version}\" \\
    -o merge_request.description=\"Release {version}\" \\
    origin {branch}
  """.format(
        version=version, branch=branch
    )

    result = utilities.action(request)
    utilities.print_result(result)
    utilities.assert_result(result)


def get_current_local_tag():
    result = utilities.action("git describe --tags --abbrev=0")
    utilities.assert_result(result)
    return str(result.stdout.decode("utf-8")).strip()


def get_current_remote_tags():
    result = utilities.action("git ls-remote --tags --sort=committerdate")
    utilities.assert_result(result)

    remote_versions = list(str(result.stdout.decode("utf-8")).split("\n"))

    if len(remote_versions) == 0:

        return []

    else:

        remote_versions = [i.strip() for i in remote_versions if i]

        remote_versions = list(map(lambda x: utilities.get_semantic_version(x), remote_versions))

        remote_versions = [i for i in remote_versions if i]

        remote_versions = [str(i.group(1)) for i in remote_versions if i]

        return list(reversed(remote_versions))


def create_tag(version):
    result = utilities.action("git tag -a " + version + " -m " + version)
    utilities.print_result(result)
    utilities.assert_result(result)
