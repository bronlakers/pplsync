from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Asset, AssetAssignment
from .forms import AssetForm, AssignForm

@login_required
def asset_list(request):
    assets = Asset.objects.all().order_by("status", "asset_tag")[:300]
    return render(request, "assets/list.html", {"assets": assets})

@login_required
def asset_create(request):
    form = AssetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Asset created.")
        return redirect("asset_list")
    return render(request, "assets/form.html", {"title": "New Asset", "form": form})

@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    return render(request, "assets/detail.html", {"asset": asset})

@login_required
def asset_assign(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if asset.status == "retired":
        messages.error(request, "Cannot assign a retired asset.")
        return redirect("asset_detail", asset_id=asset.id)

    form = AssignForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # close any open assignment
        AssetAssignment.objects.filter(asset=asset, returned_at__isnull=True).update(returned_at=timezone.now())
        AssetAssignment.objects.create(asset=asset, employee=form.cleaned_data["employee"], notes=form.cleaned_data["notes"])
        asset.status = "assigned"
        asset.save()
        messages.success(request, "Asset assigned.")
        return redirect("asset_detail", asset_id=asset.id)
    return render(request, "assets/form.html", {"title": f"Assign {asset.asset_tag}", "form": form})

@login_required
def asset_return(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    open_assign = AssetAssignment.objects.filter(asset=asset, returned_at__isnull=True).first()
    if open_assign:
        open_assign.returned_at = timezone.now()
        open_assign.save()
    asset.status = "available"
    asset.save()
    messages.success(request, "Asset returned.")
    return redirect("asset_detail", asset_id=asset.id)
