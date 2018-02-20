from nbconvert import HTMLExporter
from django.shortcuts import render
from .decorators import notebook_paths

@notebook_paths
def notebooks_list(request, file_paths=[]):
    return render(request,
                  template_name='notebook_list.html',
                  context=dict(file_paths=file_paths))

@notebook_paths
def notebook2html(request, file_name='', file_paths=[]):
    file_path, *_ = filter(lambda path: file_name in path, file_paths)
    exporter = HTMLExporter()
    html, meta = exporter.from_filename(file_path)
    return render(request, template_name='notebook2html.html', context=dict(notebook_html=html))