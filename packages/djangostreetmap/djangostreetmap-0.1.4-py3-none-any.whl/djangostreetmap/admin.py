from djangostreetmap import models
from django.contrib.gis import admin


@admin.register(models.SimplifiedLandPolygon)
class SimplifiedLandPolygonAdmin(admin.GeoModelAdmin):  # type: ignore
    pass
