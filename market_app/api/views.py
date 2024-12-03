from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import MarketSerializer, SellerSerializer, MarketHyperlinkedSerializer, ProductSerializer, ProductHyperlinkedSerializer, ProductCreateSerializer, SellerListSerializer
from market_app.models import Market, Seller, Product

from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets


class MarketsView(generics.ListAPIView):  # beinhaltet nur die GET-Methode!
    queryset = Market.objects.all()     # Abfrage-Grundlage (angezeigte Daten)
    serializer_class = MarketSerializer     # verbundene Serializer (von serializers.py)


class MarketSingleView(generics.RetrieveUpdateDestroyAPIView):       # beinhaltet die GET-, PUT-, PATCH- und DELETE-Methode!
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class SellerOfMarketList(generics.ListCreateAPIView):     # zeigt alle Seller eines Market-Objektes in einer Liste an!
    serializer_class = SellerListSerializer

    def get_queryset(self):       # Funktion zum Anpassen des "queryset"
        pk = self.kwargs.get('pk')  # holt sich die pk aus der URL
        market = Market.objects.get(pk=pk)  # holt sich das entsprechende Market-Objekt mit der pk
        return market.sellers.all() # gibt alle Seller des Market-Objektes zurück
    
    def perform_create(self, serializer):   # Funktion zum Erstellen eines Sellers, der mit dem referenzierten Market-Objekt verbunden ist! 
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk=pk)
        serializer.save(markets=[market])   # das Seller-Feld "markets" wird überschrieben und es wird eine neue Liste mit nur einem Market-Objekt übergeben! (somit sind die erstellen Seller mit nur einem Market verbunden!)


# class MarketsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):     # ersetzt komplett die Function-based View "markets_view"
#     queryset = Market.objects.all()
#     serializer_class = MarketSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


@api_view(['GET', 'POST']) # Decorator (Wrapper-function) gibt der Funktion die Http-Methoden mit (default ist GET)
def markets_view(request):
    
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketHyperlinkedSerializer(markets, many=True, context={'request': request}, fields=('id', 'name'))   # many=True bedeutet es wird eine Liste von Objekten übergeben! context muss definiert werden, da dieser Serializer ein HyperlinkedRelatedField verwendet!
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data)    # die Daten aus unserem Request werden übergeben
        if serializer.is_valid():                           # es wird geprüft ob die Daten valide sind
            serializer.save()                               # die Daten werden in die Datenbank gespeichert und es wird "create()" aufgerufen (aus "serializers.py")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # try:      # alte POST-Methode
        #     msg = request.data['message']               # holt sich aus dem Request (Anfrage) den Wert aus dem Dictionary mit dem Key 'message'
        #     return Response({'your_message': msg}, status=status.HTTP_201_CREATED)
        # except:
        #     return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class MarketDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):                # single view (Anzeige eines einzelnen Market-Objekts)

    if request.method == 'GET':
        market = Market.objects.get(pk=pk)          # der pk aus der URL wird übergeben und damit das entsprechende Market-Objekt geholt!
        serializer = MarketSerializer(market, context={'request': request})       # das einzelne Market-Objekt (Instanz) wird dem Serializer übergeben! (kein many=True mehr!)
        return Response(serializer.data)

    if request.method == 'PUT':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, data=request.data, partial=True)    # es wird das entsprechende Market-Objekt (Instanz) und die Daten aus dem Request übergeben (partial: es können auch nur einzelne Attribute verändert werden)
        if serializer.is_valid():
            serializer.save()                       # die Daten werden in die Datenbank gespeichert und es wird "update()" aufgerufen (aus "serializers.py")
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        market.delete()
        return Response(serializer.data)


# für sellers:
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellersView(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellersViewOld(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):     # ersetzt komplett die Function-based View "sellers_view"
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def get(self, request, *args, **kwargs):    # von ListModelMixin
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):   # von CreateModelMixin
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def sellers_view(request):

    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        # serializer = SellerDetailSerializer(sellers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        # serializer = SellerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def seller_single_view(request, pk):

    if request.method == 'GET':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

    if request.method == 'PUT':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        seller = Seller.objects.get(pk=pk)
        serializer = SellerSerializer(seller)
        seller.delete()
        return Response(serializer.data)


# für products:
class ProductViewSet(viewsets.ModelViewSet):    # ersetzt komplett das einfache ViewSet (inkl. PUT/PATCH)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductViewSetOld(viewsets.ViewSet):     # ersetzt die Function-based products_view und product_single_view (außer PUT/PATCH)
    queryset = Product.objects.all()
    
    def list(self, request):    # zur Anzeige von allen Objekten/ Instanzen
        serializer = ProductSerializer(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):   # zur Anzeige eines einzelnen Objektes/ Instanz
        product = get_object_or_404(self.queryset, pk=pk)  # holt sich das Objekt zu dem entsprechenden pk
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):  # neues Objekt erstellen (POST)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, pk=None):    # Objekt entfernen (DELETE)
        product = get_object_or_404(self.queryset, pk=pk)  # holt sich das Objekt zu dem entsprechenden pk
        serializer = ProductSerializer(product, context={'request': request})
        product.delete()
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def products_view(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductHyperlinkedSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def product_single_view(request, pk):

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        product.delete()
        return Response(serializer.data)