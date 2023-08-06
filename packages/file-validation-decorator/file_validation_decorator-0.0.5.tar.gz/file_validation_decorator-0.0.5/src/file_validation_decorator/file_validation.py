import pathlib


class FileTypeNotAllowed(Exception):
    def __init__(self, file_type, accepted_file_extensions):
        self.message = f"The file type of {file_type} is not found in the provided acceptable file extension list of {accepted_file_extensions}."
        super().__init__()

    def __str__(self):
        return self.message


class FileSizeExceeded(Exception):
    def __init__(self, max_file_size, file_size):
        self.message = f"This file is {file_size:0.2f}MB is larger than the allowed size of {max_file_size}MB"
        super().__init__()

    def __str__(self):
        return self.message


def file_validation(file, accepted_file_extensions: list, max_file_size: int):
    """
    Decorator for validating in memory file types, and sizes.
    :param file: in memory file object.
    :param accepted_file_extensions: a list of allowable file extensions (i.e. ['jpg', 'jpeg', 'wav', 'mp4']).
    :param max_file_size: maximum size of the file in Megabytes you will accept.
    :return: The function you are decorating.
    :exception FileTypeNotAllowed: Raised if the file extension is not found in the accepted_file_extensions parameter.
    :exception FileSizeExceeded: Raised when the file size exceeds the max_file_size parameter.
    """
    accepted_file_extensions = [x for x in accepted_file_extensions if x]
    file_size = file.seek(0, 2)/1048576
    file_extension = pathlib.Path(file.name).suffix

    def decorator(function):
        def wrapper(*args, **kwargs):
            if not file.name.upper().endswith(tuple(x.upper() for x in accepted_file_extensions)):
                raise FileTypeNotAllowed(file_extension, accepted_file_extensions)
            if file_size > max_file_size:
                raise FileSizeExceeded(max_file_size, file_size)

            return function(*args, **kwargs)
        return wrapper
    return decorator
