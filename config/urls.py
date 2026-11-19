from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.accounts.views import RegisterView, ProfileView
from apps.catalog.views import CategoryViewSet, ProductViewSet
from apps.cart.views import CartView, CartItemViewSet
from apps.orders.views import OrderViewSet
router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("cart/items", CartItemViewSet, basename="cart-item")
router.register("orders", OrderViewSet, basename="order")
urlpatterns = [path("admin/", admin.site.urls), path("api/v1/auth/register/", RegisterView.as_view()), path("api/v1/auth/login/", TokenObtainPairView.as_view()), path("api/v1/auth/refresh/", TokenRefreshView.as_view()), path("api/v1/auth/profile/", ProfileView.as_view()), path("api/v1/cart/", CartView.as_view()), path("api/v1/", include(router.urls)), path("api/schema/", SpectacularAPIView.as_view(), name="schema"), path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"), path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc")]
