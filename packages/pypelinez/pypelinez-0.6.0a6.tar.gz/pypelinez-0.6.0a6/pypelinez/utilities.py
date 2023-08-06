import os
import subprocess
import sys
import shutil
import re

current = os.getcwd()

# -------------------------- utilities


def action(command, cwd=current):
    return subprocess.run(command, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def assert_result(result):
    if result.returncode != 0:
        sys.exit(result.returncode)


def transform_result(result):
    # https://stackoverflow.com/questions/41918836/how-do-i-get-rid-of-the-b-prefix-in-a-string-in-python
    return (result.stdout.decode("UTF-8") + result.stderr.decode("UTF-8")).strip()


def print_result(result):
    print(transform_result(result))


def remove_directory(directory):
    shutil.rmtree(directory)


def validate_semantic_version(version):
    version_regex = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"  # noqa: E501
    pattern = re.compile(version_regex)
    match = pattern.match(version)
    return match is not None


def get_semantic_version(text):
    version_regex = r"^.*((0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)$"  # noqa: E501
    pattern = re.compile(version_regex)
    match = pattern.match(text)
    return match
