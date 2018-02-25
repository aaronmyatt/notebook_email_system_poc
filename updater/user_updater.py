from datetime import date
import io
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from notebooks.decorators import notebook_paths

@notebook_paths
def updater(user_activity, file_paths=[]):
    file_path, *_ = [path for path in file_paths if 'user_updater' in path]
    user_update_count = execute_notebook(file_path, globe = locals().copy(), param='user_update_count')
    return user_update_count

def execute_notebook(path, globe, param='users'):
    nb = load_notebook(path)
    [exec(cell_transformer(cell.source), globe) for cell in nb.cells if cell.cell_type == 'code']
    return globe.get(param, None)

def load_notebook(path):
    file = io.open(path)
    return nbformat.read(file, 4)

def cell_transformer(cell):
    shell = InteractiveShell.instance()
    return shell.input_transformer_manager.transform_cell(cell)