from celery import shared_task
from django.template.loader import render_to_string
from lead.models import Lead
from celery import shared_task
from userprofile.models import Userprofile
from weasyprint import HTML
import logging
import resend
import base64


logger = logging.getLogger(__name__)

@shared_task
def send_lead_pdf_task(lead_id, user_id, chosen_email):
    # 1. בדיקת ה-Lead בנפרד
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f"Task DB error: Lead ID {lead_id} does not exist.")
        return "Failed: Lead Not Found" # ⬅️ הודעה ספציפית

    # 2. בדיקת ה-Userprofile בנפרד
    try:
        userprofile = Userprofile.objects.get(user_id=user_id)
    except Userprofile.DoesNotExist:
        logger.error(f"Task DB error: Userprofile for User ID {user_id} does not exist.")
        return "Failed: Userprofile Not Found" # ⬅️ הודעה ספציפית

    except Exception as e:
         # לכסות שגיאות DB אחרות (כמו בעיית חיבור)
         logger.error(f"Task DB error (Other): {e}")
         return "Failed: DB error (Other)"

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
        pdf_base64 = base64.b64encode(pdf_file).decode("utf-8")
    except Exception as e:
        logger.error(f"PDF creation failed: {e}")
        return "Failed: PDF error"


    try:
        resend.Emails.send({
            "from": "Mazal Tov CRM <no-reply@mazaltovcrm.com>",
            "to": chosen_email,
            "subject": "הזמנת צילום – מצורף קובץ",
            "html": "<p>מצורף קובץ ההזמנה שלכם.</p>",
            "attachments": [
                {
                    "filename": f"lead_{lead.id}.pdf",
                    "content": pdf_base64,
                }
            ],
        })
        return "Email sent"
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        return "Failed: Email error"
