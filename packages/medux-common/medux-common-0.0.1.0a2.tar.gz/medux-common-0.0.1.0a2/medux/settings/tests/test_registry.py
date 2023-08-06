import pytest

from medux.settings import SettingsRegistry, Scope


def test_register_key():
    SettingsRegistry.register("namespace", "key1", [Scope.USER, Scope.VENDOR])
    assert SettingsRegistry.exists("namespace", "key1", Scope.USER)


def test_register_wrong_key():
    SettingsRegistry.register("namespace", "key2", [Scope.USER, Scope.VENDOR])
    assert SettingsRegistry.exists("namespace", "key33", Scope.USER) == False


def test_register_wrong_namespace():
    SettingsRegistry.register("namespace", "key3", [Scope.USER, Scope.VENDOR])
    assert SettingsRegistry.exists("foospace", "key45", Scope.USER) == False


def test_register_wrong_scope():
    SettingsRegistry.register("namespace", "key4", [Scope.USER, Scope.VENDOR])
    assert SettingsRegistry.exists("namespace", "key4", Scope.DEVICE) == False


def test_register_implicitly_vendor_scope():
    """check if registered settings add VENDOR scope automatically"""
    SettingsRegistry.register("namespace", "key5", [Scope.USER])
    assert SettingsRegistry.exists("namespace", "key5", Scope.VENDOR) == True


def test_retrieve_scopes():
    SettingsRegistry.register("namespace", "key6", [Scope.USER, Scope.DEVICE])
    assert SettingsRegistry.scopes("namespace", "key6") == {
        Scope.USER,
        Scope.DEVICE,
        Scope.VENDOR,
    }


def test_retrieve_empty_scopes():
    SettingsRegistry.register("namespace", "key_empty", [])
    assert SettingsRegistry.scopes("namespace", "key_empty") == {
        Scope.VENDOR,
    }


def test_retrieve_vendor_scopes():
    SettingsRegistry.register("namespace", "key_vendor", [Scope.VENDOR])
    assert SettingsRegistry.scopes("namespace", "key_vendor") == {
        Scope.VENDOR,
    }
