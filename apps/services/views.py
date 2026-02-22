from django.shortcuts import render, redirect, get_object_or_404
from .models import Procedures, Medicine, Doctor
from .forms import ProcedureForm, MedicineForm, DoctorForm


def procedure_panel(request):
    procedures = Procedures.objects.all()
    medicines = Medicine.objects.all()
    doctors = Doctor.objects.all().order_by("name")

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
            form.save()
    return redirect("procedure_panel")


def medicine_create(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
    # return redirect("procedure_panel")
    return redirect("/services/#medicine")


def doctor_create(request):
    form = DoctorForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

    return redirect("/services/#doctors")


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


def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST or None, request.FILES or None, instance=doctor)

    if form.is_valid():
        form.save()
 
    return redirect("/services/#doctors")

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


def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    return redirect("/services/#doctors")