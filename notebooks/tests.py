from more_itertools import ilen
from mock import patch
from . import views


class TestNotebooksListView:
    
    def test_view_200(self, rf, admin_user):
        request = rf.get('/notebooks')
        request.user = admin_user
        response = views.notebooks_list(request)
        assert response.status_code == 200

    @patch('notebooks.views.render')
    def test_passes_list_of_paths_to_context(self, mock_render, rf, admin_user):
        request = rf.get('/notebooks')
        request.user = admin_user
        views.notebooks_list(request)
        assert mock_render.called
        file_paths = mock_render.call_args[1]['context']['file_paths']
        assert ilen(file_paths) > 0

class TestNotebookToHtmlView:

    def test_view_200(self, rf, admin_user):
        request = rf.get('/notebooks/test_input.ipynb')
        request.user = admin_user
        view = views.notebook2html
        response = view(request, file_name='test_input.ipynb')
        assert response.status_code == 200

    @patch('notebooks.views.render')
    def test_notebook_html_to_context(self, mock_render, rf, admin_user):
        request = rf.get('/notebooks/test_input.ipynb')
        request.user = admin_user
        view = views.notebook2html
        response = view(request, file_name='test_input.ipynb')
        assert mock_render.called
        assert '<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8" />\n<title>test_input' in mock_render.call_args[1]['context']['notebook_html']

    def test_view_only_accepts_notebook_files(self, rf, admin_user):
        request = rf.get('/notebooks/test_input.css')
        request.user = admin_user
        view = views.notebook2html
        response = view(request, file_name='test_input.css')
        assert response.status_code == 403