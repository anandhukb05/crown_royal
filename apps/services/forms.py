from django import forms
from .models import Procedures, Medicine


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedures
        fields = "__all__"

    def clean_prodecure(self):
        value = self.cleaned_data["prodecure"]
        qs = Procedures.objects.filter(prodecure__iexact=value)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Procedure already exists.")

        return value


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = "__all__"

    def clean_medicine(self):
        value = self.cleaned_data["medicine"]
        qs = Medicine.objects.filter(medicine__iexact=value)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Medicine already exists.")

        return value
