from django.conf.urls import url
from django.contrib import admin

# from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/books', views.BookList.as_view()),
    url(r'^api/external-books', views.ExternalAPI.as_view()),
]
