""" MimeTypes module.

Usage: look for 'mimetypes' documentation in python standard library.
The rdo_resourcefile_core project overrides it so more mime-types can be registered. This
will ensure rdo_resourcefile_core can identify mime-types which are not centrally set up.
"""

from __future__ import absolute_import

import mimetypes as _mimetypes
import os


_ADDITIONAL_MIME_TYPES = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "_resources", "additional.mime.types",
)


def reload_mimetypes():
    """ Force reload mimetype to append custom ones.
    """
    _mimetypes.init(files=[_ADDITIONAL_MIME_TYPES])

    # Additional encodings.
    _mimetypes.encodings_map[".sc"] = "blosc"  # http://blosc.org/pages/blosc-in-depth/


reload_mimetypes()
mimetypes = _mimetypes
