import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PatientProfileForm
from .models import PatientProfile
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vital, ClinicalNotes, PatientProcedure, Prescription
from apps.services.models import Procedures, Medicine
from django.urls import reverse
from django.utils import timezone


def create_patient(request):
    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES)
        image_file = request.FILES.get("image_file")

        if form.is_valid():
            patient = form.save(commit=False)
            patient.image_path = ""
            patient.save()

            if image_file:
                patient_folder = os.path.join(
                    settings.MEDIA_ROOT, "patients", str(patient.patient_id)
                )
                os.makedirs(patient_folder, exist_ok=True)

                image_full_path = os.path.join(
                    patient_folder,
                    f"photo_{patient.patient_id}.png"
                )

                with open(image_full_path, "wb+") as f:
                    for chunk in image_file.chunks():
                        f.write(chunk)

                patient.image_path = f"patients/{patient.patient_id}/photo_{patient.patient_id}.png"
                patient.save()

            messages.success(request, "Patient profile created successfully.")
            return redirect("patient_view")

        else:
            print(form.errors)  # DEBUG

    else:
        form = PatientProfileForm()

    return render(request, "create.html", {"form": form})


def view_patients(request):
    query = request.GET.get("q", "")

    patients = PatientProfile.objects.all().order_by("-patient_id")

    if query:
        patients = patients.filter(
            Q(name__icontains=query) |
            Q(phno__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(patients, 10)  # 10 rows per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "patients_view.html", {
        "page_obj": page_obj,
        "query": query
    })


def edit_patient(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)

    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES, instance=patient)  # ✅ FIX

        if form.is_valid():
            patient = form.save(commit=False)

            image_file = request.FILES.get("image_file")

            # ✅ HANDLE IMAGE UPDATE
            if image_file:
                patient_folder = os.path.join(
                    settings.MEDIA_ROOT, "patients", str(patient.patient_id)
                )
                os.makedirs(patient_folder, exist_ok=True)

                image_path = os.path.join(
                    patient_folder,
                    f"photo_{patient.patient_id}.png"
                )

                with open(image_path, "wb+") as f:
                    for chunk in image_file.chunks():
                        f.write(chunk)

                patient.image_path = f"patients/{patient.patient_id}/photo_{patient.patient_id}.png"

            patient.save()

            messages.success(request, "Patient updated successfully")
            return redirect("patient_view")

        else:
            print(form.errors)  # debug
            messages.error(request, "Please fix the errors")

            # ❗ IMPORTANT: DON'T REDIRECT HERE
            return redirect("patient_view")  # (see note below)

    return redirect("patient_view")

def delete_patient(request, pk):
    patient = get_object_or_404(PatientProfile, pk=pk)

    if request.method == "POST":
        # 🔥 Delete image folder (optional but recommended)
        patient_folder = os.path.join(
            settings.MEDIA_ROOT, "patients", str(patient.patient_id)
        )

        if os.path.exists(patient_folder):
            import shutil
            shutil.rmtree(patient_folder)

        patient.delete()

        messages.success(request, "Patient deleted successfully")
        return redirect("patient_view")

    return redirect("patient_view")

def patient_profile(request, pk):
    profile = PatientProfile.objects.get(patient_id=pk)
    vital = Vital.objects.filter(patient_id=profile).order_by('-created_at')
    notes = ClinicalNotes.objects.filter(patient_id=profile).order_by('-created_at')
    procedures = PatientProcedure.objects.filter(patient_id=profile).order_by('-created_at')

    procedures_list = Procedures.objects.all()
    return render(
            request,
            "profile_view.html",
            {
                'profile': profile,
                'vitals': vital,
                'notes': notes,
                'procedures': procedures,
                'procedures_list': procedures_list
            })


# views.py


def vital_view(request, patient_id):
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)
    # get latest vital (for update)
    vital = Vital.objects.filter(patient=patient).order_by('-created_at').first()

    if request.method == "POST":
        data = request.POST
   
        Vital.objects.create(
                patient=patient,
                temperature=data.get("temperature"),
                weight=data.get("weight"),
                height=data.get("height"),
                sugar=data.get("sugar"),
                systolic=data.get("systolic"),
                diastolic=data.get("diastolic"),
                pulse=data.get("pulse"),
                spo2=data.get("spo2"),
                respiratory=data.get("respiratory"),
            )
        messages.success(request, "Vital added successfully")

    return redirect("patient_profile", pk=patient.patient_id)

    # return render(request, "profile_view.html", {"vital": vital})


