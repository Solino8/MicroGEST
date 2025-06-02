from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Produto, Venda, Financa
from .serializers import ProdutoSerializer, VendaSerializer, FinancaSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']

        if produto.estoque < quantidade:
            raise serializers.ValidationError('Estoque insuficiente para essa venda.')

        # Atualiza o estoque
        produto.estoque -= quantidade
        produto.save()

        serializer.save()

    def perform_update(self, serializer):
        # Para atualizar uma venda, precisamos ajustar o estoque considerando a quantidade antiga e a nova
        instance = self.get_object()
        produto = instance.produto
        quantidade_antiga = instance.quantidade
        quantidade_nova = serializer.validated_data.get('quantidade', quantidade_antiga)

        # Calcula diferença
        diferenca = quantidade_nova - quantidade_antiga

        if diferenca > 0 and produto.estoque < diferenca:
            raise serializers.ValidationError('Estoque insuficiente para essa atualização.')

        # Ajusta estoque
        produto.estoque -= diferenca
        produto.save()

        serializer.save()

    def perform_destroy(self, instance):
        # Ao deletar a venda, devolve o estoque
        produto = instance.produto
        produto.estoque += instance.quantidade
        produto.save()
        instance.delete()

class FinancaViewSet(viewsets.ModelViewSet):
    queryset = Financa.objects.all()
    serializer_class = FinancaSerializer
    permission_classes = [IsAuthenticated]