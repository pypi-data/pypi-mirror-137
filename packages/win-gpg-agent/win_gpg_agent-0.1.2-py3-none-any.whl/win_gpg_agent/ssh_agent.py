import os
from typing import NoReturn, Union

import psutil

from .config import WIN_GPG_AGENT_DIR, WSL_GPG_USER_HOME
from .util import fail, print_styled, run_wsl_socket_relay, warn
from .windows_component import ensure_windows_component_is_running


def is_wsl_native_ssh_agent_running() -> bool:
    """Checks if the `ssh-agent` process is running in WSL."""
    running_processes = psutil.process_iter()
    return any(p.name() == "ssh-agent" for p in running_processes)


def get_running_tunnel_pid() -> Union[int, None]:
    """Checks for a `socat` process that binds to a socket named S.gpg-agent.ssh."""
    for proc in psutil.process_iter():
        args = " ".join(proc.cmdline())
        if proc.name() == "socat" and "S.gpg-agent.ssh" in args:
            return proc.pid
    return None


def make_export_snippet() -> str:
    return f"export SSH_AUTH_SOCK={WSL_GPG_USER_HOME}/S.gpg-agent.ssh"


def does_socket_file_exist() -> bool:
    return (WSL_GPG_USER_HOME / "S.gpg-agent.ssh").exists()


async def run_ssh_agent_tunnel(
    listen_sock_path: str = f"{WSL_GPG_USER_HOME}/S.gpg-agent.ssh",
) -> NoReturn:
    print_styled(
        ("ssh-agent tunnel", "cyan"),
        ("listening at socket", "green"),
        (listen_sock_path, "magenta"),
    )
    if os.getenv("SSH_AUTH_SOCK", "") != listen_sock_path:
        print_styled(
            ("  Remember to set", "yellow"),
            ("SSH_AUTH_SOCK", "cyan"),
            ("to the output of", "yellow"),
            ("win-gpg-agent export", "cyan"),
        )
    await run_wsl_socket_relay(
        unix_sock_path=listen_sock_path,
        win_sock_path=f"{WIN_GPG_AGENT_DIR}/gnupg/S.gpg-agent.ssh",
    )


async def run() -> NoReturn:
    ensure_windows_component_is_running()

    tunnel_pid = get_running_tunnel_pid()
    if tunnel_pid is not None:
        fail(f"ssh-agent-tunnel already running (PID: {tunnel_pid})")

    if is_wsl_native_ssh_agent_running():
        warn("Native ssh-agent running in WSL detected, closing...")
        for proc in psutil.process_iter():
            if proc.name() == "ssh-agent":
                proc.kill()
        if is_wsl_native_ssh_agent_running():
            fail("Could not kill native ssh-agent")

    if does_socket_file_exist():
        print_styled(
            ("Orphaned socket file at", "red"),
            (WSL_GPG_USER_HOME / "S.gpg-agent.ssh", "magenta"),
            ("detected", "red"),
        )
        warn("Clearing...")
        (WSL_GPG_USER_HOME / "S.gpg-agent.ssh").unlink()

    await run_ssh_agent_tunnel()
