from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer, ProductDetailSerializer, ProductCreateSerializer
from market_app.models import Market, Seller, Product


@api_view(['GET', 'POST']) # Decorator (Wrapper-function) gibt der Funktion die Http-Methoden mit (default ist GET)
def markets_view(request):
    
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)   # many=True bedeutet es wird eine Liste von Objekten übergeben!
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data)    # die Daten aus unserem Request werden übergeben
        if serializer.is_valid():                           # es wird geprüft ob die Daten valide sind
            serializer.save()                               # die Daten werden in die Datenbank gespeichert und es wird "create()" aufgerufen (aus "serializers.py")
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

        # try:      # alte POST-Methode
        #     msg = request.data['message']               # holt sich aus dem Request (Anfrage) den Wert aus dem Dictionary mit dem Key 'message'
        #     return Response({'your_message': msg}, status=status.HTTP_201_CREATED)
        # except:
        #     return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def market_single_view(request, pk):                # single view (Anzeige eines einzelnen Market-Objekts)

    if request.method == 'GET':
        market = Market.objects.get(pk=pk)          # der pk aus der URL wird übergeben und damit das entsprechende Market-Objekt geholt!
        serializer = MarketSerializer(market)       # das einzelne Market-Objekt (Instanz) wird dem Serializer übergeben! (kein many=True mehr!)
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
@api_view(['GET', 'POST'])
def sellers_view(request):

    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerDetailSerializer(sellers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# für products:
@api_view(['GET', 'POST'])
def products_view(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
