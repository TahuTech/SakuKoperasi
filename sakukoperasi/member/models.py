from django.db import models


class Member(models.Model):
    id_member = models.CharField(max_length=50, unique=True)
    id_week = models.CharField(max_length=20)
    id_month = models.CharField(max_length=20)
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
