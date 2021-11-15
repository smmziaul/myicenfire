from django.conf.urls import url
from django.urls import path
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views

from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/books', views.BookList.as_view()),
    url(r'^api/external-books', views.ExternalAPI.as_view()),

    # added while deployment
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
