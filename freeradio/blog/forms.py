from django import forms
from django.utils import timezone
from suit_redactor.widgets import RedactorWidget
from django_filepicker.widgets import FPFileWidget
from .models import Post


class BloggerForm(forms.ModelForm):
    class Meta:
        widgets = {
            'biography': RedactorWidget,
            'photo': FPFileWidget
        }


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

        widgets = {
            'body': RedactorWidget,
            'featured_image': FPFileWidget
        }
