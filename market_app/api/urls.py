from django.urls import path
from .views import markets_view, market_single_view, sellers_view, products_view

urlpatterns = [
    path('market/', markets_view),
    path('market/<int:pk>/', market_single_view),      # pk (primary key = id aus Datenbank) wird übergeben
    path('seller/', sellers_view),
    path('product/', products_view),
]