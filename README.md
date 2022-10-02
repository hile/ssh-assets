![Unit Tests](https://github.com/hile/ssh-assets/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/ssh-assets/actions/workflows/lint.yml/badge.svg)

# SSH assets python library

This little utility allows configuring SSH keys to be loaded automatically to
the SSH agent based on asset configuration files, and can detect loaded keys
based on the key hash to avoid reloading existing keys.

This library can:

- load SSH key details from various key formats to get key hashes, comments and other key details
- detect keys loaded to the SSH agent by key hash instead of filename
- define known SSH keys from multiple locations (project specific folders, shared team folders) with
  options to name and autoload the key with the module
- load and unload keys to the agent based on custom configuration file, without asking key password
  if the key was already loaded

# Installing

This tool can be installed from PyPI.

```bash
pip install ssh-assets
```

## Using the CLI tool

This package installs command line utility `ssh-assets`. The tool currently has
only one command `load-keys` that can be used to load the keys configured in
the assets configuration file as shown below.

Following command loads any keys not yet loaded to the agent, but limits this
to the keys with `autoload` property set to `true`:

```bash
ssh-assets keys load
ssh-assets keys load --group personal
ssh-assets keys edit personal --no-autoload
ssh-assets keys edit personal --autoload
```

## SSH assets configuration file

This module uses configuration file `~/.ssh/assets.yml` to define paths to the
SSH keys.

Example configuration file:

```yaml
---
groups:
  - name: personal
    expire: 5d
    keys:
      - personal
      - missing-demo-key
  - name: work
    expire: 1d
    keys:
      - aws
      - master
      - myproject
keys:
  - name: personal
    path: ~/.ssh/id_rsa
    autoload: true
  - name: aws
    path: ~/.ssh/id_rsa-aws
  - name: myproject
    path: ~/Work/Keys/ssh_project_id
    autoload: true
  - name: master
    expire: 1d
    path: ~/Work/Keys/master_ssh_key
```

- `autoload` defaults to False in configuration if not specified.
- `expore` defines a valid value for key expiration in SSH agent, for example `8h` or `5d`

## Example python code

With such configuration file, you can load the keys marked as `autoload` to the SSH
agent with following example code. Calling the load method again does not try loading
the keys again (key is detected in agent loaded keys by hash).

```python
from ssh_assets.session import SshAssetSession
SshAssetSession().load_pending_keys()
```

## History

This module replaces previous module `systematic-ssh-config` when ready.
