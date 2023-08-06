#!/usr/bin/env python

import asyncio as aio
import signal
from typing import Union

import click
import psutil

from win_gpg_agent.config import HERE
from win_gpg_agent.util import coro, ok, print_styled, run_cmd_async

from . import gpg_agent, ssh_agent


def print_status_line(agent: str, pid: Union[int, None]) -> None:
    left = click.style(f"{agent} tunnel", fg="cyan")
    if pid is not None:
        right = click.style(f"RUNNING (pid: {pid})", fg="green")
    else:
        right = click.style("NOT RUNNING", fg="white")
    click.echo(f"   {left}      {right}")


def print_status() -> None:
    click.echo()
    click.secho("Status", fg="white")
    gpg_agent_pid = gpg_agent.get_running_tunnel_pid()
    print_status_line("gpg-agent", gpg_agent_pid)
    ssh_agent_pid = ssh_agent.get_running_tunnel_pid()
    print_status_line("ssh-agent", ssh_agent_pid)
    click.echo()


@click.group(help="Utility for tunnelling gpg-agent and ssh-agent from Windows to WSL.")
def cli():
    pass


@cli.command(help="Prints SSH_AUTH_SOCK export")
def export():
    click.echo(ssh_agent.make_export_snippet())


@cli.command(help="Prints status information about running tunnels")
def status():
    print_status()


@cli.command(help="Starts the daemon")
@click.option("--ssh/--no-ssh", default=True)
@click.option("--gpg/--no-gpg", default=True)
@coro
async def start(ssh: bool, gpg: bool):
    pid_file = HERE / "gpg-wsl-agent.pid"
    if not ssh and not gpg:
        return
    args = []
    if ssh:
        args.append("--ssh")
    if gpg:
        args.append("--gpg")
    await run_cmd_async(
        "start-stop-daemon",
        # "--verbose",
        "--pidfile",
        str(pid_file),
        "--make-pidfile",
        "--start",
        "--background",
        "--name",
        "gpg-wsl-agent",
        "--startas",
        __file__,
        "--",
        "run",
        *args,
        echo=True,
    )


@cli.command(help="Stops the daemon")
@coro
async def stop():
    pid_file = HERE / "gpg-wsl-agent.pid"
    await run_cmd_async(
        "start-stop-daemon",
        # "--verbose",
        "--pidfile",
        str(pid_file),
        "--remove-pidfile",
        "--stop",
        "--oknodo",
        echo=True,
    )
    await _kill_tunnels(ssh=True, gpg=True)


async def _kill_tunnels(ssh: bool, gpg: bool):
    ssh_pid = ssh_agent.get_running_tunnel_pid()
    gpg_pid = gpg_agent.get_running_tunnel_pid()

    if ssh_pid is None and gpg_pid is None:
        ok("ssh-agent tunnel and gpg-agent tunnel not running")
        return

    for proc in psutil.process_iter():
        if ssh and ssh_pid and proc.pid == ssh_pid:
            print_styled(
                ("Killing", "red"),
                ("ssh-agent tunnel", "cyan"),
                (f"(PID: {ssh_pid})", "red"),
            )
            proc.send_signal(signal.SIGTERM)
        if gpg and gpg_pid and proc.pid == gpg_pid:
            print_styled(
                ("Killing", "red"),
                ("gpg-agent tunnel", "cyan"),
                (f"(PID: {gpg_pid})", "red"),
            )
            proc.send_signal(signal.SIGTERM)


@cli.command(help="Kills active tunnels")
@click.option("--ssh/--no-ssh", default=True)
@click.option("--gpg/--no-gpg", default=True)
@coro
async def kill(ssh: bool, gpg: bool):
    return await _kill_tunnels(ssh, gpg)


@cli.command(help="Runs tunnel in the foreground")
@click.option("--ssh/--no-ssh", default=True)
@click.option("--gpg/--no-gpg", default=True)
@coro
async def run(ssh: bool, gpg: bool):
    tasks = []
    if ssh:
        tasks.append(aio.create_task(ssh_agent.run()))
    if gpg:
        tasks.append(aio.create_task(gpg_agent.run()))

    if len(tasks) == 0:
        print_status()

    await aio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    cli()
