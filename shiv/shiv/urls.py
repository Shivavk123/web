from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import *

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('release/', request_view, name="delivery_request"),
                  path('cancel/', cancel_view, name="delivery_cancel"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
