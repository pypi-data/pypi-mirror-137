#!/usr/bin/env python3

import click
from pypelinez.feature import feature
from pypelinez.release import release
from pypelinez.publish import publish

from pypelinez.apple import apple
from pypelinez.python import python


@click.group()
@click.version_option()
def main():
    pass


main.add_command(feature)
main.add_command(release)
main.add_command(publish)

main.add_command(apple)
main.add_command(python)

if __name__ == "__main__":
    main()
