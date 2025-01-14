from django.db import models
from django.conf import settings

class Car(models.Model):
    yard_name = models.CharField(max_length=100)
    sale_date = models.DateTimeField(null=True, blank=True)
    sale_time = models.TimeField(null=True, blank=True)
    time_zone = models.CharField(max_length=10, null=True, blank=True)
    item_number = models.CharField(max_length=50, null=True, blank=True)
    lot_number = models.CharField(max_length=50)
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model_group = models.CharField(max_length=100)
    model_detail = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    damage_description = models.TextField(null=True, blank=True)
    secondary_damage = models.CharField(max_length=100, null=True, blank=True)
    sale_title_state = models.CharField(max_length=50, null=True, blank=True)
    sale_title_type = models.CharField(max_length=50, null=True, blank=True)
    has_keys = models.BooleanField(default=False)
    vin = models.CharField(max_length=17)
    odometer = models.IntegerField(null=True, blank=True)
    odometer_brand = models.CharField(max_length=50, null=True, blank=True)
    engine = models.CharField(max_length=50, null=True, blank=True)
    drive = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, null=True, blank=True)
    fuel_type = models.CharField(max_length=50, null=True, blank=True)
    cylinders = models.CharField(max_length=20, null=True, blank=True)
    runs_drives = models.CharField(max_length=100, null=True, blank=True)
    sale_status = models.CharField(max_length=50, null=True, blank=True)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=50)
    location_zip = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.year} {self.make} {self.model_group}"

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')
