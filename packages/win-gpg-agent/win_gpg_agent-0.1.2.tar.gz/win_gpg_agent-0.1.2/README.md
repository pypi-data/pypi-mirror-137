# win-gpg-agent

Utility for tunnelling `gpg-agent` and `ssh-agent` from Windows to WSL.

Primarily used to enable the usage of Yubikeys on WSL.

## Installation
```
pip install win-gpg-agent
```

## Usage
```
# bash
win-gpg-agent export >> ~/.bashrc

# fish
echo "win-gpg-agent export | source" >> ~/.config/fish/config.fish
```

```
Usage: win-gpg-agent [OPTIONS] COMMAND [ARGS]...

  Utility for tunnelling gpg-agent and ssh-agent from Windows to WSL.

Options:
  --help  Show this message and exit.

Commands:
  export  Prints SSH_AUTH_SOCK export
  kill    Kills active tunnels
  run     Runs tunnel in the foreground
  start   Starts the daemon
  status  Prints status information about running tunnels
  stop    Stops the daemon
```
## Credit
This work is largely based around previous work from
- [@Nimamoh](https://github.com/Nimamoh)  
  [Blog post on WSL2+GPG+Yubikey](https://blog.nimamoh.net/yubi-key-gpg-wsl2-win-gpg-agent/) and [`win-gpg-agent-relay.sh` gist](https://gist.github.com/Nimamoh/e2df2ba0a99ef221d8cca360c931e5e6).
- [@rupor](https://github.com/rupor-github/win-gpg-agent)  
  The Windows component to this utility.