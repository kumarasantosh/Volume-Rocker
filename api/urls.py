from django.urls import include, path


urlpatterns = [
    path("nsedata/", include("api.nsedata.urls")),
    path("coidata/", include("api.coidata.urls")),
    path("volumerocker", include("api.VolumeRocker.urls"))
]
