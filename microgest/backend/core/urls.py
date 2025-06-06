from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, VendaViewSet, FinancaViewSet  # IMPORTAR OS DOIS

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'financas', FinancaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]