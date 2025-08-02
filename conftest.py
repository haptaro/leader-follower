import pytest
import django
from django.conf import settings
from django.test.utils import get_runner


def pytest_configure():
    """
    Configure Django settings for pytest.
    """
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'api',
        ],
        SECRET_KEY='test-secret-key',
        USE_TZ=True,
    )
    django.setup()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Enable database access for all tests.
    """
    pass
