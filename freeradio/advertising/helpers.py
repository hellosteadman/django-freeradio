from ..core.helpers import unique_id
from os import path


def upload_advert_image(instance, filename):
    return 'bcwfujtfnfou/%s%s' % (
        unique_id(),
        path.splitext(filename)[-1]
    )
