from django.urls import path, include

urlpatterns = [
    path('logic/', include('sitelfl.urls.recreated_urls')),
]
