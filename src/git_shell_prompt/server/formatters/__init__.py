from git_shell_prompt.server.formatters.registry import Registry

from git_shell_prompt.server.formatters import (
    bash,
    json_,
)
Registry.set_default(json_.JSON)
Registry.register(json_.JSON)
Registry.register(bash.Bash)
