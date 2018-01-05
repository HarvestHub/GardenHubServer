"""gardenhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from gardenhub import views
from django.contrib import admin


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    # Account
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/settings/', views.account_settings_view, name='account-settings'),  # noqa
    path('account/delete/', views.DeleteAccountView.as_view(), name='account-delete'),  # noqa
    path('activate/<uuid:token>/', views.account_activate_view, name='account-activate'),  # noqa
    # Orders
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/new/', views.OrderCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),  # noqa
    path('pick/<int:plotId>/', views.pick_create_view, name='pick-create'),
    # Plots
    path('plots/', views.PlotListView.as_view(), name='plot-list'),
    path('plot/<int:pk>/edit/', views.plot_update_view, name='plot-update'),
    # Gardens
    path('gardens/', views.GardenListView.as_view(), name='garden-list'),
    path('garden/<int:pk>/', views.GardenDetailView.as_view(), name='garden-detail'),  # noqa
    path('garden/<int:pk>/edit/', views.garden_update_view, name='garden-update'),  # noqa
    # API
    path('_api/crops/<int:pk>/', views.api_crops),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
