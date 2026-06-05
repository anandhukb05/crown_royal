from django.db import models
from django.utils import timezone


class Branch(models.Model):
    name       = models.CharField(max_length=150)
    address    = models.TextField(blank=True)
    city       = models.CharField(max_length=100, blank=True)
    phone      = models.CharField(max_length=30, blank=True)
    email      = models.EmailField(blank=True)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name


class Department(models.Model):
    name        = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    branch      = models.ForeignKey(
                      Branch,
                      on_delete=models.SET_NULL,
                      null=True, blank=True,
                      related_name='departments',
                  )
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Bill(models.Model):
    """
    One bill / invoice from a vendor.
    Status is derived from its line items — no manual status field needed.
    """

    class Category(models.TextChoices):
        EQUIPMENT     = 'equipment',     'Equipment'
        INSTRUMENT    = 'instrument',    'Instrument'
        CONSUMABLE    = 'consumable',    'Consumable / Supply'
        MEDICINE      = 'medicine',      'Medicine / Drug'
        MAINTENANCE   = 'maintenance',   'Maintenance & Repair'
        STERILIZATION = 'sterilization', 'Sterilization Supply'
        XRAY          = 'xray',          'X-Ray / Imaging'
        FURNITURE     = 'furniture',     'Furniture & Fixture'
        SOFTWARE      = 'software',      'Software / Subscription'
        OTHER         = 'other',         'Other'

    class PaymentMethod(models.TextChoices):
        CASH          = 'cash',          'Cash'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        CHEQUE        = 'cheque',        'Cheque'
        CARD          = 'card',          'Debit / Credit Card'
        UPI           = 'upi',           'UPI'
        OTHER         = 'other',         'Other'

    bill_number    = models.CharField(max_length=100, unique=True)
    bill_date      = models.DateField(default=timezone.now)
    due_date       = models.DateField(null=True, blank=True)
    category       = models.CharField(
                         max_length=20,
                         choices=Category.choices,
                         default=Category.EQUIPMENT,
                     )
    vendor_name    = models.CharField(max_length=200)
    vendor_contact = models.CharField(max_length=100, blank=True)
    branch         = models.ForeignKey(          # ← direct class ref, same file
                         Branch,
                         on_delete=models.SET_NULL,
                         null=True, blank=True,
                         related_name='bills',
                     )
    payment_method = models.CharField(
                         max_length=20,
                         choices=PaymentMethod.choices,
                         blank=True,
                     )
    notes          = models.TextField(blank=True)
    attachment     = models.FileField(
                         upload_to='expenses/bills/%Y/%m/',
                         null=True, blank=True,
                         help_text="Upload bill image (JPG/PNG) or PDF",
                     )
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-bill_date', '-created_at']

    def __str__(self):
        return f"Bill #{self.bill_number} — {self.vendor_name}"

    @property
    def total_amount(self):
        return sum(item.amount for item in self.items.all())

    @property
    def paid_amount(self):
        return sum(item.amount for item in self.items.filter(is_paid=True))

    @property
    def pending_amount(self):
        return self.total_amount - self.paid_amount

    @property
    def paid_items_count(self):
        return self.items.filter(is_paid=True).count()

    @property
    def total_items_count(self):
        return self.items.count()

    @property
    def status(self):
        items = list(self.items.all())
        if not items:
            return 'pending'
        paid_count = sum(1 for i in items if i.is_paid)
        if paid_count == 0:
            return 'pending'
        if paid_count == len(items):
            return 'paid'
        return 'partial'

    @property
    def status_display(self):
        return {
            'pending': 'Pending',
            'paid':    'Paid',
            'partial': 'Partial',
        }.get(self.status, 'Pending')

    @property
    def attachment_is_pdf(self):
        if self.attachment:
            return self.attachment.name.lower().endswith('.pdf')
        return False

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'paid':
            return timezone.now().date() > self.due_date
        return False


class BillItem(models.Model):
    """A single line item on a Bill."""

    bill       = models.ForeignKey(
                     Bill,
                     on_delete=models.CASCADE,
                     related_name='items',
                 )
    name       = models.CharField(max_length=200)
    quantity   = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid    = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} x{self.quantity} @ ₹{self.unit_price}"

    @property
    def amount(self):
        return self.unit_price * self.quantity