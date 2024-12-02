from django.urls import path
from .views import markets_view, market_single_view, sellers_view, products_view, seller_single_view, product_single_view

urlpatterns = [
    path('market/', markets_view),
    path('market/<int:pk>/', market_single_view, name='market-detail'),      # pk (primary key = id aus Datenbank) wird übergeben! name verweist auf den HyperlinkedModelSerializer in der serializers.py
    path('seller/', sellers_view),
    path('seller/<int:pk>/', seller_single_view, name='seller_single'),     # name verweist auf den view_name des HyperlinkedRelatedField in der serializers.py
    path('product/', products_view),
    path('product/<int:pk>/', product_single_view, name='product-detail')
]