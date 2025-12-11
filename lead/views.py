from django.contrib import messages
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm, AddLeadFormPublic, ContactFormSet, ContactFormSetPublic
from django.shortcuts import get_object_or_404, render, redirect
from itertools import groupby
from .forms import AddLeadForm, AddContactForm
from .models import Lead, Contact
from userprofile.models import Userprofile
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML , CSS
from django.core.mail import EmailMessage
from django.templatetags.static import static
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import LeadSerializer, ContactSerializer
from lead.tasks import send_lead_pdf_task
import logging
logger = logging.getLogger(__name__)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-id")
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]   

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by("-id")
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

@login_required
def leads_list(request):
    query = request.GET.get('q', '').strip()
    leads = Lead.objects.filter(created_by=request.user).order_by('date_gregorian')
   
    if query:
       
        leads = leads.annotate(
            full_hebrew_date=Concat(
                'hebrew_day', Value(' '),
                'hebrew_month', Value(' '),
                'hebrew_year'
            )
        ).filter(
            Q(bride_side__icontains=query) |
            Q(groom_side__icontains=query) |
            Q(date_gregorian__icontains=query) |
            Q(hebrew_day__icontains=query) |
            Q(hebrew_month__icontains=query) |
            Q(hebrew_year__icontains=query) |
            Q(full_hebrew_date__icontains=query) | 
            Q(contacts__first_name__icontains=query) |
            Q(contacts__second_name__icontains=query) |
            Q(contacts__phone__icontains=query) |
            Q(contacts__email__icontains=query)
        ).distinct()
    

    leads = list(leads)
    
    # deviding leads by the month of the event
    grouped_leads = {}
    for key, group in groupby(
        leads,
        key=lambda l: (l.hebrew_year, l.hebrew_month)):
        
        grouped_leads[key] = list(group)
        
       

    # colors by the month
    month_colors = {
        "תשרי": "bg-blue-100",
        "חשוון": "bg-purple-100",
        "כסלו": "bg-green-100",
        "טבת": "bg-yellow-100",
        "שבט": "bg-pink-100",
        "אדר": "bg-indigo-100",
        "ניסן": "bg-orange-100",
        "אייר": "bg-teal-100",
        "סיון": "bg-lime-100",
        "תמוז": "bg-rose-100",
        "אב": "bg-emerald-100",
        "אלול": "bg-cyan-100",
    }

    for lead in leads:
        if lead.date_gregorian:
            base_color = month_colors.get(lead.hebrew_month, "bg-gray-100")
            week_number = (lead.date_gregorian.day - 1) // 7
            opacity = 100 - (week_number * 15)
            lead.color_class = f"{base_color} opacity-{opacity}"
        else:
            lead.color_class = "bg-gray-100"
    
    return render(request, 'lead/leads_list.html', {
        'leads': leads,
        'query': query,
        'grouped_leads': grouped_leads,
    })

@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    contacts = lead.contacts.all()
    custom_fields = get_client_fields(request.user, lead)

    return render(request, 'lead/leads_detail.html', {
        'lead': lead,
        'contacts': contacts,
        'fields': custom_fields,
    })

@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()

    messages.success(request, "הלקוח נמחק בהצלחה")

    return redirect('leads_list')

@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, id=pk, lead__created_by=request.user)
    lead_id = contact.lead.id  

    contact.delete()
    messages.success(request, "איש הקשר נמחק בהצלחה!")

    return redirect('leads_detail', pk=lead_id)
    
@login_required
def add_lead(request):
    userprofile, created = Userprofile.objects.get_or_create(user=request.user)
    template_fields = userprofile.fields or {}

    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        formset = ContactFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user

            custom_values = {}
            for key, info in template_fields.items():
                custom_values[key] = request.POST.get(key, "")
            lead.custom_fields = custom_values

            lead.save()

            contacts = formset.save(commit=False)
            for contact in contacts:
                contact.lead = lead
                contact.save()

            messages.success(request, "הלקוח נוצר בהצלחה")

            return redirect('leads_list')
    else:
        form = AddLeadForm()
        formset = ContactFormSet()
    return render(request, 'lead/add_lead.html', {
        'form': form,
        'formset': formset,
        'fields': template_fields
    })

def add_lead_public(request, invite_token):

    userprofile = get_object_or_404(Userprofile, invite_token=invite_token)

    if request.method == 'POST':
        form = AddLeadFormPublic(request.POST)

        bride_form = AddContactForm(request.POST, role="כלה", hide_role=True, prefix="bride")
        groom_form = AddContactForm(request.POST, role="חתן", hide_role=True, prefix="groom")

        formset = ContactFormSetPublic(request.POST)

        if form.is_valid() and bride_form.is_valid() and groom_form.is_valid() and formset.is_valid():

            lead = form.save(commit=False)
            lead.created_by = userprofile.user  
            lead.status = 'יצר קשר'
            lead.payment_status = 'לא שילם'

            if lead.has_additional_crew and not lead.additional_crew:
                lead.additional_crew = "❓"

            lead.save()

            
            bride = bride_form.save(commit=False)
            bride.lead = lead
            bride.save()

            
            groom = groom_form.save(commit=False)
            groom.lead = lead
            groom.save()

            
            extra_contacts = formset.save(commit=False)
            for c in extra_contacts:
                c.lead = lead
                c.save()

            return render(request, 'lead/thanks.html', {'lead': lead})

    else:
        form = AddLeadFormPublic()
        bride_form = AddContactForm(role="כלה", hide_role=True, prefix="bride")
        groom_form = AddContactForm(role="חתן", hide_role=True, prefix="groom")
        formset = ContactFormSetPublic()

    return render(request, 'lead/add_lead_public.html', {
        'form': form,
        'bride_form': bride_form,
        'groom_form': groom_form,
        'formset': formset,
        'userprofile': userprofile,
    })


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, id=pk, lead__created_by=request.user)
    lead_id = contact.lead.id 

    if request.method == 'POST':
        form = AddContactForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()

            messages.success(request, "פרטי איש הקשר נערכו בהצלחה")

            return redirect('leads_detail', pk=lead_id)
    else:
        form = AddContactForm(instance=contact)
    return render(request, 'lead/add_contact.html', {
        'form': form,
        'contact': contact
    })

