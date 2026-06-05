from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Branch, Department
from .forms import BranchForm, DepartmentForm
import os
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Bill, BillItem
from .forms  import BillForm, BillItemFormSet


# ── SETTINGS HOME ─────────────────────────────────────────────────────────────

def settings_view(request):
    """Settings overview — renders the card-grid home page."""
    return render(request, 'settings.html')          # ← was redirect()


# ── BRANCHES ──────────────────────────────────────────────────────────────────

def settings_branches(request):
    branches = Branch.objects.all()
    form = BranchForm()
    return render(request, 'branches.html', {
        'branches': branches,
        'form': form,
        # active_section removed — templates handle active state themselves
    })


def branch_create(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()
            messages.success(request, f'Branch "{branch.name}" created successfully.')
            return redirect('settings_branches')
        branches = Branch.objects.all()
        return render(request, 'branches.html', {
            'branches': branches,
            'form': form,
        })
    return redirect('settings_branches')


def branch_edit(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, f'Branch "{branch.name}" updated.')
            return redirect('settings_branches')
        branches = Branch.objects.all()
        return render(request, 'branches.html', {
            'branches': branches,
            'form': form,
        })
    # GET: no longer used by the template (loadEdit() reads from the DOM)
    return redirect('settings_branches')                  # ← was JsonResponse


# ── BRANCHES DELETE ───────────────────────────────────────────────────────────

@require_POST
def branch_delete(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    name = branch.name
    branch.delete()
    messages.success(request, f'Branch "{name}" deleted.')
    return redirect('settings_branches')


# ── DEPARTMENTS ───────────────────────────────────────────────────────────────

def settings_departments(request):
    departments = Department.objects.select_related('branch').all()
    form = DepartmentForm()
    return render(request, 'departments.html', {
        'departments': departments,
        'form': form,
        # active_section removed
    })


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" created successfully.')
            return redirect('settings_departments')
        departments = Department.objects.select_related('branch').all()
        return render(request, 'departments.html', {
            'departments': departments,
            'form': form,
        })
    return redirect('settings_departments')


def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department "{dept.name}" updated.')
            return redirect('settings_departments')
        departments = Department.objects.select_related('branch').all()
        return render(request, 'departments.html', {
            'departments': departments,
            'form': form,
        })
    # GET: no longer used by the template (loadEdit() reads from the DOM)
    return redirect('settings_departments')               # ← was JsonResponse


# ── DEPARTMENTS DELETE ────────────────────────────────────────────────────────

@require_POST
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    name = dept.name
    dept.delete()
    messages.success(request, f'Department "{name}" deleted.')
    return redirect('settings_departments')



# ─────────────────────────────────────────────────────────────────
# LIST
# ─────────────────────────────────────────────────────────────────
def bill_list(request):
    qs = Bill.objects.prefetch_related('items').select_related('branch')

    q       = request.GET.get('q', '').strip()
    status  = request.GET.get('status', '')
    cat     = request.GET.get('category', '')

    if q:
        qs = qs.filter(
            Q(bill_number__icontains=q) |
            Q(vendor_name__icontains=q)
        )
    if cat:
        qs = qs.filter(category=cat)

    # status filter is post-queryset (computed property)
    all_bills = list(qs)
    if status:
        all_bills = [b for b in all_bills if b.status == status]

    # Summary
    all_b = list(Bill.objects.prefetch_related('items'))
    total_bills = len(all_b)
    total_amount = sum(b.total_amount for b in all_b)
    total_paid    = sum(b.paid_amount for b in all_b)
    total_pending = sum(b.pending_amount for b in all_b)
    overdue_count = sum(1 for b in all_b if b.is_overdue)

    paginator = Paginator(all_bills, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'bill_list.html', {
        'active_menu':   'expenses',
        'page_obj':       page,
        'bills':          page.object_list,
        'total_bills':    total_bills,
        'total_amount':   total_amount,
        'total_paid':     total_paid,
        'total_pending':  total_pending,
        'overdue_count':  overdue_count,
        'categories':     Bill.Category.choices,
        'filter_q':       q,
        'filter_status':  status,
        'filter_cat':     cat,
    })


# ─────────────────────────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────────────────────────
def bill_create(request):
    if request.method == 'POST':
        form = BillForm(request.POST, request.FILES)
        formset = BillItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            bill = form.save()
            formset.instance = bill
            formset.save()
            messages.success(request, f"Bill #{bill.bill_number} created successfully.")
            return redirect('bill_list')
    else:
        form = BillForm()
        formset = BillItemFormSet()

    return render(request, 'bill_form.html', {
        'active_menu': 'expenses',
        'form':         form,
        'formset':      formset,
        'action':       'Add',
    })


# ─────────────────────────────────────────────────────────────────
# DETAIL
# ─────────────────────────────────────────────────────────────────
def bill_detail(request, pk):
    bill = get_object_or_404(Bill.objects.prefetch_related('items'), pk=pk)
    return render(request, 'bill_detail.html', {
        'active_menu': 'expenses',
        'bill':         bill,
    })


# ─────────────────────────────────────────────────────────────────
# EDIT
# ─────────────────────────────────────────────────────────────────
def bill_edit(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        form = BillForm(request.POST, request.FILES, instance=bill)
        formset = BillItemFormSet(request.POST, instance=bill)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Bill #{bill.bill_number} updated.")
            return redirect('bill_detail', pk=bill.pk)
    else:
        form = BillForm(instance=bill)
        formset = BillItemFormSet(instance=bill)

    return render(request, 'expenses/bill_form.html', {
        'active_menu': 'expenses',
        'form':         form,
        'formset':      formset,
        'bill':         bill,
        'action':       'Edit',
    })


# ─────────────────────────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────────────────────────
def bill_delete(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == 'POST':
        if bill.attachment:
            try:
                if os.path.isfile(bill.attachment.path):
                    os.remove(bill.attachment.path)
            except Exception:
                pass
        bill.delete()
        messages.success(request, "Bill deleted.")
    return redirect('bill_list')


# ─────────────────────────────────────────────────────────────────
# MARK ITEMS PAID / UNPAID  (AJAX POST from detail page)
# ─────────────────────────────────────────────────────────────────
def bill_mark_items(request, pk):
    """
    POST body: paid_items=1&paid_items=3&paid_items=5  (item PKs to mark paid)
    All other items of this bill are marked unpaid.
    Returns JSON with updated totals.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    bill       = get_object_or_404(Bill.objects.prefetch_related('items'), pk=pk)
    paid_ids   = set(int(x) for x in request.POST.getlist('paid_items') if x.isdigit())

    for item in bill.items.all():
        item.is_paid = (item.pk in paid_ids)
        item.save(update_fields=['is_paid'])

    # Refresh
    bill.refresh_from_db()
    # Re-fetch items for fresh totals
    bill_fresh = get_object_or_404(Bill.objects.prefetch_related('items'), pk=pk)

    return JsonResponse({
        'status':          bill_fresh.status,
        'status_display':  bill_fresh.status_display,
        'total_amount':    float(bill_fresh.total_amount),
        'paid_amount':     float(bill_fresh.paid_amount),
        'pending_amount':  float(bill_fresh.pending_amount),
        'paid_count':      bill_fresh.paid_items_count,
        'total_count':     bill_fresh.total_items_count,
    })