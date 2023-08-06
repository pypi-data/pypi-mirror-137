class _error(Exception):
    pass


class Location(_error):
    def __str__(self):
        return "such a file does not exist or an incorrect location is specified"


class Already(_error):
    def __str__(self):
        return "such a file already exists"


class Access(_error):
    def __str__(self):
        return "the system refused access"


class FileType(_error):
    def __str__(self):
        return "invalid file type"


class NoneMeta(_error):
    def __str__(self):
        return "metadata is missing or ignored"


class OutBlock(_error):
    def __str__(self):
        return "output blocked"