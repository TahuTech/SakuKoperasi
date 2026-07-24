from django.core.management.base import BaseCommand

from core.models import LoanRule, LoanRateTable


LOAN_RULES = [
    {
        'loan_type': LoanRule.LoanType.WEEKLY,
        'max_loan_amount': 1_000_000,
        'max_installments': 10,
        'interest_rate': 10.00,
    },
    {
        'loan_type': LoanRule.LoanType.MONTHLY,
        'max_loan_amount': 5_000_000, #masimal pinjaman 5 juta
        'max_installments': 12,
        'interest_rate': 0.00,
    },
]

# (loan_amount, installment_count, installment_amount, admin_fee)
MONTHLY_RATE_TABLES = [
    (1_000_000, 6,  187_000, 50_000),
    (1_000_000, 10, 120_000, 50_000),
    (1_000_000, 12, 104_000, 50_000),
    (1_250_000, 6,  234_000, 55_000),
    (1_250_000, 10, 150_000, 55_000),
    (1_250_000, 12, 130_000, 55_000),
    (1_500_000, 6,  280_000, 60_000),
    (1_500_000, 10, 180_000, 60_000),
    (1_500_000, 12, 155_000, 60_000),
]


class Command(BaseCommand):
    help = 'Seed default loan rules and monthly rate tables.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing loan rules and rate tables before seeding.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            LoanRateTable.objects.all().delete()
            LoanRule.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing loan rules cleared.'))

        for data in LOAN_RULES:
            rule, created = LoanRule.objects.update_or_create(
                loan_type=data['loan_type'],
                defaults={
                    'max_loan_amount': data['max_loan_amount'],
                    'max_installments': data['max_installments'],
                    'interest_rate': data['interest_rate'],
                },
            )
            label = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(
                    f"{label} LoanRule: {rule}"
                )
            )

        monthly_rule = LoanRule.objects.get(loan_type=LoanRule.LoanType.MONTHLY)

        for loan_amount, installment_count, installment_amount, admin_fee in MONTHLY_RATE_TABLES:
            entry, created = LoanRateTable.objects.update_or_create(
                loan_rule=monthly_rule,
                loan_amount=loan_amount,
                installment_count=installment_count,
                defaults={
                    'installment_amount': installment_amount,
                    'admin_fee': admin_fee,
                },
            )
            label = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(
                    f"{label} LoanRateTable: {entry}"
                )
            )

        self.stdout.write(self.style.SUCCESS('Loan rules seeded successfully.'))
