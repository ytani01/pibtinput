#
# (c) 2025 Yoichi Tanibayashi
#
"""__main__.py"""

import click

from . import __version__
from .cmd_input import CmdInput
from .cmd_list import CmdList
from .utils.clickutils import click_common_opts
from .utils.mylogger import errmsg, get_logger


@click.group()
@click_common_opts(__version__)
def cli(ctx, debug):
    """pi0servo CLI top."""
    cmd_name = ctx.info_name
    subcmd_name = ctx.invoked_subcommand

    ___log = get_logger(cmd_name, debug)

    ___log.debug("cmd_name=%s, subcmd_name=%s", cmd_name, subcmd_name)

    if subcmd_name is None:
        click.echo(ctx.get_help())


@cli.command()
@click_common_opts(__version__)
def list(ctx, debug):
    """List devices."""
    __log = get_logger(__name__, debug)
    __log.debug("cmd_name=%s", ctx.command.name)

    app = None
    try:
        app = CmdList(debug=debug)
        app.main()

    except Exception as _e:
        __log.error(errmsg(_e))

    finally:
        if app:
            app.end()


@cli.command()
@click.argument("dev_words", type=str, nargs=-1)
@click.option(
    "--repeat",
    "-r",
    is_flag=True,
    default=False,
    show_default=True,
    help="show repeat",
)
@click_common_opts(__version__)
def input(ctx, dev_words, repeat, debug):
    """input test."""
    __log = get_logger(__name__, debug)
    __log.debug("cmd_name=%s", ctx.command.name)
    __log.debug("dev_words=%s, repeat=%s", dev_words, repeat)

    if not dev_words:
        __log.error("no dev_words")
        return

    app = None
    try:
        app = CmdInput(dev_words, repeat, debug=debug)
        app.main()

    except Exception as _e:
        __log.error(errmsg(_e))

    finally:
        if app:
            app.end()
