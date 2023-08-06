import click
import os
import pypelinez.utilities as utilities


# group
@click.group()
def apple():
    pass


# format
@apple.command()
@click.option("--project-path", default="apple", help="Path for Apple project")
@click.option("--project-name", help="Project Name")
@click.option("--configuration", default=".swift-format.json", help="Format configuration file")
@click.argument("directories", nargs=-1)
def format(project_path, project_name, configuration, directories):

    workingDirectory = os.path.join(project_path, project_name)
    directories = " ".join(directories)

    command = """\
    swift format format -i --configuration {config} -r -p {dirs}
    """.format(
        config=configuration, dirs=directories
    )

    result = utilities.action(command, workingDirectory)
    utilities.print_result(result)
    utilities.assert_result(result)


# lint
@apple.command()
@click.option("--project-path", default="apple", help="Path for Apple project")
@click.option("--project-name", help="Project Name")
@click.option("--configuration", default=".swift-format.json", help="Format configuration file")
@click.argument("directories", nargs=-1)
def lint(project_path, project_name, configuration, directories):

    workingDirectory = os.path.join(project_path, project_name)
    directories = " ".join(directories)

    command = """\
    swift format lint --configuration {config} -r -p {dirs}
    """.format(
        config=configuration, dirs=directories
    )

    result = utilities.action(command, workingDirectory)
    utilities.print_result(result)
    utilities.assert_result(result)


# build
@apple.command()
@click.option("--project-path", default="apple", help="Path for Apple project")
@click.option("--project-name", help="Project Name")
@click.option("--platform", help="App platform")
@click.option("--test-platform", help="App test Platform")
@click.option("--device", help="Device name")
@click.option("--os-version", help="Device name")
def build_and_test(project_path, project_name, platform, test_platform, device, os_version):

    workingDirectory = os.path.join(project_path, project_name)

    testPath = os.path.join(
        "Tests",
        "Results",
        platform,
        os_version,
        device.replace(" ", "_"),
        "Results.xcresult",
    )

    utilities.remove_directory(os.path.join(workingDirectory, testPath))

    command = """\
    xcodebuild clean test -quiet -allowProvisioningUpdates \\
    -project "{project_name}.xcodeproj" -scheme "{project_name} ({platform})" \\
    -destination "platform={test_platform},name={device},OS={os_version}" \\
    -resultBundlePath "{testPath}"
    """.format(
        project_name=project_name,
        platform=platform,
        test_platform=test_platform,
        device=device,
        os_version=os_version,
        testPath=testPath,
    )

    print(workingDirectory)
    print(command)

    result = utilities.action(command, workingDirectory)
    utilities.print_result(result)
    utilities.assert_result(result)
