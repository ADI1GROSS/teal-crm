from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from lead.models import Lead
from userprofile.models import Userprofile
from weasyprint import HTML
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_lead_pdf_task(lead_id, user_id, chosen_email):
    try:
        lead = Lead.objects.get(pk=lead_id)
        userprofile = Userprofile.objects.get(user_id=user_id)
    except Exception as e:
        logger.error(f"Task DB error: {e}")
        return "Failed: DB error"

    # בדיוק כמו ב-view
    bride_contact = lead.contacts.filter(role="כלה").first()
    groom_contact = lead.contacts.filter(role="חתן").first()

    # שדות מותאמים אישית
    template_fields = userprofile.fields or {}
    fields = {}
    for key, info in template_fields.items():
        value = (lead.custom_fields or {}).get(key, info.get("default"))
        fields[key] = {
            "label": info.get("label"),
            "type": info.get("type"),
            "value": value,
        }

    try:
        html_string = render_to_string('lead/lead_pdf.html', {
            'lead': lead,
            'userprofile': userprofile,
            'bride_contact': bride_contact,
            'groom_contact': groom_contact,
            'fields': fields,
        })

        pdf_file = HTML(string=html_string).write_pdf()
    except Exception as e:
        logger.error(f"PDF creation failed: {e}")
        return "Failed: PDF error"

    subject = 'הזמנת צילום'
    message = (
        f'מזל טוב! תודה שבחרתם בשירות של {userprofile.user.username}. '
        f'מצורף קובץ ההזמנה שלכם.'
    )

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=None,
            to=[chosen_email],
        )
        email.attach(f'lead_{lead.id}.pdf', pdf_file, 'application/pdf')
        email.send()
        return "Email sent"
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        return "Failed: Email error"
