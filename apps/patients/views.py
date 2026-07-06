import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PatientProfileForm
from .models import PatientProfile
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vital, ClinicalNotes, PatientProcedure, Prescription, Gallery
from apps.services.models import Procedures, Medicine
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

from crpms.branch_utils import get_branch_id, branch_queryset


def create_patient(request):
    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES)
        image_file = request.FILES.get("image_file")

        if form.is_valid():
            patient = form.save(commit=False)
            patient.image_path = ""
            patient.branch_id = get_branch_id(request)
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

    patients = branch_queryset(request, PatientProfile).order_by("-patient_id")

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
    patient = get_object_or_404(branch_queryset(request, PatientProfile), pk=pk)

    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES, instance=patient)  # ✅ FIX

        if form.is_valid():
            patient = form.save(commit=False)

            image_file = request.FILES.get("image_file")

            # HANDLE IMAGE UPDATE
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

            # IMPORTANT: DON'T REDIRECT HERE
            return redirect("patient_view")  # (see note below)

    return redirect("patient_view")


def delete_patient(request, pk):
    patient = get_object_or_404(branch_queryset(request, PatientProfile), pk=pk)

    if request.method == "POST":
        # Delete image folder (optional but recommended)
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
    profile = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=pk)
    vital = branch_queryset(request, Vital, patient_id=profile).order_by('-created_at')
    notes = branch_queryset(request, ClinicalNotes, patient_id=profile).order_by('-created_at')
    procedures = branch_queryset(request, PatientProcedure, patient_id=profile).order_by('-created_at')
    prescription = branch_queryset(request, Prescription, patient_id=profile).order_by('-created_at')
    gallery_items = branch_queryset(request, Gallery, patient_id=profile).order_by("-created_at")

    procedures_list = branch_queryset(request, Procedures)
    medicine_list = branch_queryset(request, Medicine)
    return render(
            request,
            "profile_view.html",
            {
                'profile': profile,
                'vitals': vital,
                'notes': notes,
                'procedures': procedures,
                'procedures_list': procedures_list,
                'medicine_list': medicine_list,
                'prescriptions': prescription,
                "gallery": gallery_items
            })


# views.py


def vital_view(request, patient_id):
    patient = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=patient_id)
    # get latest vital (for update)
    vital = branch_queryset(request, Vital, patient=patient).order_by('-created_at').first()

    if request.method == "POST":
        data = request.POST

        Vital.objects.create(
                branch_id=get_branch_id(request),
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
    vital = get_object_or_404(branch_queryset(request, Vital), pk=pk)

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
    vital = get_object_or_404(branch_queryset(request, Vital), pk=pk)
    vital.delete()
    return redirect(request.META.get("HTTP_REFERER"))


def clinical_note(request, patient_id):
    patient = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=patient_id)
    # get latest vital (for update)
    notes = branch_queryset(request, ClinicalNotes, patient=patient).order_by('-created_at').first()

    if request.method == "POST":
        data = request.POST

        ClinicalNotes.objects.create(
                branch_id=get_branch_id(request),
                patient=patient,
                notes=data.get("note"),
            )
        messages.success(request, "Note added successfully")

    # return redirect("patient_profile", pk=patient.patient_id)
    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-notes")



def notes_edit(request, pk):
    notes = get_object_or_404(branch_queryset(request, ClinicalNotes), pk=pk)

    if request.method == "POST":
        fields = [
            "notes"
        ]
        for field in fields:
            setattr(notes, field, request.POST.get(field) or None)

        notes.save()
        return redirect(f"{reverse('patient_profile', kwargs={'pk': notes.patient_id})}#tab-notes")


def notes_delete(request, pk):
    notes = get_object_or_404(branch_queryset(request, ClinicalNotes), pk=pk)
    notes.delete()
    return redirect(f"{reverse('patient_profile', kwargs={'pk': notes.patient_id})}#tab-notes")


