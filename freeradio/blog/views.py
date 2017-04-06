from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Post
from ..core.mixins import BootstrapMixin


class PostsView(BootstrapMixin, ListView):
    model = Post
    paginate_by = 10
    body_classes = ('blog', 'posts')
    menu_selection = 'blog:posts'

    def get_title_parts(self):
        yield 'Blog'


class PostView(BootstrapMixin, DetailView):
    model = Post
    body_classes = ('blog', 'post')
    menu_selection = 'blog:post'

    def get_title_parts(self):
        yield self.object.title
        yield 'Blog'

    def get_social_image(self):
        return self.object.featured_image

    def get_social_description(self):
        return self.object.excerpt
