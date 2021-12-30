from crum import get_current_user
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


class UserStampedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column='created_by',
        related_name='%(class)ss_created_by',
        related_query_name='%(class)s_created_by',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column='updated_by',
        related_name='%(class)ss_updated_by',
        related_query_name='%(class)s_updated_by',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)


class User(AbstractUser, TimeStampedModel, UserStampedModel):
    GENDER = Choices(
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    birth_date = models.DateField("Birth Date", blank=True, null=True)
    gender = models.CharField("Gender", choices=GENDER,
        blank=True, max_length=50, null=True)
