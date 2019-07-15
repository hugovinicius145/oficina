
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('oficina.urls')),
    path('account/', include('django.contrib.auth.urls')),
    #url(r'^$',views.singIn),
    #url(r'^postsign/',views.postsign)
]
