import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import notebook_html
from .decorators import notebook_paths, validate_file_type

@login_required
@notebook_paths
def notebooks_list(request, file_paths=[]):
    file_names = map(os.path.basename, file_paths)
    return render(request,
                  template_name='notebook_list.html',
                  context=dict(file_paths=file_names))

@login_required
@validate_file_type('.ipynb')
@notebook_paths
def notebook2html(request, file_name='', file_paths=[]):
    file_path, *_ = filter(lambda path: file_name in path, file_paths)
    with notebook_html(file_path) as html_output:
        return render(request, template_name='notebook2html.html', context=dict(notebook_html=html_output))