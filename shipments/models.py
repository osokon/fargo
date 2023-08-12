from django.db import models
from django_currentuser.db.models import CurrentUserField
from django.db.models import Sum, F, Q

# Create your models here.
parcel_status_choices = (
    ('In China WH', 'In china WH'),
    ('Packed for Shipping', 'Packed for Shipping'),
    ('Shipped', 'Shipped'),
    ('In TZ WH', 'In TZ WH'),
    ('Delivered to Client', 'Delivered to Client'),
)

shipment_status_choices = (
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Received', 'Received'),
)


class Shipment(models.Model):
    shipment_no = models.CharField(max_length=20)
    shipped_on = models.DateField(blank=True, null=True)
    eta = models.DateField(blank=True, null=True, verbose_name='Estimated Arrival')
    received_on = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, editable=False, default='Packed')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(editable=False)
    updated_by = CurrentUserField(editable=False, related_name='shipment_updated_by')

    class Meta:
        ordering = ['-id',]

    @property
    def parcels_count(self):
        count = self.parcels.count()

        return count

    @property
    def estimated_weight(self):
        weight = self.parcels.aggregate(total=Sum(F('weight')))['total']

        return weight

class Parcel(models.Model):
    tracking_no = models.CharField(max_length=20)
    owner = models.CharField(max_length=20)
    owner_mobile = models.PositiveIntegerField()
    weight = models.DecimalField(decimal_places=2, max_digits=6)
    received_on = models.DateField(blank=True, null=True, verbose_name='Received China WH')
    packed_on = models.DateTimeField(blank=True, null=True, editable=False)
    shipped_on = models.DateTimeField(blank=True, null=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, blank=True, null=True, related_name='parcels')
    landed_on = models.DateTimeField(blank=True, null=True, verbose_name='Received TZ')
    delivered_on = models.DateField(blank=True, null=True, verbose_name='Delievered to Client')
    status = models.CharField(max_length=20, default='In China WH', editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(editable=False)
    updated_by = CurrentUserField(editable=False, related_name='parcel_updated_by')

    class Meta:
        ordering = ['-id',]