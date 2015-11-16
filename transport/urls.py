from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'transport.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', 'main.views.home', name='home'),
	url(r'^book/$', 'main.views.staffBook', name='staffBook'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/$', 'main.views.contact', name='contact'),
    url(r'^about/$', 'main.views.about', name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
