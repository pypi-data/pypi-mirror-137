#  MedUX - Open Source Electronical Medical Record
#  Copyright (c) 2022  Christian González
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import Union, Tuple, List

import enumfields
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from medux.common.models import Client
from medux.settings import SettingsRegistry, Scope


class ScopedSettings(models.Model):
    """Convenience access model class for all scoped MedUX settings.

    You can easily access settings using ScopedSettings.get(namespace, key, scope, ...)
    """

    class Meta:
        verbose_name = verbose_name_plural = _("Scoped settings")
        ordering = ["namespace", "key", "scope"]
        unique_together = [
            # ["namespace", "key", "scope", "client"],
            ["namespace", "key", "scope", "group"],
            # ["namespace", "key", "scope", "device"],
            ["namespace", "key", "scope", "user"],
        ]
        permissions = [
            ("change_own_user_settings", _("Can change own user's Scoped settings")),
            (
                "change_own_client_settings",
                _("Can change own client's Scoped settings"),
            ),
        ]

    client = models.ForeignKey(
        Client,
        verbose_name=_("Client"),
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    # device = models.ForeignKey(
    #     "Device", on_delete=models.CASCADE, default=None, null=True, blank=True
    # )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    namespace = models.CharField(max_length=25)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    scope = enumfields.EnumIntegerField(Scope)

    def clean(self):
        self.namespace = str(self.namespace).lower()
        self.key = str(self.key).lower()

    @classmethod
    def create(cls, namespace: str, key: str, scope: Scope):
        """Creates an (empty) settings entry in the database.

        Does not overwrite existing values.
        """
        cls.assure_exists(namespace, key, scope)
        s, created = ScopedSettings.objects.get_or_create(
            namespace=namespace, key=key, scope=scope
        )
        if created:
            s.save()

    @classmethod
    def get(
        cls,
        namespace: str,
        key: str,
        scope: Scope,
        user=None,
        group=None,
        device=None,
        client=None,
    ):
        """Retrieve a settings key in a convenient way.

        :returns namespaced settings value, according to scope and, if applicable, the related
        object like user, group etc.

        :param namespace: the namespace this key is saved under. Usually the app's name.
        :param key: the key to be retrieved
        :param scope: the scope that key is valid for. If scope is None, and more than one keys are
            saved under that scope, the key with the highest priority is taken:
            USER > DEVICE > GROUP > CLIENT > VENDOR
        :param user: if scope is USER, you have to provide a User object
            that key/scope is valid for.
        :param group: if scope is GROUP, you have to provide a SettingsGroup object
            that key/scope is valid for.
        :param device: if scope is DEVICE, you have to provide a Device object
            that key/scope is valid for.
        :param client: if scope is CLIENT, you have to provide a Client object
            that key/scope is valid for.
        """

        cls.assure_exists(namespace, key, scope)

        filters = {
            "namespace": namespace,
            "key": key,
        }
        if scope:
            filters["scope"] = scope
            if scope == Scope.USER:
                filters["user"] = user
            elif scope == Scope.GROUP:
                filters["group"] = group
            elif scope == Scope.DEVICE:
                filters["device"] = device
            elif scope == Scope.CLIENT:
                filters["client"] = client

        objects = ScopedSettings.objects.filter(**filters)
        if len(objects) == 0:
            return None
        if len(objects) == 1:
            value = objects.first().value  # type: str
        else:
            # more than one scopes under that key and scope
            raise KeyError(
                f"There are multiple settings keys under {namespace}.{key}{[objects]}"
            )
        # filter out int and boolean values and return them instead.
        if value.isnumeric():
            return int(value)
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False

        return value

    @classmethod
    def set(
        cls,
        namespace: str,
        key: str,
        value: Union[str, int, bool],
        scope: Scope,
        user=None,
        client=None,
        device=None,
        group=None,
    ):

        """Sets a settings key."""

        cls.assure_exists(namespace, key, scope)

        (item, created) = ScopedSettings.objects.get_or_create(
            namespace=namespace, key=key, scope=scope
        )
        # set correct scope
        if scope == Scope.USER:
            if user is None:
                raise AttributeError(
                    "When scope==USER, a user object must be provided."
                )
            item.user = user

        elif scope == Scope.DEVICE:
            if device is None:
                raise AttributeError(
                    "When scope==DEVICE, a device object must be provided."
                )
            item.device = device

        elif scope == Scope.GROUP:
            if group is None:
                raise AttributeError(
                    "When scope==GROUP, a group object must be provided."
                )
            item.group = group

        elif scope == Scope.CLIENT:
            if client is None:
                raise AttributeError(
                    "When scope==CLIENT, a client object must be provided."
                )
            item.client = client

        item.value = str(value)
        item.namespace = namespace
        item.save()

    @classmethod
    def keys(cls) -> List[Tuple[str, str]]:
        """:returns: a Tuple[namespace,key] of all currently available keys."""

        return [(item.namespace, item.key) for item in cls.objects.all()]

    @classmethod
    def namespaces(cls):
        """:returns: a list of available namespaces."""
        # FIXME this is highly insufficient. distinct() would be better, but not available on SQLite/dev
        result = set()
        for s in ScopedSettings.objects.order_by("namespace").values_list(
            "namespace", flat=True
        ):
            result.add(s)
        return list(result)

    def __str__(self):
        # add user, client, group
        fk = ""
        if self.scope == Scope.USER:
            fk = f": '{self.user}'"
        elif self.scope == Scope.GROUP:
            fk = f": '{self.group}'"
        a = f"{'.'.join([self.namespace, self.key])} [{self.scope.name}{fk}]: {self.value}"
        return a

    @classmethod
    def assure_exists(cls, namespace, key, scope):
        """Raises KeyError if given settings are not registered."""
        if not SettingsRegistry.exists(namespace, key, scope):
            raise KeyError(f"Setting {namespace}.{key}/{scope.name} is not registered.")
