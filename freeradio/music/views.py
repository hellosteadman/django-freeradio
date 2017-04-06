from django.views.generic.list import ListView
from .models import Playlist
from ..core.mixins import BootstrapMixin


class PlaylistView(BootstrapMixin, ListView):
    model = Playlist
    body_classes = ('music', 'playlist')
    menu_selection = 'music:playlist'

    def get_title_parts(self):
        for obj in self.object_list:
            yield obj.name
            break
