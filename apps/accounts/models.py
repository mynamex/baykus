import uuid
from datetime import datetime
from django.db import models


class Account(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # kaldırsammı
    name = models.CharField(max_length=100, null=True, unique=True)
    related_person_name = models.CharField(max_length=80, null=True)
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
    address = models.CharField(max_length=200, null=True)

    name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    data_last_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('account', 'name',)

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
    apartments = models.ForeignKey(Apartments, related_name="devices", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    api_key = models.CharField(max_length=64, default=uuid.uuid1())
    data_last_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('apartments', 'name',)

    def __str__(self):
        return self.name


class Props(models.Model):
    devices = models.ForeignKey(Devices, related_name="props", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    data_last_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('devices', 'name',)

    def __str__(self):
        return self.name
