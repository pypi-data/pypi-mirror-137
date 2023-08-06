import platform
from os import getenv
from pathlib import Path
from subprocess import PIPE, CalledProcessError, check_call, check_output

import questionary
from click import secho


def echo(message):
    secho(message, fg="green")


def error(message, code=1):
    secho(f"ERROR: {message}", err=True, fg="red")
    exit(code)


def prompt(text, default="", prompt_suffix=":"):
    return questionary.text(f"{text}{prompt_suffix}", default=default).ask()


def checkbox(text, choices):
    return questionary.checkbox(text, choices=choices).ask()


def select(text, choices):
    return questionary.select(text, choices=choices).ask()


def confirm(text):
    return questionary.confirm(text).ask()


fossil = getenv("FOSSIL", "fossil")


def run(args):
    try:
        return check_output(args, stderr=PIPE).decode().strip()
    except CalledProcessError as e:
        error(e.stderr.decode(), e.returncode)


def shell(args):
    try:
        return check_call(args, stderr=PIPE)
    except CalledProcessError as e:
        exit(e.returncode)


def run_pre_pos(filename, **kwords):
    if platform.system() == "Windows":
        _file = Path(f".fossil_cli/none").with_stem(filename).with_suffix(".bat")
    else:
        _file = Path(f".fossil_cli/none").with_stem(filename).with_suffix(".sh")

    if _file.exists():
        for line in _file.read_text().splitlines():
            if line:
                run(line.format(**kwords))
