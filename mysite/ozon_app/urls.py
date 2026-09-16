from rest_framework import routers
from .views import (ProfileViewsetListAPIView, CategoryListAPIViewset,
                    SubCategoryDefaultAPIViewset, ProductListAPIViewset,
                    ReviewViewset, ProfileViewsetDetailAPIView,
                    ProductDefaultAPIViewset, CategoryDefaultAPIViewset,
                    SubCategoryListAPIViewset, RegisterView,
                    CustomLoginView, LogoutView, CartAPIView,
                    CartItemViewSet, FavoriteItemViewSet, FavoriteAPIView)
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'review', ReviewViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', ProfileViewsetListAPIView.as_view()),
    path('user/<int:pk>/', ProfileViewsetDetailAPIView.as_view()),
    path('product/', ProductListAPIViewset.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDefaultAPIViewset.as_view(), name='product_default'),
    path('category/', CategoryListAPIViewset.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDefaultAPIViewset.as_view(), name='category_default'),
    path('subcategory/', SubCategoryListAPIViewset.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDefaultAPIViewset.as_view(), name='subcategory_default'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/', CartAPIView.as_view(), name='cart_detail'),
    path('cart_item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_item/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('favorite/', FavoriteAPIView.as_view(), name='favorite_detail'),
    path('favorite_item/', FavoriteItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('favorite_item/<int:pk>', FavoriteItemViewSet.as_view({'delete': 'destroy'})),

]