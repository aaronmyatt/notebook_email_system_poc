import glob
import os
import functools
from django.conf import settings

def notebook_paths(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        notebook_path = os.path.join(settings.BASE_DIR, 'notebooks/input/*')
        file_paths = glob.glob(notebook_path)
        kwargs.update(dict(file_paths=file_paths))
        return f(request, *args, **kwargs)
    return wrapper