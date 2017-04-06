def determine_duration_and_filesize(url, episode_id):
    from tempfile import mkstemp
    from mutagen.mp3 import MP3
    from .models import Episode
    import os
    import requests

    response = requests.get(url)
    filesize = response.headers['content-length']
    handle, filename = mkstemp()

    try:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                os.write(handle, chunk)

        os.close(handle)
        audio = MP3(filename)
        duration = audio.info.length
    finally:
        os.remove(filename)

    Episode.objects.filter(
        pk=episode_id
    ).update(
        filesize=filesize,
        duration=duration
    )
