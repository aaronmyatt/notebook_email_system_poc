import glob
import os
from django.conf import settings
from django.shortcuts import render

def all_notebooks(request):
    notebook_path = os.path.join(settings.BASE_DIR, 'notebooks/input/*')
    file_paths = glob.glob(notebook_path)
    return render(request, template_name='notebook_list.html', context=dict(file_paths=file_paths))