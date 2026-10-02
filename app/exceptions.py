class BotConfigurationError(RuntimeError):
    """Raised when required service configuration is missing or invalid."""


class XPostError(RuntimeError):
    """Raised when X rejects or does not confirm a posting operation."""

