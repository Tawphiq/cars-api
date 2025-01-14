from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, Wishlist
from .serializers import CarSerializer, WishlistSerializer
from .filters import CarFilter

class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['make', 'model_group', 'model_detail', 'vin']
    ordering_fields = ['year', 'created_at', 'price']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, pk=None):
        car = self.get_object()
        wishlist, created = Wishlist.objects.get_or_create(
            user=request.user,
            car=car
        )
        return Response(
            {'status': 'added to wishlist' if created else 'already in wishlist'},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, pk=None):
        car = self.get_object()
        deleted, _ = Wishlist.objects.filter(user=request.user, car=car).delete()
        if deleted:
            return Response({'status': 'removed from wishlist'}, status=status.HTTP_200_OK)
        return Response({'status': 'not in wishlist'}, status=status.HTTP_404_NOT_FOUND)

class WishlistViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
