"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from config import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('accounts/', include('apps.accounts.urls')),
    path('authors/', include('apps.author.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('books/', include('apps.book.urls')),
    path('loans/', include('apps.loan.urls')),
    path('reservations/', include('apps.reservation.urls')),
    path('reviews/', include('apps.review.urls')),
]
handler404 = "apps.author.views.page_non_trouvee"
handler403 = "apps.author.views.page_non_trouvee"
handler500 = "apps.author.views.erreur_serveur"

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)