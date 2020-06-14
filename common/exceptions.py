class InstallationAutomationException(Exception):
    """
    This exception is returned when a export command is not successful.
    """

    def __init__(self, iam_error):
        self.message = iam_error

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message


class InstallationAutomationFileException(Exception):
    """
    This exception is returned when a the configuration is not properly formatted.
    """

    def __init__(self, iam_error):
        self.message = iam_error

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message
