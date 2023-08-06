from django.urls import path

from sitelfl.views import recreated_urls

urlpatterns = [

    path('Recreated_urls/Fetch/', recreated_urls.Recreated_urls_Fetch),
    path('Recreated_urls/Add', recreated_urls.Recreated_urls_Add),
    path('Recreated_urls/Update', recreated_urls.Recreated_urls_Update),
    path('Recreated_urls/Remove', recreated_urls.Recreated_urls_Remove),
    path('Recreated_urls/Lookup/', recreated_urls.Recreated_urls_Lookup),
    path('Recreated_urls/Info/', recreated_urls.Recreated_urls_Info),
    path('Recreated_urls/Copy', recreated_urls.Recreated_urls_Copy),

]
