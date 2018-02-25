from datetime import date
import io
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from notebooks.decorators import notebook_paths

@notebook_paths
def updater(users, file_paths=[]):
    file_path, *_ = [path for path in file_paths if 'user_updater' in path]
    users = execute_notebook(file_path, globe = locals().copy(), param='users')
    return users

def send_emails(users):
    # email handler logic goes here
    for user in users.all():
        user.emails.last_email = date.today()
        user.emails.save()

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