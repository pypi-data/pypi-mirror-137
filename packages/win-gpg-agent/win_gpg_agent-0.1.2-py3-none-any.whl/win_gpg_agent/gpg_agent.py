from typing import NoReturn, Tuple, Union

import psutil

from win_gpg_agent.config import WIN_GPG_AGENT_DIR, WSL_GPG_USER_HOME
from win_gpg_agent.util import (fail, print_styled, run_cmd_sync,
                                run_wsl_socket_relay, warn)
from win_gpg_agent.windows_component import ensure_windows_component_is_running


def is_wsl_native_gpg_agent_running() -> bool:
    """Checks if the `gpg-agent` process is running in WSL."""
    running_processes = psutil.process_iter()
    return any(p.name() == "gpg-agent" for p in running_processes)


def get_running_tunnel_pid() -> Union[int, None]:
    for proc in psutil.process_iter():
        args = " ".join(proc.cmdline())
        if (
            proc.name() == "socat"
            and "S.gpg-agent" in args
            and "S.gpg-agent.ssh" not in args
        ):
            return proc.pid
    return None


def gpg_connect_agent(*cmds: Tuple[str]) -> None:
    run_cmd_sync("gpg-connect-agent", *cmds, "/bye")


async def run_gpg_agent_tunnel(
    listen_sock_path: str = f"{WSL_GPG_USER_HOME}/S.gpg-agent",
) -> NoReturn:
    print_styled(
        ("gpg-agent tunnel", "cyan"),
        ("listening at socket", "green"),
        (listen_sock_path, "magenta"),
    )
    await run_wsl_socket_relay(
        unix_sock_path=listen_sock_path,
        win_sock_path=f"{WIN_GPG_AGENT_DIR}/gnupg/S.gpg-agent",
    )


def does_socket_file_exist() -> bool:
    return (WSL_GPG_USER_HOME / "S.gpg-agent").exists()


async def run() -> NoReturn:
    ensure_windows_component_is_running()

    gpg_agent_tunnel_pid = get_running_tunnel_pid()
    if gpg_agent_tunnel_pid is not None:
        fail(f"gpg-agent-tunnel already running (PID: {gpg_agent_tunnel_pid})")

    if is_wsl_native_gpg_agent_running():
        warn("Native gpg-agent running in WSL detected, closing...")
        gpg_connect_agent("killagent")
        if is_wsl_native_gpg_agent_running():
            fail("Could not kill native gpg-agent")

    if does_socket_file_exist():
        print_styled(
            ("Orphaned socket file at", "yellow"),
            (WSL_GPG_USER_HOME / "S.gpg-agent", "magenta"),
            ("detected", "yellow"),
        )
        warn("Clearing via the native gpg-agent...")
        gpg_connect_agent("reloadagent")
        gpg_connect_agent("killagent")
        if does_socket_file_exist():
            fail("That didn't work")

    await run_gpg_agent_tunnel()
