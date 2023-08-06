import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from medux.settings import SettingsRegistry, Scope
from medux.settings.models import ScopedSettings


@pytest.fixture
def user_admin():
    admin = get_user_model().objects.create(username="admin")
    admin.save()
    return admin


@pytest.fixture
def user_nobody():
    nobody = get_user_model().objects.create(username="nobody")
    nobody.save()
    return nobody


@pytest.fixture
def dummy_group():
    group = Group.objects.create(name="dummy")
    group.save()
    return group


@pytest.mark.django_db
def test_settings_get_nonexisting():
    """test if non-existing setting returns None"""
    SettingsRegistry.register("test", "non_existing", [Scope.VENDOR])
    assert ScopedSettings.get("test", "non_existing", Scope.VENDOR) is None


@pytest.mark.django_db
def test_settings_integer(user_admin, user_nobody):
    """test if an int settings returns actually an int"""
    SettingsRegistry.register("test", "int_setting", [Scope.USER])
    ScopedSettings.set("test", "int_setting", 42, Scope.USER, user=user_admin)

    assert ScopedSettings.get("test", "int_setting", Scope.USER, user=user_admin) == 42
    assert (
        ScopedSettings.get("test", "int_setting", Scope.USER, user=user_nobody) == None
    )


@pytest.mark.django_db
def test_settings_integer_casting(admin_user):
    """test if an int settings returns actually an int"""
    SettingsRegistry.register("test", "cast_int_setting", [Scope.USER])
    ScopedSettings.set("test", "cast_int_setting", "42", Scope.USER, user=admin_user)

    assert (
        ScopedSettings.get("test", "cast_int_setting", Scope.USER, user=admin_user)
        == 42
    )


@pytest.mark.django_db
def test_settings_str(admin_user):
    """test if a str settings actually returns a str"""
    SettingsRegistry.register("test", "str_setting", [Scope.USER])
    ScopedSettings.set("test", "str_setting", "42a", Scope.USER, user=admin_user)

    assert (
        ScopedSettings.get("test", "str_setting", Scope.USER, user=admin_user) == "42a"
    )


@pytest.mark.django_db
def test_settings_bool_true(admin_user):
    """test if a bool:True settings actually returns bool:True"""
    SettingsRegistry.register("test", "true_setting", [Scope.USER])
    ScopedSettings.set("test", "true_setting", True, Scope.USER, user=admin_user)
    assert (
        ScopedSettings.get("test", "true_setting", Scope.USER, user=admin_user) is True
    )


@pytest.mark.django_db
def test_settings_bool_false(admin_user):
    """test if a bool:False settings actually returns bool:False"""
    SettingsRegistry.register("test", "false_setting", [Scope.USER])
    ScopedSettings.set("test", "false_setting", False, Scope.USER, user=admin_user)
    assert (
        ScopedSettings.get("test", "false_setting", Scope.USER, user=admin_user)
        is False
    )


@pytest.mark.django_db
def test_settings_set_get_USER(admin_user, user_nobody):
    """test if a USER scoped setting returns the correct user and key"""
    SettingsRegistry.register("test", "user_setting", [Scope.USER])
    ScopedSettings.set("test", "user_setting", "foo", Scope.USER, user=admin_user)

    assert (
        ScopedSettings.get("test", "user_setting", Scope.USER, user=admin_user) == "foo"
    )
    assert (
        ScopedSettings.get("test", "user_setting", Scope.USER, user=user_nobody) is None
    )


@pytest.mark.django_db
def test_settings_set_get_USER_overwrite(admin_user):
    """test if a USER scoped setting returns the correct user and key"""
    SettingsRegistry.register("test", "user_setting", [Scope.USER])
    ScopedSettings.set("test", "user_setting", "foo", Scope.USER, user=admin_user)
    ScopedSettings.set("test", "user_setting", "foo2", Scope.USER, user=admin_user)

    assert (
        ScopedSettings.get("test", "user_setting", Scope.USER, user=admin_user)
        == "foo2"
    )


@pytest.mark.django_db
def test_settings_set_get_VENDOR():
    SettingsRegistry.register("test", "vendor_setting", [Scope.VENDOR])
    ScopedSettings.set("test", "vendor_setting", "shdkjhf", Scope.VENDOR)

    assert ScopedSettings.get("test", "vendor_setting", Scope.VENDOR) == "shdkjhf"


@pytest.mark.django_db
def test_settings_set_get_default_scope():
    SettingsRegistry.register("test", "vendor_setting", [Scope.VENDOR])
    ScopedSettings.set("test", "vendor_setting", 42, Scope.VENDOR)

    assert ScopedSettings.get("test", "vendor_setting", Scope.VENDOR) == 42


@pytest.mark.django_db
def test_settings_set_get_without_user_fk_object():
    SettingsRegistry.register("test", "vendor_setting", [Scope.USER])
    with pytest.raises(AttributeError):
        ScopedSettings.set("test", "vendor_setting", 45, Scope.USER)


@pytest.mark.django_db
def test_settings_set_get_specific_scope(user_admin, user_nobody, dummy_group):
    """Make sure scope with the highest priority is returned when more than one scopes
    are available for a key"""
    SettingsRegistry.register("test", "multiple_setting", [Scope.VENDOR, Scope.USER])
    ScopedSettings.set("test", "multiple_setting", 42, Scope.VENDOR)
    ScopedSettings.set("test", "multiple_setting", 43, Scope.USER, user=user_admin)
    ScopedSettings.set(
        "test", "multiple_setting", 52, Scope.GROUP, group=dummy_group
    )  # dummy

    assert (
        ScopedSettings.get("test", "multiple_setting", Scope.USER, user=user_admin)
        == 43
    )
