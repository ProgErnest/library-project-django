from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UserProfile(models.Model):
    class Role(models.TextChoices):
        BIBLIOTHECAIRE = "bibliothecaire", _("Bibliothécaire")
        LECTEUR = "lecteur", _("Lecteur")
        ADMIN = "admin", _("Administrateur")

    user = models.OneToOneField(User,related_name="profile",verbose_name=_("User"),  on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.LECTEUR)
    phone_number = models.CharField(max_length=20, blank=True, verbose_name=_("Phone Number"))
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))
    created_at = models.DateField(null=True, blank=True, verbose_name=_("Date Created"))

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
    def __str__(self):
        return f"{self.user.username} - ({self.get_role_display()})"

    @property
    def is_bibliothecaire(self):
        return self.role == self.Role.BIBLIOTHECAIRE
    @property
    def is_lecteur(self):
        return self.role == self.Role.LECTEUR
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN