from django.conf.urls import include, url
from django.contrib import admin
from cms import views

urlpatterns = [
    url(r'^$', views.mainPage),
    url(r'^(\w+)/$', views.getPage),
    url(r'^admin/', include(admin.site.urls)),
]
