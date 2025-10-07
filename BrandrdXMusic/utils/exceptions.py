class AssistantError(Exception):
    """Custom exception class for assistant-related errors."""

    def __init__(self, error: str):
        self.error = error
        super().__init__(error)

    def __str__(self):
        return f"AssistantError: {self.error}"
