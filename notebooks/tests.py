from mock import patch
from . import views


class TestNotebooksListView:
    
    def test_view_200(self, rf):
        request = rf.get('/notebooks')
        view = views.notebooks_list
        response = view(request)
        assert response.status_code == 200

    @patch('notebooks.views.render')
    def test_passes_list_of_paths_to_context(self, mock_render, rf):
        request = rf.get('/notebooks')
        view = views.notebooks_list
        response = view(request)
        assert mock_render.called
        assert len(mock_render.call_args[1]['context']['file_paths']) > 0

class TestNotebookToHtmlView:

    def test_view_200(self, rf):
        request = rf.get('/notebooks/test_input.ipynb')
        view = views.notebook2html
        response = view(request, 'test_input.ipynb')
        assert response.status_code == 200

    @patch('notebooks.views.render')
    def test_notebook_html_to_context(self, mock_render, rf):
        request = rf.get('/notebooks/test_input.ipynb')
        view = views.notebook2html
        response = view(request, file_name='test_input.ipynb')
        assert mock_render.called
        assert '<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8" />\n<title>test_input' in mock_render.call_args[1]['context']['notebook_html']