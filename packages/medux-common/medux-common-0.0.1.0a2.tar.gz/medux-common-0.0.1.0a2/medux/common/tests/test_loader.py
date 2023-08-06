# empty test so that pytest doesn't fail
# remove this test when you created your own
import pytest

from medux.settings import SettingsRegistry, Scope
from medux.settings.loaders import SettingsLoader


@pytest.mark.django_db
def test_load_key():
    loader = SettingsLoader(scope=Scope.USER)
    SettingsRegistry.register("test_namespace", "test_key", [Scope.USER])
    loader.update_settings({"test_namespace": {"test_key": 42}})


@pytest.mark.django_db
def test_load_key_without_registering():
    loader = SettingsLoader(scope=Scope.VENDOR)
    with pytest.raises(KeyError):
        loader.update_settings({"notexisting_namespace": {"new_key": 42}})
