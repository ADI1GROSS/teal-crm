import re
import unidecode 
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from userprofile.models import Userprofile


@login_required
def edit_deal_template(request, field_name):
    userprofile, _ = Userprofile.objects.get_or_create(user=request.user)
    fields = userprofile.fields or {}
    field = fields.get(field_name)

    if not field:
        messages.error(request, "השדה לא נמצא")
        return redirect("deal_list")

    if request.method == "POST":
        new_label = request.POST.get("label")
        new_type = request.POST.get("type")
        new_default = request.POST.get("default", "")

        if new_type == "choice":
            choices_text = request.POST.get("choices", "")
            options = [opt.strip() for opt in choices_text.split(',') if opt.strip()]

            field["type"] = "choice"
            field["options"] = options
            field["default"] = new_default

        else:
            field.pop("options", None)
            field["type"] = new_type
            field["default"] = new_default

        field["label"] = new_label

        userprofile.fields[field_name] = field
        userprofile.save()

        messages.success(request, f"השדה '{new_label}' עודכן בהצלחה")
        return redirect("deal_list")

    return render(request, "deal/edit_deal_template.html", {
        "field": field,
        "field_name": field_name,
    })


@login_required
def add_deal_template_field(request):
    userprofile, _ = Userprofile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        field_label = request.POST.get("label")
        field_type = request.POST.get("type", "string")
        field_default = request.POST.get("default", "")

        if not field_label:
            messages.error(request, "יש להזין שם שדה")
            return redirect("deal_list")
        
        # make a field name with the lable
        if field_type == 'choice':
           choices_text = request.POST.get('choices', '')
           options = [opt.strip() for opt in choices_text.split(',') if opt.strip()]
           field_data = {
                "label": field_label,
                "type": "choice",
                "default": field_default,
                "options": options
            }
        else:
             field_data = {
               "label": field_label,
               "type": field_type,
               "default": field_default
            }

        field_name = unidecode.unidecode(field_label)  
        field_name = field_name.lower()
        field_name = re.sub(r'[^a-z0-9_]', '_', field_name)  

        fields = userprofile.fields or {}
        if field_name in fields:
            messages.warning(request, "שדה בשם זה כבר קיים")
        else:
            fields[field_name] = field_data  
            userprofile.fields = fields
            userprofile.save()
            messages.success(request, f"השדה '{field_label}' נוסף בהצלחה")
        return redirect("deal_list")
    else:
        return render(request, "deal/add_deal_template.html")

@login_required
def delete_deal_template_field(request, field_name):
    userprofile, _ = Userprofile.objects.get_or_create(user=request.user)

    fields = userprofile.fields or {}
    if field_name in fields:
        label = fields[field_name].get("label", field_name)
        del fields[field_name]
        userprofile.fields = fields
        userprofile.save()
        
        messages.success(request, f"השדה '{label}' נמחק בהצלחה")
    else:
        messages.error(request, "השדה לא נמצא")

    return redirect("deal_list")

@login_required
def deal_list(request):
    userprofile, _ = Userprofile.objects.get_or_create(user=request.user)
    fields = userprofile.fields or {}

    return render(request, "deal/fields_list.html", {"fields": fields})
