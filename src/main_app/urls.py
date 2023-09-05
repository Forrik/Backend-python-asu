from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
# from app_rest.views import RegistrationView, CustomTokenObtainView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    # path("api/token/", CustomTokenObtainView.as_view(), name="token_obtain"),
    # path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/register/", RegistrationView.as_view(), name="token_register"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
