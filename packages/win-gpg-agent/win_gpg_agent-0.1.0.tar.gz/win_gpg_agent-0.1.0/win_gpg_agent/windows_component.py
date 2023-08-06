from win_gpg_agent.config import (WIN_GPG_AGENT_DIR,
                                  WSL_MOUNTED_WIN_GPG_AGENT_DIR)
from win_gpg_agent.util import fail


def is_windows_component_running() -> bool:
    """Checks if the win-gpg-agent directory contains any running sockets."""
    socket_dir = WSL_MOUNTED_WIN_GPG_AGENT_DIR / "gnupg"
    open_socket_files = list(socket_dir.iterdir())
    return len(open_socket_files) > 0


def ensure_windows_component_is_running():
    if not is_windows_component_running():
        fail(
            "Socket files on Windows filesystem at",
            f"  Windows   {WIN_GPG_AGENT_DIR}",
            f"  WSL       {WSL_MOUNTED_WIN_GPG_AGENT_DIR}",
            "could not be located.",
            "",
            "Please make sure win-gpg-agent is running in the Windows tray.",
        )
