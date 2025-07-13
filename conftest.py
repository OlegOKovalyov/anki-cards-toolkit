import os
import pytest

@pytest.fixture(autouse=True, scope="session")
def set_user_locale():
    """Set USER_LOCALE to 'en' for all tests to avoid language prompts."""
    os.environ['USER_LOCALE'] = 'en'
    yield
    # Clean up after all tests
    if 'USER_LOCALE' in os.environ:
        del os.environ['USER_LOCALE'] 