@login_required
def add_contact(request, pk):
    lead = get_object_or_404(Lead, id=pk, created_by=request.user)

    if request.method == 'POST':
        form = AddContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.lead = lead
            contact.save()
            messages.success(request, "איש הקשר נוסף בהצלחה!")
            return redirect('leads_detail', pk=pk)
    else:
        form = AddContactForm()

    return render(request, 'lead/add_contact.html', {'form': form, 'lead': lead})


def get_client_fields(user, lead):
    userprofile, _ = Userprofile.objects.get_or_create(user=user)

    # אם השדות נשמרים ישירות ב-userprofile
    template_fields = getattr(userprofile, "fields", {})

    client_data = lead.custom_fields or {}

    merged = {}
    for key, info in template_fields.items():
        value = client_data.get(key, info.get("default"))
        if isinstance(value, str):
            if value in ["true", "True", "1", True]:
                value = "כן"
            elif value in ["false", "False", "0", False]:
                value = "לא"
        merged[key] = {
            "label": info.get("label"),
            "type": info.get("type"),
            "value": value,
        }
    return merged
    
@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    userprofile, _ = Userprofile.objects.get_or_create(user=request.user)
    template_fields = getattr(userprofile, "fields", {})

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            new_values = {}
            for key in template_fields.keys():
                if key in request.POST:
                    new_values[key] = request.POST.get(key)
            lead.custom_fields = new_values
            form.save()
            
            
            messages.success(request, "פרטי הלקוח נערכו בהצלחה")
            return redirect('leads_list')
    
    else:
        form = AddLeadForm(instance=lead)
    merged = get_client_fields(request.user, lead)
    return render(request, 'lead/leads_edit.html', {
        "form": form,
        "fields": merged
    })

def lead_pdf(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        messages.error(request, "הלקוח לא נמצא")
        return redirect("leads_list")

    userprofile = getattr(request.user, "userprofile", None)

    bride_contact = lead.contacts.filter(role="כלה").first()
    groom_contact = lead.contacts.filter(role="חתן").first()

    custom_fields = get_client_fields(request.user, lead)

    try:
        html_string = render_to_string('lead/lead_pdf.html', {
            "lead": lead,
            "userprofile": userprofile,
            "bride_contact": bride_contact,
            "groom_contact": groom_contact,
            "fields": custom_fields,
        })

        pdf = HTML(
            string=html_string,
            base_url=request.build_absolute_uri()  # ✔️ חובה
        ).write_pdf()

    except Exception as e:
        print("PDF ERROR:", e)
        messages.error(request, "לא ניתן ליצור PDF כרגע")
        return redirect("leads_list")

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="lead_{lead.id}.pdf"'
    return response

def send_client_email(request, pk):
    
    lead = get_object_or_404(Lead, pk=pk)

    userprofile = get_object_or_404(Userprofile, user=request.user)

    emails = [
        (c.email, f"{c.first_name} {c.second_name}")
        for c in lead.contacts.all() if c.email
    ]

    if request.method == "POST":
        chosen_email = request.POST.get("chosen_email")

        try:
            template_fields = userprofile.fields or {}
            fields = {}
            for key, info in template_fields.items():
                value = (lead.custom_fields or {}).get(key, info.get("default"))
                fields[key] = {
                    "label": info.get("label"),
                    "type": info.get("type"),
                    "value": value,
                }

            html_string = render_to_string('lead/lead_pdf.html', {
                "lead": lead,
                "userprofile": userprofile,
                "bride_contact": lead.contacts.filter(role="כלה").first(),
                "groom_contact": lead.contacts.filter(role="חתן").first(),
                "fields": fields,
            })

            pdf_file = HTML(string=html_string).write_pdf()

        except Exception as e:
            print("PDF ERROR:", e)
            messages.error(request, "לא ניתן ליצור PDF כרגע.")
            return redirect("leads_list")

        try:
            email = EmailMessage(
                subject="הזמנת צילום",
                body=f"מצורף קובץ ההזמנה שלכם.",
                from_email=None,
                to=[chosen_email],
            )

            email.attach(f'lead_{lead.id}.pdf', pdf_file, "application/pdf")
            email.send()

            messages.success(request, "המייל נשלח בהצלחה! ✉️")
        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, "שליחת המייל נכשלה.")
        
        return redirect("leads_list")

    return render(request, "lead/send_email_choice.html", {
        "lead": lead,
        "emails": emails,
    })
