import pytest
from django.contrib.auth import get_user_model

# from django.contrib.sites.models import Site

from medux.settings import CachedSettings, Scope
from medux.settings.models import ScopedSettings

# from django.core.management import call_command


# @pytest.fixture(scope="session")
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command("loaddata", "initial.yaml")


@pytest.mark.django_db
def test_cachedsettings_namespace(request):
    namespace = CachedSettings(request).mynamespace
    assert type(namespace) == CachedSettings.Namespace


@pytest.mark.django_db
def test_cachedsettings_key_None(request):

    key = CachedSettings(request).test.non_existing_key
    assert key is None


@pytest.mark.django_db
def test_cachedsettings_existing_key_vendor(request):

    ScopedSettings.set("space", "my_key", 42, Scope.VENDOR)
    assert CachedSettings(request).space.my_key == 42


# FIXME: get rid of homepage dependency
# @pytest.mark.django_db
# def test_cachedsettings_existing_key_client(request, django_db_setup):
#
#     ScopedSettings.set("space", "my_key", 42, Scope.CLIENT)
#     request.site = Site.objects.get(pk=1)
#     space = CachedSettings(request).space
#     key = space.my_key
#     assert key == 42


@pytest.mark.django_db
def test_cachedsettings_existing_key_user(request):
    user1 = get_user_model().objects.create(username="user1", password="user1")
    user1.save()

    ScopedSettings.set("space", "my_key", 42, Scope.USER, user=user1)
    request.user = user1
    assert CachedSettings(request).space.my_key == 42


@pytest.mark.django_db
def test_cachedsettings_existing_key_wrong_user(request):
    user1 = get_user_model().objects.create(username="user1", password="user1")
    user1.save()
    user2 = get_user_model().objects.create(username="user2", password="user2")
    user2.save()

    ScopedSettings.set("space", "my_key", 42, Scope.USER, user=user1)
    request.user = user2
    assert CachedSettings(request).space.my_key == None


@pytest.mark.django_db
def test_cachedsettings_existing_key_user_fallback_vendor(request):
    user1 = get_user_model().objects.create(username="user1", password="user1")
    user1.save()
    user2 = get_user_model().objects.create(username="user2", password="user2")
    user2.save()

    ScopedSettings.set("space", "my_key", 41, Scope.VENDOR)
    ScopedSettings.set("space", "my_key", 42, Scope.USER, user=user1)
    request.user = user2
    assert CachedSettings(request).space.my_key == 41
