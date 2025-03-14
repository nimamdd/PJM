"""
URL configuration for ProjectManagerRest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Project Manager with DRF",
        default_version="v0.0.1-beta",
        description="this is a api version of projectmanager.com website",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email='arsham.python@gmail.com'),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated]
)

admin.site.site_header = 'Project Manager Rest Amoot header'
admin.site.site_title = 'Project Manager Rest Amoot title'
admin.site.index_title = 'Welcome Managers'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('Accounts.urls')),
    path('projects/', include('Projects.urls')),
    path('financial/', include('Financial.urls')),
   # path('__debug__/', include(debug_toolbar.urls)),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.PRODUCTION is False:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'), name='rest_auth'),
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')

    ]
