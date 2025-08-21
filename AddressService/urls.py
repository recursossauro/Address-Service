from django.contrib import admin
from django.urls import path
from address.views import home
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("postcard/", include(("postcard.urls", "postcard"), namespace="postcard")),
# path('tasks/', include(('tasks.urls','tasks'), namespace='tasks')),

]