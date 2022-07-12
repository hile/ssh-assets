# SSH assets python library

This little utility allows configuring SSH keys to be loaded automatically to
the SSH agent based on asset configuration files, and can detect loaded keys
based on the key hash to avoid reloading existing keys.

## SSH assets configuration file

This module uses configuration file `~/.ssh/assets.yml` to define paths to the
SSH keys.

Example configuration file:

```yaml
---
keys:
  - name: Demo
    path: ~/.ssh/id_rsa
    autoload: true
  - name: Project key
    path: ~/Work/Keys/ssh_project_id
    autoload: true
  - name: Master key
    path: ~/Work/Keys/master_ssh_key
```

Flag `autoload` defaults to False in configuration if not specified.

## History

This module replaces previous module `systematic-ssh-config` when ready.