def add_procedure(request, patient_id):
    patient = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=patient_id)

    if request.method == 'POST':
        PatientProcedure.objects.create(
            branch_id=get_branch_id(request),
            patient=patient,
            added_date=timezone.now(),
            procedure=get_object_or_404(
                branch_queryset(request, Procedures), id=request.POST.get('procedure_id')
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
    procedure = get_object_or_404(branch_queryset(request, PatientProcedure), pk=pk)

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
    procedure = get_object_or_404(branch_queryset(request, PatientProcedure), pk=pk)
    procedure.delete()
    # return redirect(f"{reverse('patient_profile', kwargs={'pk': procedure.patient_id})}#tab-procedure")
    return redirect(
    reverse('patient_profile', kwargs={'pk': procedure.patient.patient_id}) + '#tab-procedure'
)


def add_prescription(request, patient_id):

    patient = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=patient_id)

    if request.method == "POST":

        next_review = request.POST.get("next_review")
        next_review_date = None

        if next_review:
            next_review_date = timezone.make_aware(
                datetime.strptime(next_review, "%Y-%m-%d")
            )

        medicine_obj = get_object_or_404(
            branch_queryset(request, Medicine), id=request.POST.get("medicine_id")
        )

        quantity = int(request.POST.get("quantity") or 1)

        if quantity <= 0:
            messages.error(request, "Quantity must be at least 1")
            return redirect(
                f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-prescription"
            )

        if quantity > medicine_obj.count:
            messages.error(
                request,
                f"Only {medicine_obj.count} units of {medicine_obj.medicine} available in stock"
            )
            return redirect(
                f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-prescription"
            )

        after_food = request.POST.get("after_food") == "True"

        Prescription.objects.create(
            branch_id=get_branch_id(request),
            patient=patient,

            medicine=medicine_obj,
            quantity=quantity,
            price=medicine_obj.price,

            next_review_date=next_review_date,

            strength=request.POST.get("strength"),
            strength_unit=request.POST.get("strength_unit"),

            duration=request.POST.get("duration"),
            duration_period=request.POST.get("duration_period"),

            morning=request.POST.get("morning") or 0,
            noon=request.POST.get("noon") or 0,
            night=request.POST.get("night") or 0,

            status=request.POST.get("status") or 0,

            after_food=after_food,
            usage=request.POST.get("usage"),
        )

        medicine_obj.count -= quantity
        medicine_obj.save()

        messages.success(request, "Prescription added successfully")

    return redirect(
        f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-prescription"
    )


def prescription_edit(request, pk):

    prescription = get_object_or_404(branch_queryset(request, Prescription), pk=pk)

    if request.method == "POST":

        new_medicine = get_object_or_404(
            branch_queryset(request, Medicine), id=request.POST.get("medicine_id")
        )
        new_quantity = int(request.POST.get("quantity") or 1)

        old_medicine = prescription.medicine
        old_quantity = prescription.quantity

        if new_medicine.id == old_medicine.id:
            # same medicine: only the difference in quantity affects stock
            diff = new_quantity - old_quantity
            available = old_medicine.count
            if diff > 0 and diff > available:
                messages.error(
                    request,
                    f"Only {available} units of {old_medicine.medicine} available in stock"
                )
                return redirect(
                    f"{reverse('patient_profile', kwargs={'pk': prescription.patient.patient_id})}#tab-prescription"
                )
            old_medicine.count -= diff
            old_medicine.save()
        else:
            # medicine changed: restock old medicine, deduct from new
            if new_quantity > new_medicine.count:
                messages.error(
                    request,
                    f"Only {new_medicine.count} units of {new_medicine.medicine} available in stock"
                )
                return redirect(
                    f"{reverse('patient_profile', kwargs={'pk': prescription.patient.patient_id})}#tab-prescription"
                )
            old_medicine.count += old_quantity
            old_medicine.save()
            new_medicine.count -= new_quantity
            new_medicine.save()

        prescription.medicine = new_medicine
        prescription.quantity = new_quantity
        prescription.price = new_medicine.price

        prescription.strength = request.POST.get("strength")
        prescription.strength_unit = request.POST.get("strength_unit")

        prescription.duration = request.POST.get("duration")
        prescription.duration_period = request.POST.get("duration_period")

        prescription.morning = request.POST.get("morning", 0)
        prescription.noon = request.POST.get("noon", 0)
        prescription.night = request.POST.get("night", 0)

        prescription.after_food = request.POST.get("after_food")

        prescription.status = request.POST.get("status")

        prescription.save()

        messages.success(request, "Prescription updated successfully")

    patient_id = prescription.patient.patient_id

    return redirect(
        f"{reverse('patient_profile', kwargs={'pk': patient_id})}#tab-prescription"
    )


def prescription_delete(request, pk):

    prescription = get_object_or_404(branch_queryset(request, Prescription), pk=pk)

    patient_id = prescription.patient.patient_id

    if request.method == "POST":
        medicine_obj = prescription.medicine
        medicine_obj.count += prescription.quantity
        medicine_obj.save()

        prescription.delete()
        messages.success(request, "Prescription deleted successfully")

    return redirect(
        f"{reverse('patient_profile', kwargs={'pk': patient_id})}#tab-prescription"
    )


def patient_bill(request, patient_id):
    patient = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=patient_id)

    planned_procedures = (
        branch_queryset(request, PatientProcedure, patient=patient, status__icontains="plan")
        .select_related("procedure")
        .order_by("-created_at")
    )

    inprogress_prescriptions = (
        branch_queryset(request, Prescription, patient=patient, status="inprogress")
        .select_related("medicine")
        .order_by("-created_at")
    )
    print("--- inprogress_prescriptions ===", inprogress_prescriptions)

    return render(request, "bill.html", {
        "patient": patient,
        "planned_procedures": planned_procedures,
        "inprogress_prescriptions": inprogress_prescriptions,
    })


def add_invoice(request, patient_id):
    patient = get_object_or_404(branch_queryset(request, PatientProfile), patient_id=patient_id)

    if request.method == 'POST':
        pass
    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-prescription")


def upload_gallery(request, patient_id):

    patient = get_object_or_404(branch_queryset(request, PatientProfile), pk=patient_id)

    if request.method == "POST":

        files = request.FILES.getlist("files")

        for f in files:
            Gallery.objects.create(
                branch_id=get_branch_id(request),
                patient=patient,
                file=f
            )

        messages.success(request, "Files uploaded successfully")

    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient.patient_id})}#tab-gallery")


def delete_gallery(request, pk):

    gallery = get_object_or_404(branch_queryset(request, Gallery), pk=pk)
    patient_id = gallery.patient.patient_id

    gallery.file.delete()
    gallery.delete()

    return redirect(f"{reverse('patient_profile', kwargs={'pk': patient_id})}#tab-gallery")