from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from customapp.views import GetPizzasToLogView, UserRequestView, LeaderboardView, BuyPizzaView, LogPizzaView, UserDetailView

schema_view = get_schema_view(
   openapi.Info(
      title="Pijja Khaa Lo API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@pijjakhaalo.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('api/user/', UserRequestView.as_view(), name='user_creation_view'),
   path('api/user/<str:user_id>', UserDetailView.as_view(), name='user_detail_view'),
   path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard_view'),
   path('api/pizza/buy/', BuyPizzaView.as_view(), name='buy_pizza_view'),
   path('api/pizza/log/', LogPizzaView.as_view(), name='buy_pizza_view'),
   path('api/pizza/log/get/', GetPizzasToLogView.as_view(), name='buy_pizza_view'),
]