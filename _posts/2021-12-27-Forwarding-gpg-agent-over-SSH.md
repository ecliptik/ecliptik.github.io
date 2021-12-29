---
layout: post
title: Forwarding gpg-agent Over SSH
category: unix
tags: ssh linux unix gpg git
---

Basic notes from setting up [gpg-agent forwarding](https://wiki.gnupg.org/AgentForwarding) between a MacOS and Debian Linux system.

## Client System

Assuming system is running MacOS install [gpg](https://gnupg.org/) and pinentry (GPG password prompt tool) using [Homebrew](https://brew.sh/),

```shell
brew install gnupg pinentry-mac
```


Edit `~/.gnupg/gpg-agent.conf` and make sure that ${HOME} is the full path to your users home dir, eg `/Users/$USER`, this must match what's setup in the `~/.ssh/config` `RemoteForward` section later,

```
default-cache-ttl 600
max-cache-ttl 7200
enable-ssh-support
pinentry-program /usr/local/bin/pinentry-mac
extra-socket ${HOME}/.gnupg/S.gpg-agent.extra
```

`~/.gnupg/gpg.conf` (where `$GPG_KEY` is the fingerprint of the GPG key to use)

```
default-key $GPG_KEY
personal-digest-preferences SHA512
cert-digest-algo SHA512
default-preference-list SHA512 SHA384 SHA256 SHA224 AES256 AES192 AES CAST5 ZLIB BZIP2 ZIP Uncompressed
no-emit-version
```

Edit `~/.ssh/config` and setup a `RemoteForward`, this is important since the forward is required in order for the two gpg-agents to communicate over a socket. Make sure the `$UID` and `$USER` on the remote and local system are set accordingly, as these will differ depending on the OS and login.

Also double check the socket names, as sometimes they it can be something like `S.gpg-agent.extra` but other times `S.gpg-agent-extra`, note the differences with `.` and `-` and always double check as these are easy to miss and will cause agent forwarding to not work.

`~/.ssh/config`
```
Host $REMOTE_IP
   ForwardAgent yes
   Compression yes
   ForwardX11 yes
   RemoteForward /run/user/$UID/gnupg/S.gpg-agent /Users/${USER}/.gnupg/S.gpg-agent.extra
```

## Remote System

Update `/etc/ssh/sshd_config` (or wherever it is depending on your OS) configuration to include `StreamLocalBindUnlink yes` and restart `sshd`This option will,

>Specifies whether to remove an existing Unix-domain socket file for local or remote port forwarding before creating a new one.  If the socket file already exists and StreamLocalBindUnlink is not enabled, ssh will be unable to forward the port to the Unix-domain socket file. This option is only used for port forwarding to a Unix-domain socket file.


## Troubleshooting gpg-agent

Sometimes `StreamLocalBindUnlink yes` doesn't work and the client agent needs restarted and sockets removed from the remote system,

Restart the agent on the client system,

```
gpg-connect-agent reloadagent /bye
```

Remove the socket on the remote system,

```
rm /run/user/1000/gnupg/S.gpg-agent
```

ssh back into the remote system and gpg-agent forwarding should work again.

## References

- [Remote gpg-agent Via ssh Forwarding](https://web.archive.org/web/20190423113837/https://www.isi.edu/~calvin/gpgagent.htm)