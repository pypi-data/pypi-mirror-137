import asyncio as aio
import subprocess as sp
import sys
from functools import wraps
from pathlib import Path
from typing import NoReturn, Sequence, Tuple

import click

from .config import WSL_MOUNTED_WIN_GPG_AGENT_DIR


def fail(*msgs: Tuple[str], retcode: int = 1) -> NoReturn:
    if len(msgs) >= 1:
        msgs = ["ERROR: " + str(msgs[0]), *msgs[1:]]
    for msg in msgs:
        click.secho(msg, fg="red")
    sys.exit(retcode)


def print_styled(*parts: Tuple[str, str]) -> None:
    click.echo(" ".join((click.style(txt, fg=fg) for txt, fg in parts)))


def warn(*msgs: Tuple[str]) -> None:
    for msg in msgs:
        click.secho(msg, fg="yellow")


def ok(*msgs: Tuple[str]) -> None:
    for msg in msgs:
        click.secho(f"{msg}", fg="green")


async def run_wsl_socket_relay(
    unix_sock_path: Path,
    win_sock_path: Path,
    sorelay_exe_wsl_path: Path = f"{WSL_MOUNTED_WIN_GPG_AGENT_DIR}/sorelay.exe",
):
    listenArg = f"UNIX-LISTEN:{unix_sock_path},fork"
    socket_relay_win_cmd = f"{sorelay_exe_wsl_path} '{win_sock_path}'"

    execArg = f"EXEC:{socket_relay_win_cmd},nofork"
    await run_cmd_async("socat", listenArg, execArg)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = aio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


def run_cmd_sync(
    cmd: str, *args: Sequence[str], echo: bool = False, **run_kw
) -> sp.CompletedProcess:
    try:
        if echo:
            txt = "$ " + " ".join([cmd, *args])
            click.secho(txt, fg="cyan")
        return sp.run([cmd, *args], check=True, **run_kw)
    except Exception as err:
        fail(err)


async def run_cmd_async(
    cmd: str, *args: Sequence[str], echo: bool = False, **run_kw
) -> sp.CompletedProcess:
    try:
        if echo:
            txt = "$ " + " ".join([cmd, *args])
            click.secho(txt, fg="cyan")
        p = await aio.create_subprocess_exec(cmd, *args, **run_kw)
        retcode = await p.wait()
        if retcode != 0:
            raise RuntimeError(f"Command {cmd} exited with status code {retcode}")
    except Exception as err:
        fail(err)
