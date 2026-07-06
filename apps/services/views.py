from django.shortcuts import render, redirect, get_object_or_404
from .models import Procedures, Medicine, Doctor
from .forms import ProcedureForm, MedicineForm, DoctorForm
from crpms.branch_utils import get_branch_id, branch_queryset


def procedure_panel(request):
    procedures = branch_queryset(request, Procedures)
    medicines = branch_queryset(request, Medicine)
    doctors = branch_queryset(request, Doctor).order_by("name")

    return render(request, "service.html", {
        "procedures": procedures,
        "medicines": medicines,
        "doctors": doctors,
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
            procedure = form.save(commit=False)
            procedure.branch_id = get_branch_id(request)
            procedure.save()
    return redirect("procedure_panel")


def medicine_create(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.branch_id = get_branch_id(request)
            medicine.save()
    # return redirect("procedure_panel")
    return redirect("/services/#medicine")


def doctor_create(request):
    form = DoctorForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)

        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.branch_id = get_branch_id(request)
            doctor.save()

    return redirect("/services/#doctors")


# ======================
# UPDATE
# ======================
def procedure_update(request, pk):
    procedure = get_object_or_404(branch_queryset(request, Procedures), pk=pk)

    if request.method == "POST":
        form = ProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()

    return redirect("procedure_panel")


def medicine_update(request, pk):
    medicine = get_object_or_404(branch_queryset(request, Medicine), pk=pk)

    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()

    return redirect("/services/#medicine")


def doctor_update(request, pk):
    doctor = get_object_or_404(branch_queryset(request, Doctor), pk=pk)
    form = DoctorForm(request.POST or None, request.FILES or None, instance=doctor)

    if form.is_valid():
        form.save()

    return redirect("/services/#doctors")

# ======================
# DELETE
# ======================
def procedure_delete(request, pk):
    if request.method == "POST":
        get_object_or_404(branch_queryset(request, Procedures), pk=pk).delete()
    return redirect("procedure_panel")


def medicine_delete(request, pk):
    if request.method == "POST":
        get_object_or_404(branch_queryset(request, Medicine), pk=pk).delete()
    return redirect("/services/#medicine")


def doctor_delete(request, pk):
    doctor = get_object_or_404(branch_queryset(request, Doctor), pk=pk)
    doctor.delete()
    return redirect("/services/#doctors")
