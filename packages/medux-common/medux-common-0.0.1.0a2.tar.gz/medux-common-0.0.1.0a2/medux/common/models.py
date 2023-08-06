import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class CreatedModifiedModel(models.Model):
    """A simple mixin for model classes that need to have created/modified fields."""

    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = AutoDateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Custom Django Manager for soft-delete queries.

    This object manager transparently only fetches objects from the
    database that are not soft-deleted."""

    # https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModel(CreatedModifiedModel):
    """An abstract base class with common used functions.

    Every relevant model that needs soft_deletion in MedUX should inherit BaseModel.

    It provides:
    * basic created/modified timestamps for auditing
    * a soft delete functionality: Deleted items are just marked as deleted.
    """

    deleted_at = models.DateTimeField(
        editable=False, blank=True, null=True, default=None
    )

    row_version = models.PositiveIntegerField(editable=False, default=0)

    # The standard manager only returns not-soft-deleted objects
    objects = SoftDeletionManager()

    # The all_objects Manager returns ALL objects, even soft-deleted ones
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class User(AbstractUser):
    """Custom MedUX User model.

    To be modified later if needed.
    """


SEX = (("m", _("male")), ("f", _("female")))


class Client(models.Model):
    """A MedUX client, like an MD who "owns" a homepage, or a MedUX appliance."""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        help_text=_(
            "The associated system user, if a client needs access to services."
        ),
    )
    title = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True, default="", blank=True)

    @property
    def name(self):
        # TODO: if user exists, take his name.
        return f"{self.last_name}, {self.first_name}"

    def __str__(self):
        return f"{self.name}"
