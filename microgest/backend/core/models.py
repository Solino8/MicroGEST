from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',  # Alterado para evitar conflito
        blank=True,
        help_text='Grupos que este usuário pertence.',
        verbose_name='groups',
        related_query_name='usuario',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_set',  # Alterado para evitar conflito
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='user permissions',
        related_query_name='usuario',
    )

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    alerta_minimo = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

from django.contrib.auth.models import User  # Pra vincular a venda ao usuário (opcional)

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='vendas', null=True, blank=True)
    quantidade = models.PositiveIntegerField()
    data_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # opcional

    def __str__(self):
        return f'Venda de {self.quantidade}x {self.produto.nome} em {self.data_venda.strftime("%d/%m/%Y %H:%M")}'

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Financa(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    descricao = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.descricao}"
