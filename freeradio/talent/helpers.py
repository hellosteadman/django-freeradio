from os import path


def upload_presenter_photo(instance, filename):
    return 'presenters/%s%s' % (
        instance.slug,
        path.splitext(filename)[-1]
    )
