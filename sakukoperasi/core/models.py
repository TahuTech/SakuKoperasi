from django.db import models
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Member(models.Model):
    id_member = models.CharField(max_length=50, unique=True)
    id_week = models.CharField(
        max_length=3,
        unique=True,
        blank=True,
        validators=[RegexValidator(r'^\d{3}$', 'id_week must be exactly 3 digits (001-999).')],
    )
    id_month = models.CharField(
        max_length=4,
        unique=True,
        blank=True,
        validators=[RegexValidator(r'^\d{4}$', 'id_month must be exactly 4 digits (0001-9999).')],
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    guaranted_id = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='guaranteed_members',
    )

    def __str__(self):
        return f"{self.id_member} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.id_week:
            max_id = (
                Member.objects.filter(id_week__regex=r'^\d+$')
                .annotate(id_num=Cast('id_week', IntegerField()))
                .aggregate(max_id=Max('id_num'))['max_id']
                or 0
            )
            next_id = max_id + 1
            if next_id > 999:
                raise ValidationError('id_week exceeded maximum value 999.')
            self.id_week = f"{next_id:03d}"
        else:
            if not str(self.id_week).isdigit():
                raise ValidationError('id_week must contain only numbers.')
            normalized = int(self.id_week)
            if normalized < 1 or normalized > 999:
                raise ValidationError('id_week must be between 001 and 999.')
            self.id_week = f"{normalized:03d}"

        if not self.id_month:
            max_month = (
                Member.objects.filter(id_month__regex=r'^\d+$')
                .annotate(id_num=Cast('id_month', IntegerField()))
                .aggregate(max_id=Max('id_num'))['max_id']
                or 0
            )
            next_month = max_month + 1
            if next_month > 9999:
                raise ValidationError('id_month exceeded maximum value 9999.')
            self.id_month = f"{next_month:04d}"
        else:
            if not str(self.id_month).isdigit():
                raise ValidationError('id_month must contain only numbers.')
            normalized_month = int(self.id_month)
            if normalized_month < 1 or normalized_month > 9999:
                raise ValidationError('id_month must be between 0001 and 9999.')
            self.id_month = f"{normalized_month:04d}"

        super().save(*args, **kwargs)


class LoanRule(models.Model):
    class LoanType(models.TextChoices):
        WEEKLY = 'weekly', 'Mingguan'
        MONTHLY = 'monthly', 'Bulanan'

    loan_type = models.CharField(
        max_length=10,
        choices=LoanType.choices,
        unique=True,
    )
    max_loan_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='Maksimal jumlah pinjaman',
    )
    max_installments = models.PositiveIntegerField(
        help_text='Jumlah maksimal cicilan',
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Bunga pinjaman dalam persen (%)',
    )

    def __str__(self):
        return f"{self.get_loan_type_display()} - Maks {self.max_loan_amount} / {self.max_installments}x cicilan"


class LoanRateTable(models.Model):
    loan_rule = models.ForeignKey(
        LoanRule,
        on_delete=models.CASCADE,
        related_name='rate_tables',
        limit_choices_to={'loan_type': LoanRule.LoanType.MONTHLY},
        help_text='Aturan pinjaman (hanya bulanan)',
    )
    loan_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='Jumlah pokok pinjaman',
    )
    installment_count = models.PositiveIntegerField(
        help_text='Jumlah cicilan (bulan)',
    )
    installment_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='Besar angsuran per bulan',
    )
    admin_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text='Biaya administrasi',
    )

    class Meta:
        unique_together = ('loan_rule', 'loan_amount', 'installment_count')

    def __str__(self):
        return (
            f"{self.loan_amount} / {self.installment_count}x "
            f"→ angsuran {self.installment_amount}, admin {self.admin_fee}"
        )
