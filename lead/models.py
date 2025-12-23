from operator import concat
from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    
    DAYS = [
        ('א','א'),
        ('ב','ב'),
        ('ג','ג'),
        ('ד','ד'),
        ('ה','ה'),
        ('ו','ו'),
    ]

    HEBREW_MONTHS = [
    ('תשרי', 'תשרי'),
    ('חשוון', 'חשוון'),
    ('כסלו', 'כסלו'),
    ('טבת', 'טבת'),
    ('שבט', 'שבט'),
    ('אדר', 'אדר'),
    ('ניסן', 'ניסן'),
    ('אייר', 'אייר'),
    ('סיון', 'סיון'),
    ('תמוז', 'תמוז'),
    ('אב', 'אב'),
    ('אלול', 'אלול'),
    ]
    STATUS_CHOICES = [
    ('contacted', 'יצר קשר'),
    ('closed', 'סגר עסקה'),
    ('served', 'קיבל שירות'),
    ]

    PAYMENT_STATUS_CHOICES = [
    ('unpaid', 'לא שילם'),
    ('partial', 'שילם חלקית'),
    ('paid', 'שילם במלואו'),
    ]
    PAYMENT_METHOD = [
    ('credit-card', 'אשראי'),
    ('bank-transfer', 'העברה בנקאית'),
    ('cash', 'מזומן'),
    ]
    bride_side = models.CharField(verbose_name="משפחת הכלה", max_length=20)
    groom_side = models.CharField(verbose_name="משפחת החתן", max_length=20)
    address = models.CharField(verbose_name="כתובת האולם", max_length=40, blank=True, default="")
    day = models.CharField(verbose_name="יום", max_length=1, choices=DAYS, blank=True, default="")
    hebrew_day = models.CharField(verbose_name="יום עברי", max_length=10, blank=True, default="")
    hebrew_month = models.CharField(verbose_name="חודש עברי", max_length=10, choices=HEBREW_MONTHS, blank=True, default="")
    hebrew_year = models.CharField(verbose_name="שנה עברית", max_length=10, blank=True, default="")
    date_gregorian = models.DateField(verbose_name="תאריך לועזי", null=True, blank=True)
    hour = models.CharField(verbose_name="שעה", max_length=10,blank=True, default="לא נקבע")
    hall = models.CharField(max_length=255, verbose_name="אולם", blank=True, default="")
    additional_details = models.TextField(verbose_name="פרטים נוספים", blank=True, default="")
    additional_crew = models.CharField(verbose_name="צלמת",max_length=50, blank=True, null=True, default="")
    has_additional_crew = models.BooleanField(verbose_name="רוצים צלמת בנוסף?", default=False)
    video = models.CharField(verbose_name="וידאו",max_length=50, blank=True, default="❓")
    assistent = models.CharField(verbose_name="עוזר",max_length=50, blank=True, default="❓")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='contacted')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(verbose_name="אמצעי תשלום",max_length=20, choices=PAYMENT_METHOD, default='')
    custom_fields = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.bride_side} - {self.groom_side} - {self.date_gregorian}"

class Contact(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(verbose_name="שם פרטי", max_length=100, default="")
    second_name = models.CharField(verbose_name="שם משפחה", max_length=100, default="")
    phone = models.CharField(verbose_name="טלפון", max_length=20,blank=True, null=True)
    email = models.EmailField(verbose_name="אימייל", blank=True, null=True)
    role = models.CharField(verbose_name="קשר לבעלי השמחה:", max_length=50, blank=True, null=True)
    concat_address = models.CharField(verbose_name="כתובת", max_length=50, blank=True, null=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.second_name}".strip()
        return f"{full_name} ({self.role})"

