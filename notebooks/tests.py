from mock import patch
from . import views


class TestNotebooksListView:
    
    def test_notebooks_view(self, rf):
        request = rf.get('/notebooks')
        view = views.notebooks_list
        response = view(request)
        assert response.status_code == 200

    @patch('notebooks.views.render')
    def test_view_passes_list_of_paths_to_context(self, mock_render, rf):
        request = rf.get('/notebooks')
        view = views.notebooks_list
        response = view(request)
        assert mock_render.called
        assert len(mock_render.call_args[1]['context']['file_paths']) > 0