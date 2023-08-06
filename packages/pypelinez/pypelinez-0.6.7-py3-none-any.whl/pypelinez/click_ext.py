import click


def assertUsage(state, message):
    if state is not True:
        raise click.UsageError(message)


def assertBadParameter(state, message):
    if state is not True:
        raise click.BadParameter(message)


def assertLocalVersionIsLatest(state, message):
    if state is not True:
        raise click.UsageError(message)
