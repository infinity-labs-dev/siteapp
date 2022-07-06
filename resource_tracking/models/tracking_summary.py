from .site_tracking import SiteTracking
class TrackingSummary(SiteTracking):
    class Meta:
        proxy = True
        verbose_name = 'Tracking Summary'
        verbose_name_plural = 'Tracking Summary'