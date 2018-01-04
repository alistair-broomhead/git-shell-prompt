Formatter = 'git_shell_prompt.server.formatters.base.Formatter'


class Registry:
    _formatters = {}
    _default = None

    @classmethod
    def get(cls, formatter: str) -> Formatter:
        return cls._formatters.get(formatter, cls._default)

    @classmethod
    def register(cls, formatter: Formatter):
        for spec in formatter.specs:
            existing = cls._formatters.get(spec)

            if existing is not None:
                raise KeyError(
                    f'{spec} defined for both {existing} and {formatter}'
                )
            else:
                cls._formatters[spec] = formatter

    @classmethod
    def set_default(cls, formatter: Formatter):
        cls._default = formatter
