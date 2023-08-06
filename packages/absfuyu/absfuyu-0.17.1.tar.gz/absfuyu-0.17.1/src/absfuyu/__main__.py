#!/usr/bin/env python3
"""
CLI
"""
"""
ABSFUYU
-------
COMMAND LINE INTERFACE
"""


# Library
##############################################################
CLI_MODE = False

try:
    import click as __click
    import colorama as __colorama
except:
    print("This feature is in absfuyu[cli] package")
else:
    CLI_MODE = True

from .code_red import toggle_luckgod as __luck
from .config import show_cfg as __scfg
from .config import reset_cfg as __reset
from .generator import randStrGen as __randStr
from .version import __version__ as __v
from .version import check_for_update as __check_for_update




# Color stuff
##############################################################
__COLOR = {}
if CLI_MODE:
    __colorama.init(autoreset=True)
    __COLOR = {
        "green": __colorama.Fore.LIGHTGREEN_EX,
        "blue": __colorama.Fore.LIGHTCYAN_EX,
        "red": __colorama.Fore.LIGHTRED_EX,
        "reset": __colorama.Fore.RESET
    }



# Main group
##############################################################
@__click.command()
def welcome():
    """Welcome message"""
    import os as __os
    try:
        user = __os.getlogin()
    except:
        import getpass
        user = getpass.getuser()
    welcome_msg = f"{__COLOR['green']}Welcome {__COLOR['red']}{user} {__COLOR['green']}to {__COLOR['blue']}absfuyu's cli"
    __click.echo(f"""
        {__COLOR['reset']}{'='*(len(welcome_msg)-20)}
        {welcome_msg}
        {__COLOR['reset']}{'='*(len(welcome_msg)-20)}
    """)


@__click.command()
@__click.argument("name")
def greet(name):
    """Greet"""
    __click.echo(f"{__COLOR['red']}Hello {name}")


@__click.command()
@__click.option(
    "--setting", "-s",
    type=__click.Choice(["luckgod"]),
    help="Toggle on/off selected setting")
def toggle(setting):
    """Toggle on/off setting"""
    if setting is "luckgod":
        __luck()
        out = __scfg("luckgod-mode")
        __click.echo(f"{__COLOR['red']}{out}")
    else:
        __click.echo(f"{__COLOR['red']}Invalid setting")
    pass


@__click.command()
def version():
    """Check current version"""
    __click.echo(f"{__COLOR['green']}absfuyu: {__v}")


@__click.command()
@__click.argument("force_update", type=bool, default=True)
def update(force_update: bool):
    """Update the package to latest version"""
    __click.echo(__COLOR['green'])
    __check_for_update(force_update=force_update)



# Do group
##############################################################
@__click.command(name="gen-pass")
@__click.argument("size", type=int, default=8)
@__click.option(
    "--password_type", "-p",
    type=__click.Choice(["default","full"]),
    default="full",
    help="default: [a-zA-Z0-9] | full: [a-zA-Z0-9] + special char")
def gen_password(size, password_type):
    """Generate password of choice"""
    __click.echo(__randStr(
        size=size,
        char=password_type,
        string_type_if_1=True))


@__click.command()
@__click.argument("force_update", type=bool, default=True)
def update(force_update: bool):
    """Update the package to latest version"""
    __click.echo(__COLOR['green'])
    __check_for_update(force_update=force_update)


@__click.command()
def reset():
    """Reset config to default value"""
    __reset()
    __click.echo(f"{__COLOR['green']}All settings have been reseted")
    pass



@__click.group(name="do")
def do_group():
    """Perform functinalities"""
    pass
do_group.add_command(gen_password)
do_group.add_command(reset)
do_group.add_command(update)



# Main group init
##############################################################
@__click.group()
def main():
    """absfuyu's command line interface"""
    pass
main.add_command(welcome)
main.add_command(greet)
main.add_command(toggle)
main.add_command(version)
main.add_command(do_group)


if __name__ == "__main__":
    if CLI_MODE:
        main()