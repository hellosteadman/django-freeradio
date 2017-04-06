from django import forms
from django.utils import timezone
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.fields['published'].initial = timezone.localtime(
            timezone.now()
        )

    class Meta:
        model = Post
        fields = (
            'title',
            'slug',
            'body',
            'excerpt',
            'author',
            'blogger',
            'published',
            'featured_image',
            'categories',
            'tags'
        )
