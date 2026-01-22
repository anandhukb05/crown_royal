from django.shortcuts import render, redirect, get_object_or_404
from .models import Procedures, Medicine
from .forms import ProcedureForm, MedicineForm


def procedure_panel(request):
    procedures = Procedures.objects.all()
    medicines = Medicine.objects.all()

    return render(request, "service.html", {
        "procedures": procedures,
        "medicines": medicines,
        "procedure_form": ProcedureForm(),
        "medicine_form": MedicineForm(),
    })


# ======================
# CREATE
# ======================
def procedure_create(request):
    if request.method == "POST":
        form = ProcedureForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("procedure_panel")


def medicine_create(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
    # return redirect("procedure_panel")
    return redirect("/services/#medicine")


# ======================
# UPDATE
# ======================
def procedure_update(request, pk):
    procedure = get_object_or_404(Procedures, pk=pk)

    if request.method == "POST":
        form = ProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()

    return redirect("procedure_panel")


def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()

    return redirect("/services/#medicine")


# ======================
# DELETE
# ======================
def procedure_delete(request, pk):
    if request.method == "POST":
        get_object_or_404(Procedures, pk=pk).delete()
    return redirect("procedure_panel")


def medicine_delete(request, pk):
    if request.method == "POST":
        get_object_or_404(Medicine, pk=pk).delete()
    return redirect("/services/#medicine")
