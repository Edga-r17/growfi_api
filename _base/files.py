from urllib.parse import urlparse
import os
import requests
from django.core.files.base import ContentFile

from functools import wraps
from unipath import Path

import hashlib
import time


def upload_to_kwargs(fn, *args, **kwargs):
    extra_args = kwargs

    @wraps(fn)
    def proxy(*args, **kwargs):
        extra_args.update(kwargs)
        return fn(*args, **extra_args)
    return proxy


def generate_hashed_filename(filename, versioned=False):
    """
    Hashes `filename` to remove special chars reliably,
    make filename unique.
    """
    path = Path(filename)
    if versioned:
        # add UNIX timestamp to ensure uniqueness of filename
        filename += str(time.time())

    return "{stem}{ext}".format(
        stem=hashlib.md5(filename.encode('utf-8')).hexdigest(),
        ext=path.ext
    )


def upload_to_generic(instance, filename, subfolder=None):
    """
    Generic function to use on upload_to attribute of ImageField
    This will create a file path with the name of the class under MEDIA_ROOT
    and a hashed-version-name of the filename to ensure uniqueness
    """
    folder = instance.__class__.__name__.lower()

    if subfolder:
        folder = '{}/{}'.format(folder, subfolder)

    file_hash = generate_hashed_filename(filename, versioned=True)
    return '/'.join([folder, file_hash])


def save_image_from_row(instance, row):
    if row.get('photo'):
        if row['photo'] == instance.photo:
            image_content = ContentFile(requests.get(row['photo']).content)
            print('row***',row)
            url_image = urlparse(row['photo'])
            instance.photo.save(os.path.basename(url_image.path), image_content)
            instance.save()
