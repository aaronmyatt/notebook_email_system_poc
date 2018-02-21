import functools
from django.http import HttpResponseForbidden
from .utils import file_paths_in_project_dir

def notebook_paths(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        notebook_paths = file_paths_in_project_dir('notebooks/input/')
        kwargs.update(dict(file_paths=notebook_paths))
        return f(request, *args, **kwargs)
    return wrapper

def validate_file_type(check_string):
    def wrapper_wrapper(f):
        @functools.wraps(f)
        def wrapper(request, *args, **kwargs):
            if ('file_name' in kwargs
                    and check_string in kwargs.get('file_name', '')):
                return f(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        return wrapper
    return wrapper_wrapper