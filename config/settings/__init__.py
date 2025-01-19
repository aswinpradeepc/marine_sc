"""
Django settings module.

This file acts as the entry point for your Django project's settings.
"""
from .third_party import *

# Load the appropriate settings file based on the environment
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .prod import *
elif ENVIRONMENT == 'development':
    from .local import *
else:
    raise ValueError(f"Invalid environment '{ENVIRONMENT}'")
