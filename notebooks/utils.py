import os
import glob
from contextlib import contextmanager
from django.conf import settings
from nbconvert import HTMLExporter

def file_paths_in_project_dir(directory):
    path = os.path.join(settings.BASE_DIR, directory + '*')
    file_paths = glob.glob(path)
    return file_paths

@contextmanager
def notebook_html(notebook_path):
    exporter = HTMLExporter()
    html, meta = exporter.from_filename(notebook_path)
    yield html