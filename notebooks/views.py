from django.shortcuts import render
from .decorators import notebook_paths

@notebook_paths
def notebooks_list(request, **kwargs):
    context = kwargs
    return render(request,
                  template_name='notebook_list.html',
                  context=context)