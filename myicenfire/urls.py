from django.conf.urls import url
from django.urls import path
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/books', views.BookList.as_view()),
    url(r'^api/external-books', views.ExternalAPI.as_view()),


    # url(r'api/v1/books/<int:book_id>', views.BookList.as_view()), # , name='book'),
    # path(r'api/v1/<int:id>', views.OneBook.as_view(), name='OneBook')

    # url(r'^api/v1/books/(P<pk>[0-9]+)$', views.BookList.as_view()),
    # path('api/v1/books/<int:id>', views.BookList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
