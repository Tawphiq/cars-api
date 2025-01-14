from django.contrib import admin
from .models import Car, Wishlist

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model_group', 'vin', 'location_city', 'sale_status')
    list_filter = ('year', 'make', 'model_group', 'location_state', 'sale_status')
    search_fields = ('vin', 'make', 'model_group', 'model_detail')
    ordering = ('-created_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'car__vin')
