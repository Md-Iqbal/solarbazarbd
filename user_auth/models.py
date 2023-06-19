from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the customer site.'),
    )
    is_vendor = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the vendor site.'),
    )
    is_agent = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the agent site.'),
    )
    is_admin = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    # is_agent = models.BooleanField(
    #     default=False,
    #     help_text=_('Designates whether the user can log into the admin site.'),
    # )

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')
