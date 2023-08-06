import django
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django.contrib.sites",
            "medux.common",
            "medux.settings",
        ],
    )
    django.setup()


@pytest.fixture
def django_user_model():
    return get_user_model()
