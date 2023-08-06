from pathlib import Path

HERE = Path(".").resolve()

WSL_GPG_USER_HOME = Path("~/.gnupg").expanduser()
WSL_MOUNTED_WIN_GPG_AGENT_DIR = Path("/mnt/c/win-gpg-agent")
WIN_GPG_AGENT_DIR = Path("C:/win-gpg-agent")
SOCKET_DIR = "gnupg"