def vital_edit(request, pk):
    vital = get_object_or_404(Vital, pk=pk)

    if request.method == "POST":
        fields = [
            "temperature", "weight", "height", "sugar",
            "systolic", "diastolic", "pulse", "spo2", "respiratory"
        ]
        for field in fields:
            setattr(vital, field, request.POST.get(field) or None)

        vital.save()
        return redirect(request.META.get("HTTP_REFERER"))


def vital_delete(request, pk):
    vital = get_object_or_404(Vital, pk=pk)
    vital.delete()
    return redirect(request.META.get("HTTP_REFERER"))


def clinical_note(request, patient_id):
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)
    # get latest vital (for update)
    notes = ClinicalNotes.objects.filter(patient=patient).order_by('-created_at').first()

    if request.method == "POST":
        data = request.POST

        ClinicalNotes.objects.create(
                patient=patient,
                notes=data.get("note"),
            )
        messages.success(request, "Note added successfully")

    # return redirect("patient_profile", pk=patient.patient_id)
    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-notes")



def notes_edit(request, pk):
    notes = get_object_or_404(ClinicalNotes, pk=pk)

    if request.method == "POST":
        fields = [
            "notes"
        ]
        for field in fields:
            setattr(notes, field, request.POST.get(field) or None)

        notes.save()
        return redirect(f"{reverse('patient_profile', kwargs={'pk': notes.patient_id})}#tab-notes")


def notes_delete(request, pk):
    notes = get_object_or_404(ClinicalNotes, pk=pk)
    notes.delete()
    return redirect(f"{reverse('patient_profile', kwargs={'pk': notes.patient_id})}#tab-notes")


def add_procedure(request, patient_id):
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)

    if request.method == 'POST':
        PatientProcedure.objects.create(
            patient=patient,
            added_date=timezone.now(),
            procedure=get_object_or_404(
                Procedures, id=request.POST.get('procedure_id')
            ),
            quantity=int(request.POST.get('quantity', 0)),
            price=float(request.POST.get('price', 0)),
            notes=request.POST.get('notes'),
            discount_type=request.POST.get('discount_type'),
            discount=float(request.POST.get('discount', 0)),
            status=request.POST.get('status')
        )

    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-procedure")


def patient_procedure_edit(request, pk):
    procedure = get_object_or_404(PatientProcedure, pk=pk)

    if request.method == "POST":

        procedure.procedure_id = request.POST.get("procedure_id")

        for field in ("notes", "quantity",
                      "price", "discount", "discount_type", "status", "total"):
            value = request.POST.get(field)
            if value:
                setattr(procedure, field, value)

        procedure.save()

        return redirect(
            f"{reverse('patient_profile', kwargs={'pk': procedure.patient.patient_id})}#tab-procedure"
        )


def patient_procedure_delete(request, pk):
    procedure = get_object_or_404(PatientProcedure, pk=pk)
    procedure.delete()
    # return redirect(f"{reverse('patient_profile', kwargs={'pk': procedure.patient_id})}#tab-procedure")
    return redirect(
    reverse('patient_profile', kwargs={'pk': procedure.patient.patient_id}) + '#tab-procedure'
)


def add_prescription(request, patient_id):
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)

    if request.method == 'POST':

        Prescription.objects.create(
            patient=patient,
            next_review_date=request.POST.get('next_review', 0),
            medicine=get_object_or_404(
                        Medicine, id=request.POST.get('medicine_id')
                    ),
            srength=request.POST.get('strength', 0),
            unit=request.POST.get('quantity', 0),
            duration=request.POST.get('quantity', 0),
            duration_period=request.POST.get('quantity', 0),
            morning=int(request.POST.get('quantity', 0)),
            noon=int(request.POST.get('quantity', 0)),
            night=int(request.POST.get('quantity', 0)),
            after_food=request.POST.get('quantity', 0),
            usage=request.POST.get('quantity', 0)
        )

    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-prescription")


def patient_bill(request, patient_id):
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)
    return render(request, "bill.html",{"patient": patient})

def add_invoice(request, patient_id):
    patient = get_object_or_404(PatientProfile, patient_id=patient_id)

    if request.method == 'POST':
        pass
    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-prescription")