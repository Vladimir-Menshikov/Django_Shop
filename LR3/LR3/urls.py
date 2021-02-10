from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.views import e_handler404

handler404 = e_handler404

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    url(r'^orders/', include(('orders.urls', 'orders'), namespace='orders')),
    url(r'^account/', include('account.urls')),
    url(r'^', include(('app.urls', 'app'), namespace='app')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)