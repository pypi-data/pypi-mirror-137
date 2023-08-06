import pathlib
import magic


class FileExtensionNotAllowed(Exception):
    def __init__(self, file_extension, accepted_list):
        self.message = f"The file extension of {file_extension} is not found in the provided acceptable file extension list of {accepted_list}."
        super().__init__()

    def __str__(self):
        return self.message


class FileTypeNotAllowed(Exception):
    def __init__(self, file_type, accepted_file_extensions):
        self.message = f"The file type of {file_type} is not found in the provided acceptable file extension list of {accepted_file_extensions}."
        super().__init__()

    def __str__(self):
        return self.message


class FileMimeTypeNotAllowed(Exception):
    def __init__(self, mime_type, accepted_mime_types):
        self.message = f"The mime type of {mime_type} is not found in the provided acceptable mime type list of {accepted_mime_types}."
        super().__init__()

    def __str__(self):
        return self.message


class FileSizeExceeded(Exception):
    def __init__(self, max_file_size, file_size):
        self.message = f"This file is {file_size:0.2f}MB is larger than the allowed size of {max_file_size}MB"
        super().__init__()

    def __str__(self):
        return self.message


def file_magic(file):
    file.seek(0)
    file_type = magic.from_buffer(file.read())
    file.seek(0)
    mime_type = magic.from_buffer(file.read(), mime=True)
    file.seek(0)
    return file_type, mime_type


def file_validation(
    accepted_file_extensions: list = None,
    accepted_file_types: list = None,
    accepted_mime_types: list = None,
    max_file_size: float or int = None
):
    """
    Decorator for validating in memory file types, and sizes.
    :param accepted_mime_types: a list of allowable mime types (i.e. ['text/plain'])
    :param accepted_file_types: a list of allowable file types (i.e. ['ASCII text, with no line terminators'])
    :param accepted_file_extensions: a list of allowable file extensions (i.e. ['jpg', 'jpeg', 'wav', 'mp4']).
    :param max_file_size: maximum size of the file in Megabytes you will accept.
    :return: The function you are decorating.
    :exception FileExtensionNotAllowed: Raised when the file's extension is not found in the list of accepted_file_extensions.
    :exception FileTypeNotAllowed: Raised when the file's type is not found in the list of accepted_file_types.
    :exception FileMimeTypeNotAllowed: Raised when the file's mime type is not found in the list of accepted_mime_types.
    :exception FileSizeExceeded: Raised when the file's size is larger than the max_file_size.
    """
    accepted_file_extensions = [x for x in accepted_file_extensions if x]  # removes emtpy strings

    def _method_wrapper(function):
        def _arguments_wrapper(file, *args, **kwargs):
            try:
                file_size = file.seek(0, 2) / 1048576
                file_extension = pathlib.Path(file.name).suffix
                file_type, mime_type = file_magic(file)

                if accepted_file_extensions and not file.name.upper().endswith(
                    tuple(x.upper() for x in accepted_file_extensions)
                ):
                    raise FileTypeNotAllowed(f'"{file_extension}"', accepted_file_extensions)

                if max_file_size <= 0:
                    raise ValueError("Max file size must be a positive float or integer.")

                if 0 < max_file_size < file_size:
                    raise FileSizeExceeded(f'"{max_file_size}"', file_size)

                if accepted_mime_types and mime_type not in accepted_mime_types:
                    raise FileMimeTypeNotAllowed(f'"{mime_type}"', accepted_mime_types)

                if accepted_file_types and file_type not in accepted_file_types:
                    raise FileTypeNotAllowed(f'"{file_type}"', accepted_file_types)

                return function(file, *args, **kwargs)

            except AttributeError:
                raise AttributeError('The first parameter defined in your function must be a in memory file object.')

        return _arguments_wrapper

    return _method_wrapper
