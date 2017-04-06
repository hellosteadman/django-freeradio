from .models import Notice


def noticeboard(request):
    return {
        'noticeboard': Notice.objects.all()
    }
