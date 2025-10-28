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
@click.argument("search_keywords", type=str, nargs=-1)
@click_common_opts(__version__)
def list(ctx, search_keywords, debug):
    """List devices."""
    __log = get_logger(__name__, debug)
    __log.debug("cmd_name=%s", ctx.command.name)
    __log.debug("search_keywords=%s", search_keywords)

    app = None
    try:
        app = CmdList(search_keywords, debug=debug)
        app.main()

    except Exception as _e:
        __log.error(errmsg(_e))

    finally:
        if app:
            app.end()


@cli.command()
@click.argument("search_keywords", type=str, nargs=-1)
@click.option(
    "--repeat",
    "-r",
    is_flag=True,
    default=False,
    show_default=True,
    help="show repeat",
)
@click_common_opts(__version__)
def input(ctx, search_keywords, repeat, debug):
    """input test."""
    __log = get_logger(__name__, debug)
    __log.debug("cmd_name=%s", ctx.command.name)
    __log.debug("search_keywords=%s, repeat=%s", search_keywords, repeat)

    if not search_keywords:
        __log.error("no search_keywords")
        return

    app = None
    try:
        app = CmdInput(search_keywords, repeat, debug=debug)
        app.main()

    except Exception as _e:
        __log.error(errmsg(_e))

    finally:
        if app:
            app.end()
