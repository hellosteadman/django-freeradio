from .helpers import programme_on_air_now, programme_next_on_air


def traffic(request):
    next_programme, next_date = programme_next_on_air()
    
    return {
        'on_air_now': programme_on_air_now(),
        'on_air_next': {
            'programme': next_programme,
            'date': next_date
        }
    }
