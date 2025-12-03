# dashboard/context_processors.py
def site_settings(request):
    try:
        from .models import SiteSetting
        settings = SiteSetting.objects.first()
        return {'site_settings': settings}
    except:
        return {'site_settings': None}