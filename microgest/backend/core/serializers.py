from rest_framework import serializers
from .models import Produto
from .models import Venda
from .models import Financa

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'

class FinancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financa
        fields = '__all__'