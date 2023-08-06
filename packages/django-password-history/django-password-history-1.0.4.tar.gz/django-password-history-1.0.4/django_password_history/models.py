#
# Created on Tue Dec 21 2021
#
# Copyright (c) 2021 Lenders Cooperative, a division of Summit Technology Group, Inc.
#

from django.db import models
from django.conf import settings
from django.apps import apps
from django.contrib.auth.hashers import make_password, check_password


class UserPasswordHistory(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password_1 = models.CharField(blank=True, null=True, max_length=128)
    password_2 = models.CharField(blank=True, null=True, max_length=128)
    password_3 = models.CharField(blank=True, null=True, max_length=128)
    password_4 = models.CharField(blank=True, null=True, max_length=128)
    password_5 = models.CharField(blank=True, null=True, max_length=128)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + "_password_history"

    def password_is_used(self, password, site_id=1):
        previous_passwords_count = 5
        SiteSettings = None

        use_site_setting_password_history = getattr(settings,"USE_SITE_SETTINGS_PASSWORD_HISTORY",False)
        
        try:
            SiteSettings = apps.get_model("setup","SiteSettings")
        except:
            SiteSettings = None

        if use_site_setting_password_history and SiteSettings:
            previous_passwords_count = SiteSettings.objects.get(id=site_id).previous_password_count
        else:
            previous_passwords_count = getattr(settings,"PREVIOUS_PASSWORD_COUNT", 5)

        if previous_passwords_count:
            for x in range(1, min(previous_passwords_count, 5) + 1):
                f = getattr(self, f'password_{x}', None)
                if f is not None and check_password(password, f):
                    return True

        return False

    def store_password(self):
        self.password_5 = self.password_4
        self.password_4 = self.password_3
        self.password_3 = self.password_2
        self.password_2 = self.password_1
        self.password_1 = self.user.password
        self.save()