""" MimeTypes module.

Usage: look for 'mimetypes' documentation in python standard library.
"""
import mimetypes as _mimetypes
import os


_ADDITIONAL_MIME_TYPES = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "_resources",
    "additional.mime.types",
)


def reload_mimetypes():
    """ Force reload mimetype to append custom ones.
    """
    _mimetypes.init(files=[_ADDITIONAL_MIME_TYPES])


reload_mimetypes()
mimetypes = _mimetypes
