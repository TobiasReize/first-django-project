from rest_framework import serializers
from market_app.models import Market, Seller, Product


def validate_no_x(value):     # allgemeine Validierungsfunktion für "value" (wird in der Regel in eine eigene Datei geschrieben!)
        errors = []
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
            errors.append('no Y in location')
        if errors:
             raise serializers.ValidationError(errors)
        return value


class MarketSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)   # ist der pk (primary key) von unserer Datenbank (muss bei jedem Serializer vorhanden sein!)
    # name = serializers.CharField(max_length=255)      # die Validierung der Daten geschieht hier! (nicht mehr in den models!)
    # location = serializers.CharField(max_length=255, validators=[validate_no_x])    # validators ist die Validierungsfunktion
    # description = serializers.CharField()
    # net_worth = serializers.DecimalField(max_digits=10, decimal_places=2)

    # def create(self, validated_data):                   # wird aufgerufen wenn in der POST-Methode save() ausgeführt wird!
    #     return Market.objects.create(**validated_data)

    # def update(self, instance, validated_data):         # für die PUT-Methode (hier muss eine Instanz übergeben werden!)
    #     instance.name = validated_data.get('name', instance.name)   # der zweite Wert von der .get() Methode ist der default Wert (falls nichts übergeben wird!)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.net_worth = validated_data.get('net_worth', instance.net_worth)
    #     instance.save()
    #     return instance
    
    # def validate_location(self, value):     # eigene Validierungsfunktion für eine bestimmte Eigenschaft: "location" (muss im Funktionsnamen nach "_" stehen!)
    #     if 'X' in value:
    #         raise serializers.ValidationError('no X in location')
    #     return value

    class Meta:
        model = Market          # referenziert auf das Model "Market"
        fields = '__all__'      # übernimmt alle Felder von dem Model "Market"


# für sellers:
class SellerDetailSerializer(serializers.Serializer):   # für GET-Methode (zum Anzeigen der Seller)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)   # nested serializer! ist der komplette Market! (durch die many-to-many Beziehung kann hier der MarketSerializer verwendet werden)
    markets = serializers.StringRelatedField(many=True)       # StringRelatedField nutzt die __str__ Methode und zeigt nur den Namen des Markets an!


class SellerCreateSerializer(serializers.Serializer):   # für POST-Methode (zum Erstellen von Seller), id wird nicht benötigt, da es bei POST erstellt wird!
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # hier soll eine Liste mit den primary-keys von den Markets übergeben werden! (daher IntegerField)

    def validate_markets(self, value):  # Validierungsfunktion für die Variable "markets" (value soll eine Liste mit den pk von Markets sein!)
        markets = Market.objects.filter(id__in=value)   # hier wird gefiltert, damit nur die values in markets sind, dessen id wir auch haben!
        if len(markets) != len(value):                      # hier wird nochmal geprüft ob von der value-Liste auch kein Eintrag rausgefiltert wurde! (sonst hätte man eine id in der Liste, die nicht vorhanden ist!)
            raise serializers.ValidationError({'message': 'Passt nicht mit den IDs!'})
        return value
    
    def create(self, validated_data):           # für die POST-Methode (validated_data ist eine Liste von pk von Markets)
        market_ids = validated_data.pop('markets')    # hier wird aus dem validated_data-Objekt die Markets rausgezogen und in einer Liste gespeichert! (werden entfernt!)
        seller = Seller.objects.create(**validated_data)    # hier wird die Seller-Instanz erstellt (ohne die markets) 
        markets_list = Market.objects.filter(id__in=market_ids)     # hier wird gefiltert, damit nur die market_ids in der markets_list sind, die wir auch haben!
        seller.markets.set(markets_list)                            # hier werden dann die Market-Objekte in das Attribut "markets" des neu-erzeugten Seller-Objekts gespeichert!
        return seller

# Testdaten zum Erstellen von Sellers:
# {
#     "name": "Seller1",
#     "contact_info": "Seller1@test.com",
#     "markets": [2, 3]
# }


# für products:
class ProductDetailSerializer(serializers.Serializer):      # für GET-Methode (zum Anzeigen der Products)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    # market = MarketSerializer(read_only=True)
    market = serializers.StringRelatedField(read_only=True)     # nur der Name des Markets wird angezeigt!
    # seller = SellerDetailSerializer(read_only=True)
    seller = serializers.StringRelatedField(read_only=True)     # nur der Name des Sellers wird angezeigt!


class ProductCreateSerializer(serializers.Serializer):       # für POST-Methode (zum Erstellen von Products)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.IntegerField()
    seller = serializers.IntegerField()

    def validate_market(self, value):
        # Prüfe, ob ein Market mit dieser ID existiert
        if not Market.objects.filter(id=value).exists():
            raise serializers.ValidationError('Market nicht vorhanden!')
        return value  # Gebe die ID zurück (Integer)

    def validate_seller(self, value):
        # Prüfe, ob ein Seller mit dieser ID existiert
        if not Seller.objects.filter(id=value).exists():
            raise serializers.ValidationError('Seller nicht vorhanden!')
        return value  # Gebe die ID zurück (Integer)

    def create(self, validated_data):
        market_id = validated_data.pop('market')
        seller_id = validated_data.pop('seller')
        market = Market.objects.get(id=market_id)
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.create(market=market, seller=seller, **validated_data)
        return product

# Testdaten zum Anzeigen von Products - GET:
# {
#     "id": 1,
#     "name": "Product1",
#     "description": "Beschreibung_1",
#     "price": 49.95,
#     "market": {"id": 2, "name": "HalloMarkt", ...},
#     "seller": {"id": 1, "name": "Seller1", ...}
# }

# Testdaten zum Erstellen von Products - POST:
# {
#     "name": "Product1",
#     "description": "Beschreibung_1",
#     "price": 49.95,
#     "market": 2,
#     "seller": 1
# }