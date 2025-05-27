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
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Financa(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=(('receita', 'Receita'), ('despesa', 'Despesa')))
