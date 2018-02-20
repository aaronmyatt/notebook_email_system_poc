import functools
from .utils import file_paths_in_project_dir

def notebook_paths(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        notebook_paths = file_paths_in_project_dir('notebooks/input/')
        kwargs.update(dict(file_paths=notebook_paths))
        return f(request, *args, **kwargs)
    return wrapper