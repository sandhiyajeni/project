from django.urls import path,include
from ecomapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('cart/',views.cart),
    path('contact/',views.contact),
    path('about/',views.about),
    path('login/',views.user_login),
    path('register/',views.register),
    path('logout/',views.user_logout),
    path('catfilter/<int:a>',views.cat_filter),
    path('sort/<str:a>',views.sort),
    path('range/',views.range),
    path('pdetails/<int:b>/',views.productsdetails),
    path('addtocart/<int:pid>/',views.addtocart),
    path('remove/<int:a>',views.remove),
    path('qty/<a>/<pid>',views.cartqty),
    path('place/',views.placeorder),
    path('mk/',views.makepayment)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
