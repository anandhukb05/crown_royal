from django import forms
from .models import Branch, Department
from django.forms import inlineformset_factory
from .models import Bill, BillItem


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'city', 'phone', 'email', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Main Street Clinic',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Street address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 98765 43210',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'branch@example.com',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'branch', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Orthodontics',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief description (optional)',
            }),
            'branch': forms.Select(attrs={
                'class': 'form-select',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'bill_number', 'bill_date', 'due_date', 'category',
            'vendor_name', 'vendor_contact',
            'payment_method', 'branch',
            'attachment', 'notes',
        ]
        widgets = {
            'bill_number':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. INV-2024-001'}),
            'bill_date':      forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category':       forms.Select(attrs={'class': 'form-select'}),
            'vendor_name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor / Supplier name'}),
            'vendor_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone or email'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'branch':         forms.Select(attrs={'class': 'form-select'}),
            'attachment':     forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
            'notes':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional notes…'}),
        }

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file and hasattr(file, 'name'):
            ext = file.name.lower().split('.')[-1]
            if ext not in ('jpg', 'jpeg', 'png', 'webp', 'pdf'):
                raise forms.ValidationError("Only JPG, PNG, WEBP, or PDF files are allowed.")
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10 MB.")
        return file


class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['name', 'quantity', 'unit_price']
        widgets = {
            'name':       forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Item name / description',
            }),
            'quantity':   forms.NumberInput(attrs={
                'class': 'form-control form-control-sm text-center',
                'min': '1', 'value': '1',
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '0.00', 'step': '0.01', 'min': '0',
            }),
        }


# Inline formset — up to 20 items, at least 1 required
BillItemFormSet = inlineformset_factory(
    Bill,
    BillItem,
    form=BillItemForm,
    fields=['name', 'quantity', 'unit_price'],
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)