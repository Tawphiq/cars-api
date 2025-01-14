from django_filters import rest_framework as filters
from .models import Car

class CarFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')
    year_min = filters.NumberFilter(field_name="year", lookup_expr='gte')
    year_max = filters.NumberFilter(field_name="year", lookup_expr='lte')
    
    class Meta:
        model = Car
        fields = {
            'make': ['exact', 'icontains'],
            'model_group': ['exact', 'icontains'],
            'year': ['exact'],
            'fuel_type': ['exact'],
            'transmission': ['exact'],
            'color': ['exact'],
            'location_state': ['exact'],
            'location_city': ['exact'],
            'sale_status': ['exact'],
        } 