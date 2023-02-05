import uuid
from datetime import datetime
from django.db import models
import shortuuid

class Account(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # kaldırsammı
    name = models.CharField(max_length=100, null=True, unique=True)

    phone = models.CharField(max_length=20, null=True)
    licence_date = models.DateTimeField(default=datetime.now)
    license_status = models.BooleanField(default=True)

    date_last_updated = models.DateTimeField(auto_now_add=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    # def get_absolute_url(self):
    #     return reverse('get_account_info', args=[self.id])
    #
    # def validate_unique(self, *args, **kwargs):
    #     super(Account, self).validate_unique(*args, **kwargs)
    #     query = Account.objects.filter(tax_number=self.tax_number)
    #
    #     if query.filter(blocks__block_name=self.customer.block_name).exists():
    #         raise ValidationError({'extension': ['Bu block var', ]})
    #
    #     if query.filter(gates=self.gates.gate_name).exists():
    #         raise ValidationError({'extension': ['Bu kapı adı var', ]})

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name',)


class Apartments(models.Model):
    account = models.ForeignKey(Account, related_name="apartments", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)

    api_key = models.CharField(max_length=32)

    wifi_name = models.CharField(max_length=50, null=True)
    wifi_pass = models.CharField(max_length=20, null=True)

    is_active = models.BooleanField(default=True)
    data_created = models.DateTimeField(auto_now=True, null=True)

    device_last_online_date = models.DateTimeField(auto_now=True, null=True)

    # device = models.OneToOneField("Devices", on_delete=models.CASCADE, related_name="apartments")

    devices = models.ManyToManyField("Devices", related_name="devices_apartments")

    class Meta:
        unique_together = (('account', 'name'), ("api_key",))

    # def validate_unique(self, *args, **kwargs):
    #     super(Blocks, self).validate_unique(*args, **kwargs)
    #     query = Blocks.objects.filter(block_name=self.block_name)
    #     if query.filter(daire__daire_name=self.daires.daire_name).exists():
    #         raise ValidationError({'extension': ['Bu blokta bu daire zaten var', ]})

    # class Meta:
    #     unique_together = (
    #                       ("daire__daire_name", "block_name", "account__tax_number")
    #                        # How can I enforce UserProfile's Client
    #                        # and Extension to be unique? This obviously
    #                        # doesn't work, but is this idea possible without
    #                        # creating another FK in my intermediary model
    #                        # ("account", "block_name")
    #     )

    def __str__(self):
        return self.name


class Devices(models.Model):
    CATEGORIES_CHOICES = (
        ('output', 'Output'),
        ('input', 'Input')
    )

    name = models.CharField(max_length=50, null=True)
    key = models.CharField(max_length=50, null=True)
    apartment = models.ForeignKey('Apartments', on_delete=models.CASCADE, related_name="device")
    device_type = models.CharField(max_length=7, default="input", choices=CATEGORIES_CHOICES)
    status = models.BooleanField(default=False)
    label = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('apartment', 'name'), ('apartment', 'key'))












