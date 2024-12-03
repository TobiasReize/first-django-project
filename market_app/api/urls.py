from django.urls import path, include
from .views import markets_view, market_single_view, sellers_view, products_view, seller_single_view, product_single_view, \
    MarketsView, SellersView, MarketDetailView, MarketSingleView, SellerOfMarketList, ProductViewSet, SellerSingleView, SellerViewSet
from rest_framework import routers

# Bei zu vielen Routes sollte man es in eine extra Datei verschieben!
router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'sellers', SellerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketSingleView.as_view(), name='market-detail'),      # pk (primary key = id aus Datenbank) wird übergeben! name verweist auf den HyperlinkedModelSerializer in der serializers.py
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
    # path('seller/', SellersView.as_view()),
    # path('seller/<int:pk>/', SellerSingleView.as_view(), name='seller-detail'),     # name verweist auf den view_name des HyperlinkedRelatedField in der serializers.py
    # path('product/', products_view),
    # path('product/<int:pk>/', product_single_view, name='product-detail')
]